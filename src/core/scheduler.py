#!/usr/bin/env python3
"""
AI Automation Scheduler — cron-based bot orchestration engine.
For educational purposes only.

Manages scheduled execution of AI bots with configurable
prompts, delivery targets, and retry logic.
"""

import os
import json
import time
import logging
import threading
from typing import Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("scheduler")


@dataclass
class JobConfig:
    id: str
    name: str
    schedule: str  # cron expression or interval shorthand
    prompt_template: str
    delivery_channel: str = "telegram"
    delivery_target: str = ""
    model_url: str = "http://127.0.0.1:1234/v1"
    model_name: str = "local-model"
    max_tokens: int = 2048
    temperature: float = 0.7
    enabled: bool = True
    retry_count: int = 2
    retry_delay: int = 30
    timeout: int = 60


@dataclass
class JobResult:
    job_id: str
    success: bool
    output: str = ""
    error: str = ""
    duration_ms: int = 0
    timestamp: str = ""


class CronParser:
    """Minimal cron expression parser for scheduling."""

    INTERVALS = {
        "@hourly": 3600,
        "@daily": 86400,
        "@weekly": 604800,
        "@30m": 1800,
        "@15m": 900,
        "@5m": 300,
    }

    @classmethod
    def next_run(cls, schedule: str, last_run: float) -> float:
        if schedule in cls.INTERVALS:
            return last_run + cls.INTERVALS[schedule]

        parts = schedule.split()
        if len(parts) == 5:
            # Standard cron: minute hour day month weekday
            return cls._parse_cron(parts, last_run)

        # Fallback: treat as seconds interval
        try:
            return last_run + int(schedule)
        except ValueError:
            log.warning("Invalid schedule '%s', defaulting to hourly", schedule)
            return last_run + 3600

    @classmethod
    def _parse_cron(cls, parts: list, after: float) -> float:
        minute, hour = parts[0], parts[1]
        now = datetime.fromtimestamp(after)

        target_min = int(minute) if minute != "*" else now.minute
        target_hour = int(hour) if hour != "*" else now.hour

        target = now.replace(
            hour=target_hour, minute=target_min, second=0, microsecond=0
        )

        if target.timestamp() <= after:
            if hour == "*":
                target += timedelta(hours=1)
            else:
                target += timedelta(days=1)

        return target.timestamp()


class Scheduler:
    """Orchestrates scheduled AI bot execution."""

    def __init__(self):
        self.jobs: dict[str, JobConfig] = {}
        self._last_run: dict[str, float] = {}
        self._results: list[JobResult] = []
        self._running = False
        self._lock = threading.Lock()
        self._executor: Optional[Callable] = None
        self._delivery: Optional[Callable] = None

    def register_executor(self, fn: Callable):
        self._executor = fn

    def register_delivery(self, fn: Callable):
        self._delivery = fn

    def add_job(self, job: JobConfig):
        self.jobs[job.id] = job
        if job.id not in self._last_run:
            self._last_run[job.id] = 0
        log.info("Registered job: %s (%s)", job.id, job.schedule)

    def remove_job(self, job_id: str):
        self.jobs.pop(job_id, None)
        self._last_run.pop(job_id, None)

    def load_config(self, config_path: str):
        with open(config_path) as f:
            data = json.load(f)

        for job_data in data.get("jobs", []):
            self.add_job(JobConfig(**job_data))

        log.info("Loaded %d jobs from %s", len(self.jobs), config_path)

    def run(self, check_interval: int = 10):
        self._running = True
        log.info("Scheduler started — %d jobs registered", len(self.jobs))

        while self._running:
            now = time.time()
            for job_id, job in self.jobs.items():
                if not job.enabled:
                    continue

                next_at = CronParser.next_run(
                    job.schedule, self._last_run.get(job_id, 0)
                )

                if now >= next_at:
                    self._execute_job(job)
                    self._last_run[job_id] = now

            time.sleep(check_interval)

    def stop(self):
        self._running = False

    def _execute_job(self, job: JobConfig):
        log.info("Executing: %s", job.id)
        start = time.time()

        for attempt in range(1, job.retry_count + 1):
            try:
                if self._executor:
                    output = self._executor(job)
                else:
                    output = self._default_execute(job)

                duration = int((time.time() - start) * 1000)
                result = JobResult(
                    job_id=job.id,
                    success=True,
                    output=output,
                    duration_ms=duration,
                    timestamp=datetime.now().isoformat(),
                )

                with self._lock:
                    self._results.append(result)

                if self._delivery and job.delivery_target:
                    self._delivery(job.delivery_channel, job.delivery_target, output)

                log.info("Completed: %s (%dms)", job.id, duration)
                return

            except Exception as e:
                log.warning(
                    "Job %s attempt %d/%d failed: %s",
                    job.id, attempt, job.retry_count, e,
                )
                if attempt < job.retry_count:
                    time.sleep(job.retry_delay)

        duration = int((time.time() - start) * 1000)
        result = JobResult(
            job_id=job.id,
            success=False,
            error=str(e),
            duration_ms=duration,
            timestamp=datetime.now().isoformat(),
        )
        with self._lock:
            self._results.append(result)

    def _default_execute(self, job: JobConfig) -> str:
        from urllib.request import urlopen, Request

        payload = json.dumps({
            "model": job.model_name,
            "messages": [
                {"role": "system", "content": "You are an automation assistant."},
                {"role": "user", "content": job.prompt_template},
            ],
            "temperature": job.temperature,
            "max_tokens": job.max_tokens,
        }).encode()

        req = Request(
            f"{job.model_url}/chat/completions",
            data=payload,
            method="POST",
        )
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=job.timeout) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]

    @property
    def recent_results(self) -> list[JobResult]:
        with self._lock:
            return list(self._results[-50:])

    def status(self) -> dict:
        return {
            "running": self._running,
            "jobs_total": len(self.jobs),
            "jobs_enabled": sum(1 for j in self.jobs.values() if j.enabled),
            "executions": len(self._results),
            "last_results": [
                {"id": r.job_id, "ok": r.success, "ms": r.duration_ms}
                for r in self._results[-10:]
            ],
        }

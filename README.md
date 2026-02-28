> **Disclaimer:** This project is for educational and research purposes only. Use responsibly and in compliance with applicable laws and terms of service.

# AI Automation Stack

> **9 AI bots. 1 laptop. 1,000+ automated actions per week. $0.02/day.**

The complete automation system that runs an entire business operation privately on a single machine. Built by a plumber on an old laptop with home wifi.

## The Stack

```
┌─────────────────────────────────────────────────────┐
│                 AUTOMATION ENGINE                     │
│          cron scheduler + message routing             │
├──────────┬──────────┬──────────┬───────────┬────────┤
│ CONTENT  │ MARKET   │ CRYPTO   │ FINANCE   │ GROWTH │
│ 06:00    │ 07:00    │ 08:00    │ 09:00     │ 10:00  │
├──────────┼──────────┼──────────┼───────────┼────────┤
│ NURTURE  │ PROOF    │ SALES    │ PRICE     │        │
│ 12:00    │ 17:00    │ 24/7     │ WATCH 24/7│        │
├──────────┴──────────┴──────────┴───────────┴────────┤
│              LOCAL AI MODEL (LM Studio)              │
│          localhost:1234 — zero cloud dependency       │
├─────────────────────────────────────────────────────┤
│           DELIVERY: Telegram / WhatsApp              │
└─────────────────────────────────────────────────────┘
```

## The 9 Bots

| Bot | Schedule | What It Does |
|-----|----------|-------------|
| **Content AI** | Daily 06:00 | Generates marketing posts for multiple platforms |
| **Market Intel** | Daily 07:00 | Scans opportunities and competitor activity |
| **Crypto Analyst** | Daily 08:00 | Portfolio tracking, price analysis, alerts |
| **Finance AI** | Daily 09:00 | Revenue tracking, expense analysis, forecasting |
| **Growth AI** | Daily 10:00 | Social media automation, engagement metrics |
| **Nurture AI** | Daily 12:00 | Customer engagement, follow-ups, lead warming |
| **Proof AI** | Daily 17:00 | Social proof generation, testimonials, stats |
| **Sales AI** | 24/7 | Auto-delivery, fulfillment checks |
| **Price Watch** | Every 30 min | Real-time price alerts, market movement |

## How It Works

Each bot is a cron job that:
1. Fires at its scheduled time
2. Sends a specialized prompt to the local AI model
3. The AI generates the output (analysis, content, alerts)
4. Results are delivered via Telegram to the owner
5. **Zero data leaves the machine** (except the Telegram delivery)

### Example: Crypto Monitor Bot

```yaml
# cron-config.yaml (example structure)
crypto-monitor:
  schedule: "*/30 * * * *"    # Every 30 minutes
  model: "local"
  prompt_template: |
    Analyze current crypto market conditions.
    Focus on: BTC, ETH, SOL
    Include: price, 24h change, volume, key levels
    Format: brief alert style
  delivery:
    channel: telegram
    target: owner
```

### Example: Content Generator Bot

```yaml
content-blaster:
  schedule: "0 6 * * *"    # Daily at 6 AM
  model: "local"
  prompt_template: |
    Generate marketing content for today.
    Platforms: Twitter, Telegram, LinkedIn
    Tone: professional but accessible
    Theme: private AI, independence from Big Tech
    Include: hook, body, CTA
  delivery:
    channel: telegram
    target: owner
```

## Quick Start

### Prerequisites

- Local AI server running ([Setup Guide](https://github.com/Zombie760/private-ai-quickstart))
- Telegram bot created ([Bot Guide](https://github.com/Zombie760/telegram-ai-bot))
- Node.js 18+ or Python 3.8+

### 1. Clone and Configure

```bash
git clone https://github.com/Zombie760/ai-automation-stack.git
cd ai-automation-stack
cp .env.example .env
# Edit .env with your tokens and model settings
```

### 2. Define Your Bots

```bash
cp config/bots.example.yaml config/bots.yaml
# Customize schedules, prompts, and delivery targets
```

### 3. Start the Engine

```bash
# Using the built-in scheduler
node scheduler.js

# OR using system cron
crontab -e
# Add entries for each bot
```

### 4. Monitor

```bash
# Check bot status
node status.js

# View recent outputs
tail -f logs/automation.log
```

## Scaling

| Setup | Bots | Hardware | Cost |
|-------|------|----------|------|
| Starter | 1-3 | Any laptop, 8GB RAM | $0/day |
| Builder | 4-6 | Decent laptop, 16GB RAM | $0.01/day |
| Boss | 7-9+ | Good laptop or mini PC | $0.02/day |
| Enterprise | 20+ | Desktop or server | $0.05/day |

## Real Results

This exact stack runs a live business:
- **1,000+ automated actions** per week
- **9 specialized bots** handling different business functions
- **$0.02/day** total operating cost
- **Zero human intervention** required for daily operations
- **Zero data** sent to Big Tech

## Project

Built by **SGKx1904** — a plumber who automated an entire business in 48 hours.

- [Website](https://Zombie760.github.io)
- [Live Demo](https://t.me/moneymakingmitch1904_bot)
- [Quick Start](https://github.com/Zombie760/private-ai-quickstart)
- [Full Course](https://github.com/Zombie760/ai-empire-course)

---

*AI For The Rest of Us. 9 bots. 1 laptop. Zero Big Tech.*

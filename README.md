> **Disclaimer:** This project is for educational and research purposes only. Use responsibly and in compliance with applicable laws and terms of service.

# AI Automation Stack

> **9 AI agents. 1 laptop. 1,050+ automated actions per week. $0.02/day.**

The complete automation system that runs an entire business operation privately on a single machine. Built by a plumber in 48 hours with zero coding experience.

## What This Does

While you sleep, 9 AI agents handle your business:

| Agent | Schedule | Function |
|-------|----------|----------|
| **Content Engine** | Daily 06:00 | Marketing posts for Telegram, X, Reddit |
| **Market Intel** | Daily 07:00 | Business opportunities, competitor signals |
| **Crypto Analyst** | Daily 08:00 + every 30 min | Portfolio tracking, price alerts, Fear & Greed |
| **Finance Bot** | Daily 09:00 | Stripe revenue summary, MRR tracking |
| **Growth Generator** | Daily 10:00 | Reddit posts + Twitter threads |
| **Lead Nurture** | Daily 12:00 | Value content + engagement |
| **Social Proof** | Daily 17:00 | Automated stats and proof-of-work |
| **Sales Fulfillment** | Every 15 min | Detect sales, auto-deliver products |
| **Price Watch** | Every 30 min | Real-time crypto price alerts |

## Architecture

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
│           DELIVERY: Telegram / Stripe                │
└─────────────────────────────────────────────────────┘
```

## The Numbers

| Metric | Value |
|--------|-------|
| Automated actions | 1,050+/week |
| Active agents | 9 |
| Operating cost | $0.02/day ($7.30/year) |
| Human intervention required | Zero |
| Data sent to Big Tech | Zero |

## Quick Start

```bash
git clone https://github.com/Zombie760/ai-automation-stack.git
cd ai-automation-stack
cp .env.example .env
# Edit .env with your tokens
cp config/bots.example.json config/bots.json
# Start the engine
python3 src/core/scheduler.py
```

### Prerequisites

- Local AI server running ([Setup Guide](https://github.com/Zombie760/private-ai-quickstart))
- Telegram bot created ([Bot Guide](https://github.com/Zombie760/telegram-ai-bot))
- Python 3.8+ or Node.js 18+

## Links

- [Website](https://Zombie760.github.io)
- [Live Demo Bot](https://t.me/moneymakingmitch1904_bot)
- [Full Course](https://github.com/Zombie760/ai-empire-course)
- [Twitter/X](https://x.com/lyfer1904)

---

*9 agents. 1 laptop. Zero Big Tech. Built from nothing.*

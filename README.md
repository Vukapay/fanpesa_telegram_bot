# FanPesa Telegram Bot & Platform SDK

Production-grade Telegram bot and reusable Platform Integration SDK for
**FanPesa** ([www.fanpesa.com](https://www.fanpesa.com)), built for
[@fanpesa_bot](https://t.me/fanpesa_bot).

The bot exposes FanPesa's Mini App inside Telegram and lets users check
their wallet, browse promotions, and manage deposits/withdrawals — all
betting itself happens inside the Mini App. The backend team has not
shipped real APIs yet, so this milestone runs entirely on a **mock API
layer** behind a clean service boundary, so switching to the real
FanPesa backend later requires no changes to bot commands.

## Overview

- **Telegram bot** (`python-telegram-bot` v22, polling mode) — commands,
  menus, and a Telegram WebApp launch button.
- **FastAPI service** (`app/main.py`) — health/readiness/liveness
  endpoints today; the future home of the FanPesa REST surface and
  Telegram webhook mode.
- **Platform SDK** (`app/platform/`) — a platform-agnostic interface
  (`PlatformAdapter`) implemented by Telegram, browser, and (future)
  Safaricom OneApp adapters, so new client integrations reuse the same
  service layer without duplicating business logic.
- **Mock API** (`app/api/mock.py`) — realistic, randomised sample data
  standing in for the FanPesa backend until it ships.

## Architecture

```text
Telegram / Web / OneApp
        │
        ▼
Command Layer          (app/bot/commands, app/bot/handlers)
        │
        ▼
Platform SDK Layer      (app/platform/base.py, telegram.py, browser.py, oneapp.py)
        │
        ▼
Service Layer           (app/services/*)
        │
        ▼
API / Repository Layer  (app/api/client.py, app/api/mock.py)
        │
        ▼
FanPesa Backend APIs    (not yet available — mocked today)
```

**Rule:** the Telegram bot never calls backend APIs directly. Commands
and handlers only depend on a `PlatformAdapter`; adapters depend on
services; services depend on `app/api/client.py` (real) or
`app/api/mock.py` (today).

### Project layout

```text
app/
├── api/            HTTP client + mock backend
├── bot/            Commands, message handlers, keyboards, application factory
├── config/         Pydantic-settings configuration
├── core/           Constants, exceptions, structured logging, security helpers
├── database/       Redis wrapper (future use)
├── models/         Typed Pydantic domain models
├── platform/       Platform SDK: base interface + Telegram/browser/OneApp adapters
├── services/       Business logic shared across all platforms
├── utils/          Formatting and validation helpers
├── webhooks/        Telegram webhook endpoint (for future webhook-mode)
└── main.py         FastAPI application entry point
```

## Setup

### Prerequisites

- Python 3.12+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Docker (optional, for containerized runs)

### Environment configuration

Copy `.env.example` to `.env` and fill in your bot token:

```powershell
Copy-Item .env.example .env
```

| Variable        | Description                                     | Default                       |
| --------------- | ------------------------------------------------ | ------------------------------ |
| `APP_NAME`      | Application display name                          | `FanPesa Telegram Bot`         |
| `APP_VERSION`   | Application version                               | `1.0.0`                        |
| `ENVIRONMENT`   | `development`, `staging`, or `production`         | `development`                  |
| `DEBUG`         | Enable debug behaviour                            | `True`                         |
| `BOT_TOKEN`     | Telegram bot token — **never commit a real one**  | `CHANGE_ME`                    |
| `WEBHOOK_URL`   | Public URL for webhook mode (leave blank in dev)  | *(empty)*                      |
| `WEBAPP_URL`    | FanPesa Mini App URL opened by the launch button  | `https://www.fanpesa.com`      |
| `API_BASE_URL`  | FanPesa backend base URL (used once available)    | `https://api.fanpesa.com`      |
| `LOG_LEVEL`     | Python logging level                              | `INFO`                         |
| `REDIS_URL`     | Redis connection URL (future use)                 | `redis://localhost:6379`       |

## Running locally

### Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run the API

```powershell
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/` for application metadata, or
`http://127.0.0.1:8000/health` for a mock-backed health check.

### Run the bot

```powershell
python -m app.bot.application
```

The bot runs in polling mode and responds to `/start`, `/help`,
`/about`, and `/support`, plus the persistent menu buttons (Wallet,
Promotions, Deposit, Withdraw).

## Running with Docker

```powershell
docker compose up --build
```

This starts the FastAPI app (port `8000`) and a Redis instance,
loading configuration from `.env` and mounting the project directory
for live-reload during development. Run the bot separately (Docker
Compose here only runs the API + Redis):

```powershell
docker compose exec app python -m app.bot.application
```

## Telegram bot configuration

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the
   token into `.env` as `BOT_TOKEN`.
2. (Optional) Register the FanPesa Mini App with BotFather so
   `https://www.fanpesa.com` is allow-listed as a WebApp URL.
3. Start the bot with `python -m app.bot.application` — polling mode
   requires no public URL.
4. For production, switch to webhook mode: set `WEBHOOK_URL`, call
   `setWebhook` pointing at `{WEBHOOK_URL}/webhooks/telegram`, and stop
   running the polling process (`app/webhooks/telegram.py` already
   implements the receiving endpoint).

## Future backend integration

Every service in `app/services/` currently calls `app/api/mock.py`.
Once the FanPesa backend is available:

1. Implement the equivalent endpoints against `app/api/client.py`
   (`APIClient.get` / `APIClient.post`).
2. Swap the `mock_api` import in each service for `api_client` calls.
3. No changes are required in `app/bot/`, `app/platform/`, or
   `app/main.py` — they depend on service/adapter interfaces, not on
   how data is sourced.

The same `app/platform/base.py` interface is designed to be reused by
future browser and Safaricom OneApp integrations (`app/platform/browser.py`,
`app/platform/oneapp.py`) without duplicating business logic.

## Development workflow

- Format code: `black .`
- Sort imports: `isort .`
- Lint: `ruff check .`
- Run all checks locally before pushing (CI runs the same steps):

  ```powershell
  ruff check . ; black --check . ; isort --check-only . ; pytest
  ```

## Testing

```powershell
pytest
```

Test suite layout:

- `tests/integration/` — FastAPI endpoint tests
- `tests/services/` — service-layer unit tests (wallet, promotions)
- `tests/commands/` — Telegram command unit tests (`/start`)

## Deployment guidance

- Build and run the production image via the provided `Dockerfile`
  (non-root user, port `8000`, `uvicorn` entrypoint).
- Run the FastAPI process and the Telegram bot process independently —
  they scale differently and a bot crash should never take down the
  health-checked API.
- In production, prefer Telegram **webhook mode** over polling (see
  above) so the bot can run behind the same infrastructure as the API.
- Provide `BOT_TOKEN`, `WEBHOOK_URL`, `API_BASE_URL`, and `REDIS_URL`
  via your deployment platform's secret/environment management — never
  commit real values to `.env`.

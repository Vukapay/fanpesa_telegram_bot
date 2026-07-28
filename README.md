# FanPesa Telegram Bot & Platform SDK

Production-grade Telegram bot and reusable Platform Integration SDK for
**FanPesa** ([www.fanpesa.com](https://www.fanpesa.com)), built for
[@fanpesa_bot](https://t.me/fanpesa_bot).

The bot's menu (Register, Login, Deposit, Withdraw, Open FanPesa) opens
the FanPesa Mini App directly inside Telegram via Telegram's native
`web_app` buttons — the user never leaves the app. Support opens a
Telegram chat with the FanPesa support line directly. None of this
needs a backend call: Telegram resolves every button client-side.

The reusable **Platform SDK** (`app/platform/`) and its backing
services still exist underneath for capabilities the Telegram bot
doesn't currently surface (wallet balance, promotions, referrals) —
they're ready for a future browser or Safaricom OneApp integration,
or for the bot to use again later, without any redesign. The backend
team has not shipped real APIs yet, so those services still run on a
**mock API layer** behind a clean service boundary.

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

All configuration lives in a single `.env` file at the project root
(gitignored — it holds the real bot token, so it's never committed).
If you don't have one yet, create it with the variables below.

| Variable        | Description                                     | Default                       |
| --------------- | ------------------------------------------------ | ------------------------------ |
| `APP_NAME`      | Application display name                          | `FanPesa Telegram Bot`         |
| `APP_VERSION`   | Application version                               | `1.0.0`                        |
| `ENVIRONMENT`   | `development`, `staging`, or `production`         | `development`                  |
| `DEBUG`         | Enable debug behaviour                            | `True`                         |
| `BOT_TOKEN`     | Telegram bot token — **never commit a real one**  | `CHANGE_ME`                    |
| `WEBHOOK_URL`   | Public URL for webhook mode (leave blank in dev)  | *(empty)*                      |
| `WEBAPP_URL`    | FanPesa Mini App URL opened by the launch button  | `https://www.fanpesa.com`      |
| `REGISTER_URL`  | Mini App page opened by the Register button       | `https://www.fanpesa.com/register` |
| `LOGIN_URL`     | Mini App page opened by the Login button          | `https://www.fanpesa.com/login`    |
| `DEPOSIT_URL`   | Mini App page opened by the Deposit button        | `https://www.fanpesa.com/deposit`  |
| `WITHDRAW_URL`  | Mini App page opened by the Withdraw button       | `https://www.fanpesa.com/withdrawal` |
| `PROMOTION_URL` | Mini App page opened by the Promotion button      | `https://www.fanpesa.com/promotion` |
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
`/about` (available as a slash command; no longer on the menu), and
`/support`. The persistent menu's Register, Login, Deposit, Withdraw,
and Promotion buttons open the Mini App directly and never reach the
bot process at all — see "Telegram bot configuration" below.

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
2. Set `REGISTER_URL`, `LOGIN_URL`, `DEPOSIT_URL`, `WITHDRAW_URL`, and
   `PROMOTION_URL` in `.env` once the real Mini App pages exist — they
   default to `https://www.fanpesa.com/{register,login,deposit,withdrawal,promotion}`.
   No code changes are needed to update them later.
3. `web_app` buttons only work in a private chat with the bot (not in
   groups), and only need to be on an HTTPS domain — no BotFather
   registration is required for these per-message buttons (that's only
   needed for the bot's single global Menu Button, which this project
   doesn't use).
4. Start the bot with `python -m app.bot.application` — polling mode
   requires no public URL.
5. For production, switch to webhook mode: set `WEBHOOK_URL`, call
   `setWebhook` pointing at `{WEBHOOK_URL}/webhooks/telegram`, and stop
   running the polling process (`app/webhooks/telegram.py` already
   implements the receiving endpoint).

### Support

The "🛟 Support" button and `/support` command open a direct Telegram
chat with the FanPesa support line (`app/core/constants.py:
SUPPORT_PHONE_TELEGRAM`) via a `tg://resolve?phone=...` deep link —
this only resolves if that number is registered with a Telegram
account. To change the number, update `SUPPORT_PHONE_DISPLAY` and
`SUPPORT_PHONE_TELEGRAM` in `app/core/constants.py`.

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

## Deploying to Cloudflare (Containers)

`python-telegram-bot` needs a persistent process and isn't Workers/Pyodide
-compatible, so this deploys as a **Cloudflare Container** — the existing
Docker image, run as a long-lived process behind a thin front-end Worker
(`src/worker.js`) — not a Worker rewrite. Webhook mode (not polling) is
required in this setup: `app/main.py`'s `lifespan` already builds, starts,
and registers the bot's webhook automatically whenever `WEBHOOK_URL` and a
real `BOT_TOKEN` are present, so there's no manual `setWebhook` call to run.

### One-time setup

```powershell
npm install
npx wrangler login
```

`wrangler login` opens a browser to authenticate against your Cloudflare
account — this repo has no access to that account, so this step can only
be done by you.

### Configuration

`wrangler.jsonc` already declares every non-secret setting your bot needs
under `"vars"` (`APP_NAME`, `WEBAPP_URL`, `REGISTER_URL`, etc. — the same
values as `.env`), plus the `bot.fanpesa.com` custom-domain route and the
container/Durable-Object bindings. The **one real secret** is the bot
token:

```powershell
npx wrangler secret put BOT_TOKEN
```

Paste your real token when prompted. It's encrypted at rest by Cloudflare
and never appears in `wrangler.jsonc` or git.

> `src/worker.js`'s `FanPesaContainer` constructor explicitly copies both
> `vars` and secrets into the container's process environment
> (`envVars`) — Cloudflare does **not** do this automatically. If you add
> a new setting to `app/config/settings.py` later, add its key to
> `FORWARDED_ENV_KEYS` in `src/worker.js` too, or the container won't see it.

### Custom domain (`bot.fanpesa.com`)

The `routes` entry in `wrangler.jsonc` only works if **`fanpesa.com` is
already an active zone on this Cloudflare account** (nameservers pointed
at Cloudflare, or otherwise onboarded). That step happens in the
Cloudflare dashboard and needs your account access — this repo can't do
it for you. Once the zone exists, `wrangler deploy` provisions the
`bot.fanpesa.com` custom domain and its TLS certificate automatically. If
you'd rather verify the deploy first, delete the `routes` block and
you'll get a free `<name>.<subdomain>.workers.dev` URL instead — add the
custom domain back once the zone is ready.

### Deploy

```powershell
npm run deploy
```

This builds the Docker image, pushes it to Cloudflare's container
registry, and deploys the Worker + container. The first deploy takes a
few minutes; later ones are faster. Check status with:

```powershell
npx wrangler deployments list   # Worker deploy history
npx wrangler containers list    # container instance status
npx wrangler tail               # live logs
```

### Verify

1. `https://bot.fanpesa.com/health` should return the mock-backed health
   check (or the `workers.dev` URL if you haven't wired the domain yet).
2. Message `/start` to [@fanpesa_bot](https://t.me/fanpesa_bot) — updates
   now arrive via webhook instead of polling.
3. `npx wrangler tail` streams the container's logs live if anything
   looks wrong.

### Things worth knowing

- **Don't run polling and webhook mode at once.** Once this is deployed,
  do not also run `python -m app.bot.application` anywhere — Telegram
  delivers updates one way at a time, and the two modes will fight each
  other for them.
- **Cold starts.** `sleepAfter: "10m"` in `src/worker.js` stops the
  container after 10 minutes idle to save cost; the next request pays a
  cold-start cost (typically seconds). Raise it or remove it if instant
  responses matter more than idle cost.
- **Redis isn't wired in yet.** `app/database/database.py` is
  forward-looking scaffolding (see the Overview above) — nothing calls it
  today, so its absence from this deployment isn't a gap. When it's
  needed, use [Upstash Redis](https://developers.cloudflare.com/workers/learning/using-upstash-redis/)
  or a `REDIS_URL` pointed at a Redis instance reachable from the container.
- **This is a young Cloudflare product.** Containers moved to general
  availability recently and its `wrangler.jsonc` schema/CLI can still
  shift. If `wrangler deploy` errors out on something in this file,
  check [Cloudflare's current Containers docs](https://developers.cloudflare.com/containers/)
  before assuming the code is wrong.

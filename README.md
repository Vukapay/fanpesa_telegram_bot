# FanPesa Telegram Bot

Telegram bot for **FanPesa** ([www.fanpesa.com](https://www.fanpesa.com)),
built for [@fanpesa_bot](https://t.me/fanpesa_bot).

Every feature is a direct link opened inside Telegram — Register, Login,
Deposit, Withdraw, Promotion, and Open FanPesa all open the FanPesa Mini
App via Telegram's native `web_app` buttons, and Support opens a direct
Telegram chat with the FanPesa support line. None of this needs a
backend call: Telegram resolves every button entirely client-side, so
the bot itself has no API layer, database, or business logic to
maintain — it's a thin, static menu in front of pages that already
exist on fanpesa.com.

## Overview

- **Telegram bot** (`python-telegram-bot` v22) — `/start`, `/help`,
  `/about`, `/support` commands, plus a persistent menu and inline
  keyboard of direct links. Runs via polling locally, or via webhook
  in production (see "Deploying to Cloudflare" below).
- **FastAPI service** (`app/main.py`) — health/readiness/liveness
  endpoints, and (in production) the Telegram webhook endpoint.

## Project layout

```text
app/
├── bot/            Commands, keyboards, application factory
│   ├── commands/   /start, /help, /about, /support
│   └── keyboards/  Persistent menu + inline keyboard (web_app / tg:// links)
├── config/         Pydantic-settings configuration
├── core/           Constants + structured logging
├── webhooks/       Telegram webhook endpoint (production only)
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

| Variable        | Description                                       | Default                            |
| --------------- | -------------------------------------------------- | ------------------------------------ |
| `APP_NAME`      | Application display name                            | `FanPesa Telegram Bot`               |
| `APP_VERSION`   | Application version                                 | `1.0.0`                              |
| `ENVIRONMENT`   | `development`, `staging`, or `production`           | `development`                        |
| `DEBUG`         | Enable debug behaviour                              | `True`                                |
| `BOT_TOKEN`     | Telegram bot token — **never commit a real one**    | `CHANGE_ME`                          |
| `WEBHOOK_URL`   | Public URL for webhook mode (leave blank in dev)    | *(empty)*                            |
| `WEBAPP_URL`    | FanPesa Mini App URL opened by the launch button    | `https://www.fanpesa.com`            |
| `REGISTER_URL`  | Mini App page opened by the Register button         | `https://www.fanpesa.com/register`   |
| `LOGIN_URL`     | Mini App page opened by the Login button            | `https://www.fanpesa.com/login`      |
| `DEPOSIT_URL`   | Mini App page opened by the Deposit button          | `https://www.fanpesa.com/deposit`    |
| `WITHDRAW_URL`  | Mini App page opened by the Withdraw button         | `https://www.fanpesa.com/withdrawal` |
| `PROMOTION_URL` | Mini App page opened by the Promotion button        | `https://www.fanpesa.com/promotion`  |
| `AVIATOR_URL`   | Mini App page opened by the Aviator button          | `https://www.fanpesa.com/gameLobby/1/9/1138` |
| `AVIATOR_IMAGE_URL` | Promo image sent alongside `/start`'s Aviator callout | *(Aviator artwork URL)*        |
| `SUPPORT_EMAIL` | Email shown by `/support`                           | `support@fanpesa.com`                |
| `SUPPORT_PHONE` | Phone number `/support` opens a Telegram chat with  | `+254 745 275 966`                   |
| `LOG_LEVEL`     | Python logging level                                | `INFO`                               |

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
`http://127.0.0.1:8000/health` for a health check.

### Run the bot

```powershell
python -m app.bot.application
```

The bot runs in polling mode and responds to `/start`, `/help`,
`/about`, and `/support`. The persistent menu's Aviator, Register,
Login, Deposit, Withdraw, and Promotion buttons open the Mini App
directly and never reach the bot process at all.

## Running with Docker

```powershell
docker compose up --build
```

This starts the FastAPI app on port `8000`, loading configuration from
`.env` and mounting the project directory for live-reload during
development. Run the bot separately:

```powershell
docker compose exec app python -m app.bot.application
```

## Telegram bot configuration

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the
   token into `.env` as `BOT_TOKEN`.
2. Set `REGISTER_URL`, `LOGIN_URL`, `DEPOSIT_URL`, `WITHDRAW_URL`,
   `PROMOTION_URL`, and `AVIATOR_URL` in `.env` once the real Mini App
   pages exist — they default to
   `https://www.fanpesa.com/{register,login,deposit,withdrawal,promotion}`
   and the game lobby URL respectively. No code changes are needed to
   update them later.
3. `web_app` buttons only work in a private chat with the bot (not in
   groups), and only need to be on an HTTPS domain — no BotFather
   registration is required for these per-message buttons (that's only
   needed for the bot's single global Menu Button, which this project
   doesn't use).
4. Start the bot with `python -m app.bot.application` — polling mode
   requires no public URL.
5. For production, switch to webhook mode: set `WEBHOOK_URL` — see
   "Deploying to Cloudflare" below, which automates the rest.

### Support

The "🛟 Support" button and `/support` command open a direct Telegram
chat with the FanPesa support line, using `SUPPORT_PHONE` from `.env`,
via a `tg://resolve?phone=...` deep link — this only resolves if that
number is registered with a Telegram account. `settings.support_phone_telegram`
derives the digits-only format the deep link needs automatically, so
`SUPPORT_PHONE` is the only value to update (in the display format,
e.g. `+254 745 275 966`) — no separate digits-only variable to keep in
sync. `SUPPORT_EMAIL` is also read from `.env`.

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
- `tests/commands/` — Telegram command unit tests (`/start`)

## Deployment guidance

- Build and run the production image via the provided `Dockerfile`
  (non-root user, port `8000`, `uvicorn` entrypoint).
- Run the FastAPI process and the Telegram bot process independently —
  they scale differently and a bot crash should never take down the
  health-checked API.
- In production, prefer Telegram **webhook mode** over polling (see
  above) so the bot can run behind the same infrastructure as the API.
- Provide `BOT_TOKEN` and `WEBHOOK_URL` via your deployment platform's
  secret/environment management — never commit real values to `.env`.

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

1. `https://bot.fanpesa.com/health` should return a healthy status (or
   the `workers.dev` URL if you haven't wired the domain yet).
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
- **This is a young Cloudflare product.** Containers moved to general
  availability recently and its `wrangler.jsonc` schema/CLI can still
  shift. If `wrangler deploy` errors out on something in this file,
  check [Cloudflare's current Containers docs](https://developers.cloudflare.com/containers/)
  before assuming the code is wrong.

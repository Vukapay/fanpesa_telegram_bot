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

- **Telegram bot** — the production implementation is the stateless
   JavaScript Worker in `src/worker.js`; the Python implementation in `app/`
   supports local polling and API development.
- **Cloudflare Worker** — receives Telegram webhooks, calls Telegram's HTTPS
   Bot API, and serves health/readiness/liveness endpoints.

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

Local configuration is read from `.env`:

| Variable | Purpose |
| --- | --- |
| `BOT_TOKEN` | Telegram bot token; never commit or expose it |
| `WEBHOOK_URL` | Production webhook base URL; leave empty for polling |
| `WEBAPP_URL`, `REGISTER_URL`, `LOGIN_URL` | Mini App destinations |
| `DEPOSIT_URL`, `WITHDRAW_URL`, `PROMOTION_URL`, `AVIATOR_URL` | Mini App destinations |
| `AVIATOR_IMAGE_URL` | Aviator promotion image |
| `SUPPORT_EMAIL`, `SUPPORT_PHONE` | Support contact details |

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
5. For production, deploy the Worker described below. Do not run the local
   polling process at the same time as the production webhook.

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

## Deploying to Cloudflare Workers

Production runs as a stateless JavaScript Worker in `src/worker.js`.
It handles Telegram webhook updates directly through Telegram's HTTPS Bot
API. The Python/FastAPI application and Docker files are for local use only.

### One-time setup

```powershell
npm install
npx wrangler login
```

`wrangler login` opens a browser to authenticate against your Cloudflare
account — this repo has no access to that account, so this step can only
be done by you.

### Configuration

`wrangler.jsonc` declares the non-secret Worker variables. The bot token is
the one secret:

```powershell
npx wrangler secret put BOT_TOKEN
```

Paste your real token when prompted. It's encrypted at rest by Cloudflare
and never appears in `wrangler.jsonc` or git.

### Worker Builds settings

If deploying through **Cloudflare Worker Builds**, configure the project as
follows:

| Setting | Value |
| --- | --- |
| Repository | `Vukapay/fanpesa_telegram_bot` |
| Branch | `main` |
| Root directory | `/` |
| Build command | Leave blank |
| Deploy command | `npx wrangler deploy` |
| Version command | Leave blank |

The Worker-only deployment must bundle `src/worker.js`. It must not build
`Dockerfile`, install `requirements.txt`, or show `FANPESA_CONTAINER` or
`FanPesaContainer` in the deployment output.

### Custom domain (`bot.playfanpesa.com`)

The `routes` entry in `wrangler.jsonc` only works if **`playfanpesa.com` is
already an active zone on this Cloudflare account** (nameservers pointed
at Cloudflare, or otherwise onboarded). That step happens in the
Cloudflare dashboard and needs your account access — this repo can't do
it for you. Once the zone exists, `wrangler deploy` provisions the
`bot.playfanpesa.com` custom domain and its TLS certificate automatically. If
you'd rather verify the deploy first, delete the `routes` block and
you'll get a free `<name>.<subdomain>.workers.dev` URL instead — add the
custom domain back once the zone is ready.

### Deploy

```powershell
npx wrangler secret put BOT_TOKEN
npm run deploy
```

The first command stores the Telegram token as an encrypted Worker secret.
It does not belong in `wrangler.jsonc`, `.env` committed to Git, or Worker
Build variables. The second command deploys the Worker from the repository
root.

Check deployment status with:

```powershell
npx wrangler deployments list
npx wrangler tail
```

### Verify

1. Visit `https://bot.playfanpesa.com/health` once. It should return:

   ```json
   {"status":"ok","application":"FanPesa Telegram Bot","version":"1.0.0"}
   ```

   The request also registers the Telegram webhook at
   `https://bot.playfanpesa.com/webhooks/telegram`.
2. Message `/start` to [@fanpesa_bot](https://t.me/fanpesa_bot) — updates
   now arrive via webhook instead of polling.
3. `npx wrangler tail` streams the Worker's logs if anything looks wrong.

The Worker deployment is successful when Wrangler reports the
`bot.playfanpesa.com (custom domain)` trigger and does not report a
Container, Durable Object, Docker image, or Python build.

### Troubleshooting deployment failures

If Cloudflare reports:

```text
The build token selected for this build has been deleted or rolled
Unauthorized
```

Open **Workers & Pages > fanpesa-bot > Settings > Builds**, replace the
deleted or rotated build token, save the settings, and start a new build.
The build token is a Cloudflare deployment credential; it is separate from
the Telegram `BOT_TOKEN` secret.

If the logs still show `FANPESA_CONTAINER`, `FanPesaContainer`, Docker, or
`python:3.12-slim`, Cloudflare is using stale remote Worker configuration.
Confirm that Worker Builds points to `main` and uses the settings above.
If the old Container configuration remains attached to the remote Worker,
remove the old Worker and deploy the current repository as a new Worker.

Before retrying, validate locally from the repository root:

```powershell
npm run check
npx wrangler deploy --dry-run
```

The dry run should list only environment-variable bindings and should not
list a Container, Durable Object, or Docker image.

### Things worth knowing

- **Don't run polling and webhook mode at once.** Once this is deployed,
  do not also run `python -m app.bot.application` anywhere — Telegram
  delivers updates one way at a time, and the two modes will fight each
  other for them.

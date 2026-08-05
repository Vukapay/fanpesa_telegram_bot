/**
 * Thin front-end Worker for the FanPesa bot container.
 *
 * This file intentionally has almost no logic: it exists only because
 * Cloudflare Containers are addressed through a Worker + Durable
 * Object. Every real request — health checks, the Telegram webhook,
 * everything — is proxied straight through to the FastAPI app running
 * inside the container on port 8000 (see Dockerfile / app/main.py).
 *
 * IMPORTANT: wrangler.jsonc's "vars" and any `wrangler secret put`
 * values are only visible to this Worker's JS environment by default —
 * they are NOT automatically forwarded into the container's process
 * environment. The constructor below explicitly copies every value
 * the Python app reads via pydantic-settings (see app/config/settings.py)
 * into `envVars`, which IS passed through to the container process.
 * Add any new setting here too, or it won't reach the container.
 */

import { Container, getContainer } from "@cloudflare/containers";

const FORWARDED_ENV_KEYS = [
  "APP_NAME",
  "APP_VERSION",
  "ENVIRONMENT",
  "DEBUG",
  "BOT_TOKEN",
  "WEBHOOK_URL",
  "WEBAPP_URL",
  "REGISTER_URL",
  "LOGIN_URL",
  "DEPOSIT_URL",
  "WITHDRAW_URL",
  "PROMOTION_URL",
  "AVIATOR_URL",
  "AVIATOR_IMAGE_URL",
  "SUPPORT_EMAIL",
  "SUPPORT_PHONE",
  "LOG_LEVEL",
];

export class FanPesaContainer extends Container {
  defaultPort = 8000; // matches the Dockerfile's uvicorn port
  sleepAfter = "10m"; // scales to zero after 10 min idle; see README for tradeoffs

  constructor(ctx, env) {
    super(ctx, env);

    this.envVars = Object.fromEntries(
      FORWARDED_ENV_KEYS.filter((key) => env[key] !== undefined).map((key) => [key, env[key]]),
    );
  }
}

export default {
  async fetch(request, env) {
    // Single shared instance — this bot does not need per-user routing.
    const container = getContainer(env.FANPESA_CONTAINER, "fanpesa");
    return container.fetch(request);
  },
};

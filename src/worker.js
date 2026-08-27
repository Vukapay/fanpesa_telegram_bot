const WEBHOOK_PATH = "/webhooks/telegram";

const defaultConfig = {
  APP_NAME: "FanPesa Telegram Bot",
  APP_VERSION: "1.0.0",
  ENVIRONMENT: "production",
  WEBAPP_URL: "https://www.fanpesa.com",
  REGISTER_URL: "https://www.fanpesa.com/register",
  LOGIN_URL: "https://www.fanpesa.com/login",
  DEPOSIT_URL: "https://www.fanpesa.com/deposit",
  WITHDRAW_URL: "https://www.fanpesa.com/withdrawal",
  PROMOTION_URL: "https://www.fanpesa.com/promotion",
  AVIATOR_URL: "https://www.fanpesa.com/gameLobby/1/9/1138",
  AVIATOR_IMAGE_URL:
    "https://de2.sportal365images.com/process/smp-betway-images/blog.betway.com.en/16042025/b404a83d-33f6-450b-9b1c-486252c35c0a.jpg",
  SUPPORT_EMAIL: "support@fanpesa.com",
  SUPPORT_PHONE: "+254 745 275 966",
};

function config(env, key) {
  return env[key] ?? defaultConfig[key];
}

function webAppButton(text, url) {
  return { text, web_app: { url } };
}

function supportUrl(env) {
  return `tg://resolve?phone=${config(env, "SUPPORT_PHONE").replace(/\D/g, "")}`;
}

function launchKeyboard(env) {
  return {
    inline_keyboard: [
      [webAppButton("🚀 Open FanPesa", config(env, "WEBAPP_URL"))],
      [{ text: "✈️ Play Aviator 🔥", callback_data: "aviator_promo" }],
      [
        webAppButton("📝 Register", config(env, "REGISTER_URL")),
        webAppButton("🔐 Login", config(env, "LOGIN_URL")),
      ],
      [
        webAppButton("💳 Deposit", config(env, "DEPOSIT_URL")),
        webAppButton("💸 Withdraw", config(env, "WITHDRAW_URL")),
      ],
      [{ text: "🛟 Contact Support", url: supportUrl(env) }],
    ],
  };
}

function mainMenu(env) {
  return {
    keyboard: [[{ text: "🛟 Support" }]],
    resize_keyboard: true,
    is_persistent: true,
  };
}

async function telegram(env, method, body) {
  if (!env.BOT_TOKEN) throw new Error("BOT_TOKEN is not configured");

  const response = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) throw new Error(`Telegram ${method} failed with HTTP ${response.status}`);
  return response.json();
}

async function sendMessage(env, chatId, text, extra = {}) {
  return telegram(env, "sendMessage", { chat_id: chatId, text, ...extra });
}

async function registerWebhook(env) {
  if (!env.BOT_TOKEN || !env.WEBHOOK_URL) return;
  const webhookUrl = `${env.WEBHOOK_URL.replace(/\/$/, "")}${WEBHOOK_PATH}`;
  await telegram(env, "setWebhook", { url: webhookUrl });
}

async function handleUpdate(update, env) {
  const message = update.message;
  const callback = update.callback_query;

  if (callback?.data === "aviator_promo") {
    await telegram(env, "answerCallbackQuery", { callback_query_id: callback.id });
    const chatId = callback.message?.chat?.id ?? callback.from?.id;
    if (chatId) {
      await telegram(env, "sendPhoto", {
        chat_id: chatId,
        photo: config(env, "AVIATOR_IMAGE_URL"),
        caption:
          "🔴⚫ *AVIATOR* ⚫🔴\n\n🔥 *Our most popular game!*\n\nWatch the multiplier climb and cash out before the plane flies away. Simple rules, fast rounds, instant payouts.\n\n✈️ Tap below to take off.",
        parse_mode: "Markdown",
        reply_markup: { inline_keyboard: [[webAppButton("✈️ Play Aviator Now 🔥", config(env, "AVIATOR_URL"))]] },
      });
    }
    return;
  }

  if (!message?.chat?.id) return;
  const chatId = message.chat.id;
  const command = (message.text ?? "").split(/\s+/)[0].toLowerCase();

  if (command === "/start") {
    await sendMessage(env, chatId, "🎉 *Welcome to FanPesa!*\n\nThe fastest betting experience inside Telegram.\n\n✅ Register\n✅ Deposit\n✅ Bet\n✅ Win\n✅ Withdraw\n\n👇 Tap below to get started — no need to leave Telegram.", {
      parse_mode: "Markdown",
      reply_markup: launchKeyboard(env),
    });
    await sendMessage(env, chatId, "Use the menu below any time to jump straight to a feature.", {
      reply_markup: mainMenu(env),
    });
  } else if (command === "/help") {
    await sendMessage(env, chatId, "Available Commands\n\n/start — show the welcome message and launch FanPesa\n/help — show this message\n/about — learn more about FanPesa\n/support — message our support team directly on Telegram\n\n✈️ Aviator, 📝 Register, 🔐 Login, 💳 Deposit, 💸 Withdraw, and 🎁 Promotion open the FanPesa Mini App directly from the menu below.");
  } else if (command === "/about") {
    await sendMessage(env, chatId, `ℹ️ *${config(env, "APP_NAME")}*\n\nFast. Secure. Reliable.\n\nFanPesa brings a full betting experience straight into Telegram, backed by the same platform available at https://www.fanpesa.com.`, { parse_mode: "Markdown" });
  } else if (command === "/support" || message.text === "🛟 Support") {
    await sendMessage(env, chatId, `🛟 *Need help?*\n\nTap below to message our support team directly on Telegram.\n\n📞 Phone: ${config(env, "SUPPORT_PHONE")}\n📧 Email: ${config(env, "SUPPORT_EMAIL")}`, {
      parse_mode: "Markdown",
      reply_markup: { inline_keyboard: [[{ text: "🛟 Message Support", url: supportUrl(env) }]] },
    });
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "GET" && ["/", "/health", "/ready", "/live"].includes(url.pathname)) {
      ctx.waitUntil(registerWebhook(env).catch((error) => console.error("Webhook registration failed", error)));
      return Response.json({ status: "ok", application: config(env, "APP_NAME"), version: "1.0.0" });
    }

    if (request.method !== "POST" || ![WEBHOOK_PATH, "/webhook", "/telegram/webhook"].includes(url.pathname)) {
      return new Response("Not found", { status: 404 });
    }

    if (!env.BOT_TOKEN) return Response.json({ error: "BOT_TOKEN is not configured" }, { status: 503 });

    try {
      const update = await request.json();
      await handleUpdate(update, env);
      return Response.json({ ok: true });
    } catch (error) {
      console.error("Telegram update processing failed", error);
      return Response.json({ error: "Unable to process update" }, { status: 500 });
    }
  },
};

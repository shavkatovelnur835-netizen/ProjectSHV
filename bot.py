async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if (
        "who created you" in user_message
        or "who is your founder" in user_message
        or "who made you" in user_message
        or "founder" in user_message
        or "elnur" in user_message
    ):
        await update.message.reply_text(
            "ProjectSHV AI was created and developed by Elnur Shavkatov."
        )
        return

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ProjectSHV AI, an AI-powered Telegram assistant. "
                        "Maintain a professional and intelligent tone."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        reply = completion.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your AI bot powered by OpenRouter."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ],
        )

        reply = completion.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()

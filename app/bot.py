import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

FASTAPI_URL = "http://localhost:8000/ask"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ Thinking...")
    
    response = httpx.post(FASTAPI_URL, json={"text": user_text}, timeout=60)
    answer = response.json()["answer"]
    
    await update.message.reply_text(answer)

def run_bot(token: str):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    print("Bot is running...")
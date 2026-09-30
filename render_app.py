import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, InlineKeyboardButton, InlineKeyboardMarkup

# ============ ВАШИ НАСТРОЙКИ ============
BOT_TOKEN = "8603010595:AAF3Ct7EgGLMS4sJOQsZdsgPEA2zg9Mk13Y"
CHANNEL_ID = -1004296873580
CHANNEL_USERNAME = "probye_bot"
GIFT_LINK = "https://t.me/probye_bot"
# ========================================

# --- Простой веб-сервер для Render (без Flask) ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass  # отключаем лишние логи

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# --- Логика бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, int(user_id))
        is_subscribed = member.status in ["member", "administrator", "creator"]
    except Exception:
        is_subscribed = False
    
    if is_subscribed:
        await update.message.reply_text(f"🎉 {user.first_name}, ваш подарок: {GIFT_LINK}")
    else:
        keyboard = [[InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton("✅ Проверить", callback_data="check_sub")]]
        await update.message.reply_text(f"👋 {user.first_name}, подпишитесь на канал!", reply_markup=InlineKeyboardMarkup(keyboard))

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, int(user_id))
        is_subscribed = member.status in ["member", "administrator", "creator"]
    except Exception:
        is_subscribed = False
    
    if is_subscribed:
        await query.edit_message_text(f"🎉 {query.from_user.first_name}, ваш подарок: {GIFT_LINK}")
    else:
        keyboard = [[InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton("✅ Проверить снова", callback_data="check_sub")]]
        await query.edit_message_text("❌ Вы ещё не подписаны.", reply_markup=InlineKeyboardMarkup(keyboard))

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check_sub"))
    application.run_polling()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    run_web()
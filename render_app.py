import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, InlineKeyboardButton, InlineKeyboardMarkup

# ============ ВАШИ НАСТРОЙКИ ============
BOT_TOKEN = "8603010595:AAF3Ct7EgGLMS4sJOQsZdsgPEA2zg9Mk13Y"
CHANNEL_ID = -1004296873580  
CHANNEL_USERNAME = "probye_bot" 
GIFT_LINK = "https://t.me/probye_bot"
# ========================================

# --- Создаём Flask приложение для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK"

# --- Логика бота (упрощённая) ---
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
    # Упрощённая проверка (в реальности нужно проверить подписку снова)
    await query.edit_message_text(f"Ваш подарок: {GIFT_LINK}")

def run_bot():
    """Функция запуска бота в фоне"""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check_sub"))
    application.run_polling()

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask сервер (Render будет проверять его)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
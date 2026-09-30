import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКИ (ЗАМЕНИТЕ ЭТО!) ====================
BOT_TOKEN = "8603010595:AAF3Ct7EgGLMS4sJOQsZdsgPEA2zg9Mk13Y"        
CHANNEL_ID = -1004296873580                 
CHANNEL_USERNAME = "probye_bot"              
GIFT_LINK = "https://disk.yandex.ru/i/WvA_ACC0cti7_w"  
# ===================================================================

USED_USERS_FILE = "used_users.txt"

def load_used_users():
    if os.path.exists(USED_USERS_FILE):
        with open(USED_USERS_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_used_user(user_id):
    with open(USED_USERS_FILE, "a", encoding="utf-8") as f:
        f.write(str(user_id) + "\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    first_name = user.first_name or "друг"
    
    if user_id in load_used_users():
        await update.message.reply_text(
            f"😊 {first_name}, вы уже получили подарок!\n\n"
            f"📥 Ссылка: {GIFT_LINK}\n"
            f"Если не открывается — напишите @ваш_ник"
        )
        return
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, int(user_id))
        is_subscribed = member.status in ["member", "administrator", "creator"]
    except:
        is_subscribed = False
    
    if is_subscribed:
        save_used_user(user_id)
        await update.message.reply_text(
            f"🎉 {first_name}, ваш подарок!\n\n"
            f"📥 Скачать: {GIFT_LINK}\n\n"
            f"Спасибо, что вы с нами! ❤️"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ Проверить", callback_data="check_sub")]
        ]
        await update.message.reply_text(
            f"👋 {first_name}, подпишитесь на канал и нажмите 'Проверить'.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_id = str(user.id)
    first_name = user.first_name or "друг"
    
    if user_id in load_used_users():
        await query.edit_message_text(f"😊 {first_name}, вы уже получили подарок! Ссылка: {GIFT_LINK}")
        return
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, int(user_id))
        is_subscribed = member.status in ["member", "administrator", "creator"]
    except:
        is_subscribed = False
    
    if is_subscribed:
        save_used_user(user_id)
        await query.edit_message_text(
            f"🎉 {first_name}, ваш подарок!\n\n"
            f"📥 Скачать: {GIFT_LINK}\n\n"
            f"Спасибо, что вы с нами! ❤️"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ Проверить снова", callback_data="check_sub")]
        ]
        await query.edit_message_text(
            f"❌ {first_name}, вы не подписаны. Подпишитесь и нажмите 'Проверить снова'.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    print("🤖 Бот запускается...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_sub"))
    print("✅ Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
"""
YHQ Test Bot - Yo'l harakati qoidalari test boti
Muallif: YHQ Team
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

from database.db_manager import Database
from handlers import user_handlers, admin_handlers
from handlers.admin_handlers import (
    ADDING_QUESTION, 
    ADDING_OPTIONS, 
    ADDING_ANSWER, 
    ADDING_CATEGORY
)

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables yuklash
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/bot_data.json')

# Database ob'ekti
db = Database(DATABASE_PATH)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komandasi"""
    await user_handlers.start_command(update, context, db)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel"""
    await admin_handlers.admin_panel(update, context, db, ADMIN_ID)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarlarni qayta ishlash"""
    user_id = update.effective_user.id
    device_id = str(user_id)
    text = update.message.text
    
    # Foydalanuvchi ruxsat etilganligini tekshirish
    if not db.is_user_authorized(user_id, device_id):
        await update.message.reply_text(
            "⛔ Siz botdan foydalana olmaysiz.\n"
            "/start buyrug'ini bosing va ruxsat so'rang."
        )
        return
    
    # Matn buyruqlarini qayta ishlash
    if text == "📝 Testni boshlash":
        await user_handlers.start_test(update, context, db)
    
    elif text == "📊 Statistika":
        await user_handlers.show_statistics(update, context, db)
    
    elif text == "👤 Profil":
        await user_handlers.show_profile(update, context, db)
    
    elif text == "ℹ️ Qo'llanma":
        await user_handlers.show_help(update, context)
    
    elif text == "👥 Foydalanuvchilar" and user_id == ADMIN_ID:
        await admin_handlers.manage_users(update, context, db, ADMIN_ID)
    
    elif text == "❓ Savollar" and user_id == ADMIN_ID:
        await admin_handlers.manage_questions(update, context, db, ADMIN_ID)
    
    elif text == "📊 Statistika" and user_id == ADMIN_ID:
        await admin_handlers.show_statistics(update, context, db, ADMIN_ID)
    
    elif text == "🔙 Asosiy menyu":
        await start(update, context)
    
    else:
        await update.message.reply_text(
            "❓ Noma'lum buyruq.\n"
            "Iltimos, menyudan tanlang yoki /start buyrug'ini kiriting."
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback query'larni qayta ishlash"""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    # Foydalanuvchi uchun callback'lar
    if data == "request_access":
        await user_handlers.request_access(update, context, db, ADMIN_ID)
    
    elif data.startswith("answer_"):
        await user_handlers.handle_answer(update, context, db)
    
    elif data == "next_question":
        await user_handlers.next_question(update, context, db)
    
    elif data == "stop_test":
        await user_handlers.stop_test(update, context, db)
    
    elif data == "finish_test":
        await user_handlers.finish_test(update, context, db)
    
    elif data == "restart_test":
        db.reset_user_progress(user_id)
        await user_handlers.next_question(update, context, db)
    
    elif data == "reset_stats":
        db.reset_user_progress(user_id)
        await query.edit_message_text("✅ Statistika tozalandi!")
    
    elif data == "test_database":
        await query.answer("Ushbu funksiya keyinroq qo'shiladi", show_alert=True)
    
    # Admin uchun callback'lar
    elif data.startswith("approve_") and user_id == ADMIN_ID:
        await admin_handlers.approve_user(update, context, db, ADMIN_ID)
    
    elif data.startswith("reject_") and user_id == ADMIN_ID:
        await admin_handlers.reject_user(update, context, ADMIN_ID)
    
    elif data.startswith("user_info_") and user_id == ADMIN_ID:
        await admin_handlers.user_info(update, context, db, ADMIN_ID)
    
    elif data.startswith("deactivate_user_") and user_id == ADMIN_ID:
        await admin_handlers.deactivate_user(update, context, db, ADMIN_ID)
    
    elif data.startswith("activate_user_") and user_id == ADMIN_ID:
        await admin_handlers.activate_user(update, context, db, ADMIN_ID)
    
    elif data.startswith("delete_user_") and user_id == ADMIN_ID:
        await admin_handlers.delete_user(update, context, db, ADMIN_ID)
    
    elif data.startswith("confirm_delete_") and not data.startswith("confirm_delete_q_") and user_id == ADMIN_ID:
        await admin_handlers.confirm_delete_user(update, context, db, ADMIN_ID)
    
    elif data == "list_questions" and user_id == ADMIN_ID:
        await admin_handlers.list_questions(update, context, db, ADMIN_ID)
    
    elif data.startswith("question_info_") and user_id == ADMIN_ID:
        await admin_handlers.question_info(update, context, db, ADMIN_ID)
    
    elif data.startswith("delete_question_") and user_id == ADMIN_ID:
        await admin_handlers.delete_question(update, context, db, ADMIN_ID)
    
    elif data.startswith("confirm_delete_q_") and user_id == ADMIN_ID:
        await admin_handlers.confirm_delete_question(update, context, db, ADMIN_ID)
    
    elif data == "add_question_start" and user_id == ADMIN_ID:
        # ConversationHandler will handle this
        pass
    
    elif data == "upload_questions_file" and user_id == ADMIN_ID:
        await admin_handlers.upload_questions_file_start(update, context)
    
    elif data == "confirm_file_upload" and user_id == ADMIN_ID:
        await admin_handlers.confirm_file_upload(update, context, db)
    
    elif data == "cancel_file_upload" and user_id == ADMIN_ID:
        await admin_handlers.cancel_file_upload(update, context)
    
    else:
        await query.answer("⚠️ Noma'lum buyruq!")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatolarni qayta ishlash"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
        )


def main():
    """Botni ishga tushirish"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return
    
    if ADMIN_ID == 0:
        logger.error("ADMIN_ID topilmadi! .env faylini tekshiring.")
        return
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ConversationHandler for adding questions
    add_question_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                admin_handlers.add_question_start, 
                pattern="^add_question_start$"
            )
        ],
        states={
            ADDING_QUESTION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, 
                    admin_handlers.receive_question_text
                ),
                MessageHandler(
                    filters.Document.ALL,
                    lambda update, context: admin_handlers.receive_questions_file(update, context, db)
                )
            ],
            ADDING_OPTIONS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, 
                    admin_handlers.receive_question_options
                )
            ],
            ADDING_ANSWER: [
                CallbackQueryHandler(admin_handlers.receive_correct_answer)
            ],
            ADDING_CATEGORY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    lambda update, context: admin_handlers.receive_question_category(update, context, db)
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", admin_handlers.cancel_question_adding)
        ],
    )
    
    # Add ConversationHandler
    application.add_handler(add_question_conv)
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Callback handler
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushmoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

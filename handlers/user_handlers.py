"""
User handlers for YHQ Test Bot
Foydalanuvchilar uchun handlerlar
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_manager import Database
from utils.helpers import format_question, format_statistics
import random


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Start komandasi - botni boshlash"""
    user = update.effective_user
    user_id = user.id
    device_id = str(user_id)  # Telegram user_id ni device_id sifatida ishlatamiz
    
    # Foydalanuvchi ruxsat etilganligini tekshirish
    if db.is_user_authorized(user_id, device_id):
        # Asosiy menyu
        keyboard = [
            ["📝 Testni boshlash", "📊 Statistika"],
            ["ℹ️ Qo'llanma", "👤 Profil"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Assalomu alaykum, {user.first_name}! 👋\n\n"
            "Yo'l harakati qoidalari bo'yicha test botiga xush kelibsiz!\n\n"
            "Quyidagi tugmalardan birini tanlang:",
            reply_markup=reply_markup
        )
    else:
        # Foydalanuvchi ro'yxatdan o'tmagan
        keyboard = [[InlineKeyboardButton("📝 Ro'yxatdan o'tish so'rovi yuborish", callback_data="request_access")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Assalomu alaykum, {user.first_name}! 👋\n\n"
            f"Sizning Telegram ID: <code>{user_id}</code>\n"
            f"Qurilma ID: <code>{device_id}</code>\n\n"
            "⚠️ Siz hali ro'yxatdan o'tmagansiz.\n\n"
            "Botdan foydalanish uchun admin ruxsatini so'rang.",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )


async def request_access(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Ruxsat so'rash"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_id = user.id
    device_id = str(user_id)
    
    # Adminга xabar yuborish
    admin_message = (
        f"🔔 <b>Yangi ruxsat so'rovi</b>\n\n"
        f"👤 Ism: {user.first_name} {user.last_name or ''}\n"
        f"🆔 User ID: <code>{user_id}</code>\n"
        f"📱 Device ID: <code>{device_id}</code>\n"
        f"👨‍💼 Username: @{user.username or 'Mavjud emas'}\n\n"
        f"Foydalanuvchiga ruxsat berasizmi?"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Ruxsat berish", callback_data=f"approve_{user_id}_{device_id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_message(
            chat_id=admin_id,
            text=admin_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        await query.edit_message_text(
            "✅ So'rovingiz adminga yuborildi.\n"
            "Tez orada javob beriladi. Iltimos, kuting..."
        )
    except Exception as e:
        await query.edit_message_text(
            f"❌ Xatolik yuz berdi: {str(e)}\n"
            "Iltimos, keyinroq qayta urinib ko'ring."
        )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Testni boshlash"""
    user_id = update.effective_user.id
    
    # Savollar mavjudligini tekshirish
    questions_count = db.get_questions_count()
    if questions_count == 0:
        await update.message.reply_text(
            "❌ Hozircha savollar mavjud emas.\n"
            "Admin savollar qo'shgandan keyin test topshirishingiz mumkin."
        )
        return
    
    # Progressni boshlash yoki qayta boshlash
    db.reset_user_progress(user_id)
    db.init_user_progress(user_id)
    
    # Tasodifiy savol tanlash
    all_questions = db.get_all_questions()
    question = random.choice(all_questions)
    
    # Progress ma'lumoti
    progress = db.get_user_progress(user_id)
    total_answered = len(progress.get('answered_questions', []))
    
    # Savolni formatlash (rasmga o'xshash)
    question_text = f"📊 <b>Savol {total_answered + 1}/{questions_count}</b>\n\n"
    question_text += f"{question['question']}\n\n"
    
    for key, value in question['options'].items():
        question_text += f"<b>{key})</b> {value}\n\n"
    
    # Variantlar uchun tugmalar (bir qatorda)
    keyboard = []
    row = []
    for key in sorted(question['options'].keys()):
        row.append(InlineKeyboardButton(key, callback_data=f"answer_{question['id']}_{key}"))
    keyboard.append(row)
    
    # Qo'shimcha tugmalar
    keyboard.append([InlineKeyboardButton("📋 Katta testlar bazasi", callback_data="test_database")])
    keyboard.append([InlineKeyboardButton("🚫 Testni to'xtatish", callback_data="stop_test")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        question_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Javobni tekshirish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Callback data'dan ma'lumotlarni olish
    data_parts = query.data.split('_')
    question_id = int(data_parts[1])
    user_answer = data_parts[2]
    
    # Savolni olish
    question = db.get_question(question_id)
    if not question:
        await query.edit_message_text("❌ Savol topilmadi.")
        return
    
    # Javobni tekshirish
    is_correct = (user_answer == question['correct_answer'])
    
    # Progressni yangilash
    db.update_user_progress(user_id, is_correct, question_id)
    
    # Statistika
    stats = db.get_user_statistics(user_id)
    
    # Natijani ko'rsatish (rasmga o'xshash)
    if is_correct:
        result_text = "✅ <b>To'g'ri!</b>\n\n"
    else:
        result_text = f"❌ <b>Noto'g'ri!</b>\n\n"
        result_text += f"<b>To'g'ri javob:</b> {question['correct_answer']}) {question['options'][question['correct_answer']]}\n\n"
    
    # Progress ko'rsatkichi
    result_text += f"━━━━━━━━━━━━━━━\n"
    result_text += f"📊 <b>Natija:</b> ✅ {stats['correct']} | ❌ {stats['wrong']}\n"
    result_text += f"🎯 <b>To'g'ri javoblar:</b> {stats['percentage']}%"
    
    # Keyingi savol tugmasi
    keyboard = [
        [InlineKeyboardButton("▶️ Keyingi savol", callback_data="next_question")],
        [InlineKeyboardButton("🏁 Testni yakunlash", callback_data="finish_test")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        result_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Keyingi savolga o'tish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Barcha savollar
    all_questions = db.get_all_questions()
    questions_count = len(all_questions)
    progress = db.get_user_progress(user_id)
    
    # Javob berilmagan savollarni topish
    answered = set(progress.get('answered_questions', []))
    unanswered = [q for q in all_questions if q['id'] not in answered]
    
    if not unanswered:
        # Barcha savollarga javob berilgan
        stats = db.get_user_statistics(user_id)
        result_text = (
            f"🎉 <b>Tabriklaymiz! Barcha savollarga javob berdingiz!</b>\n\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 <b>YAKUNIY NATIJA</b>\n\n"
            f"✅ To'g'ri javoblar: {stats['correct']}\n"
            f"❌ Noto'g'ri javoblar: {stats['wrong']}\n"
            f"📝 Jami savollar: {stats['total']}\n\n"
            f"🎯 <b>Natija: {stats['percentage']}%</b>\n"
            f"━━━━━━━━━━━━━━━\n\n"
        )
        
        # Baho
        if stats['percentage'] >= 90:
            result_text += "🏆 <b>A'lo!</b> Siz ajoyib natija ko'rsatdingiz!"
        elif stats['percentage'] >= 70:
            result_text += "👍 <b>Yaxshi!</b> Davom eting!"
        elif stats['percentage'] >= 50:
            result_text += "📚 <b>Qoniqarli.</b> Ko'proq mashq qiling!"
        else:
            result_text += "💪 <b>Harakat qiling!</b> Siz albatta uddalaysiz!"
        
        keyboard = [[InlineKeyboardButton("🔄 Qaytadan boshlash", callback_data="restart_test")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            result_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    # Tasodifiy savol tanlash
    question = random.choice(unanswered)
    total_answered = len(answered)
    
    # Savolni formatlash (rasmga o'xshash)
    question_text = f"📊 <b>Savol {total_answered + 1}/{questions_count}</b>\n\n"
    question_text += f"{question['question']}\n\n"
    
    for key, value in question['options'].items():
        question_text += f"<b>{key})</b> {value}\n\n"
    
    # Variantlar uchun tugmalar (bir qatorda)
    keyboard = []
    row = []
    for key in sorted(question['options'].keys()):
        row.append(InlineKeyboardButton(key, callback_data=f"answer_{question['id']}_{key}"))
    keyboard.append(row)
    
    # Qo'shimcha tugmalar
    keyboard.append([InlineKeyboardButton("📋 Katta testlar bazasi", callback_data="test_database")])
    keyboard.append([InlineKeyboardButton("🚫 Testni to'xtatish", callback_data="stop_test")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        question_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Statistikani ko'rsatish"""
    user_id = update.effective_user.id
    stats = db.get_user_statistics(user_id)
    
    stats_text = format_statistics(stats)
    
    keyboard = [[InlineKeyboardButton("🔄 Statistikani tozalash", callback_data="reset_stats")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        stats_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Profilni ko'rsatish"""
    user = update.effective_user
    user_id = user.id
    
    user_data = db.get_user(user_id)
    if not user_data:
        await update.message.reply_text("❌ Foydalanuvchi ma'lumotlari topilmadi.")
        return
    
    stats = db.get_user_statistics(user_id)
    
    profile_text = (
        f"👤 <b>Profil ma'lumotlari</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"👨‍💼 Ism: {user.first_name} {user.last_name or ''}\n"
        f"📱 Username: @{user.username or 'Mavjud emas'}\n"
        f"📅 Ro'yxatdan o'tgan: {user_data['registered_at'][:10]}\n\n"
        f"📊 <b>Statistika:</b>\n"
        f"✅ To'g'ri: {stats['correct']}\n"
        f"❌ Noto'g'ri: {stats['wrong']}\n"
        f"🎯 Natija: {stats['percentage']}%"
    )
    
    await update.message.reply_text(profile_text, parse_mode='HTML')


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Qo'llanma"""
    help_text = (
        "📖 <b>Qo'llanma</b>\n\n"
        "<b>Asosiy funksiyalar:</b>\n\n"
        "📝 <b>Testni boshlash</b> - Yo'l harakati qoidalari bo'yicha test topshirish\n\n"
        "📊 <b>Statistika</b> - O'z natijalaringizni ko'rish\n\n"
        "👤 <b>Profil</b> - Shaxsiy ma'lumotlaringizni ko'rish\n\n"
        "ℹ️ <b>Qo'llanma</b> - Botdan foydalanish bo'yicha ko'rsatmalar\n\n"
        "<b>Qanday ishlaydi?</b>\n"
        "1. 'Testni boshlash' tugmasini bosing\n"
        "2. Savolga javob variantlaridan birini tanlang\n"
        "3. Natijangizni ko'ring va keyingi savolga o'ting\n"
        "4. Statistikangizni kuzatib boring\n\n"
        "Omad! 🚗💨"
    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')


async def stop_test(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Testni to'xtatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    stats = db.get_user_statistics(user_id)
    
    result_text = (
        f"🛑 <b>Test to'xtatildi</b>\n\n"
        f"📊 <b>Joriy natija:</b>\n"
        f"✅ To'g'ri: {stats['correct']}\n"
        f"❌ Noto'g'ri: {stats['wrong']}\n"
        f"🎯 Natija: {stats['percentage']}%"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 Qaytadan boshlash", callback_data="restart_test")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        result_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Testni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    stats = db.get_user_statistics(user_id)
    
    result_text = (
        f"🏁 <b>Test yakunlandi!</b>\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📊 <b>YAKUNIY NATIJA</b>\n\n"
        f"✅ To'g'ri javoblar: {stats['correct']}\n"
        f"❌ Noto'g'ri javoblar: {stats['wrong']}\n"
        f"📝 Jami savollar: {stats['total']}\n\n"
        f"🎯 <b>Natija: {stats['percentage']}%</b>\n"
        f"━━━━━━━━━━━━━━━\n\n"
    )
    
    if stats['percentage'] >= 90:
        result_text += "🏆 <b>A'lo!</b> Siz ajoyib natija ko'rsatdingiz!"
    elif stats['percentage'] >= 70:
        result_text += "👍 <b>Yaxshi!</b> Davom eting!"
    elif stats['percentage'] >= 50:
        result_text += "📚 <b>Qoniqarli.</b> Ko'proq mashq qiling!"
    else:
        result_text += "💪 <b>Harakat qiling!</b> Siz albatta uddalaysiz!"
    
    keyboard = [[InlineKeyboardButton("🔄 Qaytadan boshlash", callback_data="restart_test")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        result_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def test_database_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Katta testlar bazasi haqida ma'lumot"""
    query = update.callback_query
    await query.answer("Ushbu funksiya keyinroq qo'shiladi", show_alert=True)

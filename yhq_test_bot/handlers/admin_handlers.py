"""
Admin handlers for YHQ Test Bot
Admin uchun handlerlar
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database.db_manager import Database
from utils.helpers import format_question, format_user_info, validate_question_data


# Conversation states
ADDING_QUESTION, ADDING_OPTIONS, ADDING_ANSWER, ADDING_CATEGORY = range(4)


def is_admin(user_id: int, admin_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return user_id == admin_id


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Admin panel"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id, admin_id):
        await update.message.reply_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    keyboard = [
        ["👥 Foydalanuvchilar", "❓ Savollar"],
        ["📊 Statistika", "⚙️ Sozlamalar"],
        ["🔙 Asosiy menyu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    total_users = len(db.get_all_users())
    total_questions = db.get_questions_count()
    
    admin_text = (
        f"🔐 <b>Admin Panel</b>\n\n"
        f"👥 Foydalanuvchilar: {total_users}\n"
        f"❓ Savollar: {total_questions}\n\n"
        f"Quyidagi bo'limlardan birini tanlang:"
    )
    
    await update.message.reply_text(
        admin_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def manage_users(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchilarni boshqarish"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id, admin_id):
        await update.message.reply_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("📝 Hozircha foydalanuvchilar yo'q.")
        return
    
    keyboard = []
    for user in users[:10]:  # Birinchi 10 ta foydalanuvchi
        status = "✅" if user.get('is_active', False) else "❌"
        keyboard.append([
            InlineKeyboardButton(
                f"{status} {user.get('name', 'N/A')} (ID: {user.get('user_id')})",
                callback_data=f"user_info_{user.get('user_id')}"
            )
        ])
    
    if len(users) > 10:
        keyboard.append([InlineKeyboardButton(f"... va yana {len(users) - 10} ta", callback_data="show_more_users")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👥 <b>Foydalanuvchilar ro'yxati</b>\n\n"
        f"Jami: {len(users)} ta\n\n"
        f"Batafsil ma'lumot olish uchun foydalanuvchini tanlang:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchi haqida ma'lumot"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[2])
    user = db.get_user(user_id)
    
    if not user:
        await query.edit_message_text("❌ Foydalanuvchi topilmadi.")
        return
    
    user['user_id'] = user_id
    user_text = format_user_info(user)
    
    # Statistika
    stats = db.get_user_statistics(user_id)
    user_text += f"\n\n📊 <b>Statistika:</b>\n"
    user_text += f"✅ To'g'ri: {stats['correct']}\n"
    user_text += f"❌ Noto'g'ri: {stats['wrong']}\n"
    user_text += f"🎯 Natija: {stats['percentage']}%"
    
    # Tugmalar
    keyboard = []
    if user.get('is_active', False):
        keyboard.append([InlineKeyboardButton("🚫 O'chirish", callback_data=f"deactivate_user_{user_id}")])
    else:
        keyboard.append([InlineKeyboardButton("✅ Faollashtirish", callback_data=f"activate_user_{user_id}")])
    
    keyboard.append([InlineKeyboardButton("🗑 Butunlay o'chirish", callback_data=f"delete_user_{user_id}")])
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_users")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        user_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchiga ruxsat berish"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    data_parts = query.data.split('_')
    user_id = int(data_parts[1])
    device_id = data_parts[2]
    
    # Foydalanuvchi ma'lumotlarini olish
    try:
        user = await context.bot.get_chat(user_id)
        name = f"{user.first_name} {user.last_name or ''}".strip()
    except:
        name = "Unknown"
    
    # Foydalanuvchini qo'shish
    if db.add_user(user_id, device_id, name):
        await query.edit_message_text(
            f"✅ Foydalanuvchi ruxsat etildi!\n\n"
            f"👤 {name}\n"
            f"🆔 ID: {user_id}"
        )
        
        # Foydalanuvchiga xabar yuborish
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="✅ Sizga ruxsat berildi!\n\n"
                     "Endi botdan foydalanishingiz mumkin.\n"
                     "/start buyrug'ini bosing."
            )
        except:
            pass
    else:
        await query.edit_message_text("❌ Foydalanuvchi allaqachon mavjud.")


async def reject_user(update: Update, context: ContextTypes.DEFAULT_TYPE, admin_id: int):
    """Foydalanuvchini rad etish"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[1])
    
    await query.edit_message_text(
        f"❌ So'rov rad etildi!\n\n"
        f"🆔 User ID: {user_id}"
    )
    
    # Foydalanuvchiga xabar yuborish
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Afsus, sizga ruxsat berilmadi.\n\n"
                 "Agar bu xato deb hisoblasangiz, admin bilan bog'laning."
        )
    except:
        pass


async def deactivate_user(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchini o'chirish (deaktivatsiya)"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[2])
    
    if db.deactivate_user(user_id):
        await query.edit_message_text("✅ Foydalanuvchi o'chirildi (deaktivatsiya).")
        
        # Foydalanuvchiga xabar
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="⚠️ Sizning hisobingiz admin tomonidan o'chirildi.\n\n"
                     "Botdan foydalana olmaysiz."
            )
        except:
            pass
    else:
        await query.edit_message_text("❌ Xatolik yuz berdi.")


async def activate_user(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchini faollashtirish"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[2])
    
    if db.activate_user(user_id):
        await query.edit_message_text("✅ Foydalanuvchi faollashtirildi.")
        
        # Foydalanuvchiga xabar
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="✅ Sizning hisobingiz qayta faollashtirildi!\n\n"
                     "Endi botdan foydalanishingiz mumkin.\n"
                     "/start buyrug'ini bosing."
            )
        except:
            pass
    else:
        await query.edit_message_text("❌ Xatolik yuz berdi.")


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchini butunlay o'chirish"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[2])
    
    # Tasdiqlash
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"confirm_delete_{user_id}"),
            InlineKeyboardButton("❌ Yo'q", callback_data=f"user_info_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚠️ <b>Diqqat!</b>\n\n"
        "Foydalanuvchini butunlay o'chirmoqchimisiz?\n"
        "Bu amal barcha ma'lumotlarni o'chiradi va qaytarib bo'lmaydi!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def confirm_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Foydalanuvchini o'chirishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    user_id = int(query.data.split('_')[2])
    
    if db.remove_user(user_id):
        await query.edit_message_text("✅ Foydalanuvchi butunlay o'chirildi.")
    else:
        await query.edit_message_text("❌ Xatolik yuz berdi.")


async def manage_questions(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Savollarni boshqarish"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id, admin_id):
        await update.message.reply_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    questions_count = db.get_questions_count()
    
    keyboard = [
        [InlineKeyboardButton("➕ Bitta savol qo'shish", callback_data="add_question_start")],
        [InlineKeyboardButton("📁 Fayldan yuklash", callback_data="upload_questions_file")],
        [InlineKeyboardButton("📝 Savollar ro'yxati", callback_data="list_questions")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"❓ <b>Savollar boshqaruvi</b>\n\n"
        f"Jami savollar: {questions_count}\n\n"
        f"Amallardan birini tanlang:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def add_question_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Savol qo'shishni boshlash"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📝 <b>Yangi savol qo'shish</b>\n\n"
        "Savol matnini yuboring:\n\n"
        "Misol: O'zbekiston Respublikasi yo'llarida qanday harakat tartibi belgilangan?\n\n"
        "Bekor qilish uchun /cancel buyrug'ini yuboring.",
        parse_mode='HTML'
    )
    
    return ADDING_QUESTION


async def receive_question_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Savol matnini qabul qilish"""
    question_text = update.message.text
    
    if len(question_text) < 10:
        await update.message.reply_text(
            "❌ Savol juda qisqa! Kamida 10 ta belgi kiriting.\n"
            "Qaytadan kiriting yoki /cancel buyrug'ini yuboring."
        )
        return ADDING_QUESTION
    
    # Contextga saqlash
    context.user_data['new_question'] = {
        'question': question_text,
        'options': {}
    }
    
    await update.message.reply_text(
        "✅ Savol saqlandi!\n\n"
        "📋 <b>Endi variantlarni kiriting:</b>\n\n"
        "Quyidagi formatda yuboring:\n"
        "A) Variant 1\n"
        "B) Variant 2\n"
        "C) Variant 3\n"
        "D) Variant 4\n\n"
        "Misol:\n"
        "A) Chap tomonlama harakat\n"
        "B) O'ng tomonlama harakat\n"
        "C) Ikki tomonlama harakat\n"
        "D) Erkin harakat\n\n"
        "Bekor qilish uchun /cancel",
        parse_mode='HTML'
    )
    
    return ADDING_OPTIONS


async def receive_question_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Variantlarni qabul qilish"""
    options_text = update.message.text
    
    # Variantlarni parse qilish
    options = {}
    lines = options_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # A) Variant formatida parse qilish
        if ')' in line:
            parts = line.split(')', 1)
            if len(parts) == 2:
                key = parts[0].strip().upper()
                value = parts[1].strip()
                if key in ['A', 'B', 'C', 'D']:
                    options[key] = value
    
    if len(options) < 2:
        await update.message.reply_text(
            "❌ Kamida 2 ta variant kiriting!\n\n"
            "Format:\n"
            "A) Variant 1\n"
            "B) Variant 2\n\n"
            "Qaytadan kiriting yoki /cancel"
        )
        return ADDING_OPTIONS
    
    # Contextga saqlash
    context.user_data['new_question']['options'] = options
    
    # Variantlarni ko'rsatish
    variants_text = "\n".join([f"{k}) {v}" for k, v in options.items()])
    
    # To'g'ri javob uchun tugmalar
    keyboard = []
    row = []
    for key in sorted(options.keys()):
        row.append(InlineKeyboardButton(key, callback_data=f"correct_{key}"))
    keyboard.append(row)
    keyboard.append([InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_question")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ Variantlar saqlandi!\n\n"
        f"<b>Variantlar:</b>\n{variants_text}\n\n"
        f"<b>To'g'ri javobni tanlang:</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    return ADDING_ANSWER


async def receive_correct_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To'g'ri javobni qabul qilish"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel_question":
        await query.edit_message_text("❌ Savol qo'shish bekor qilindi.")
        context.user_data.clear()
        return ConversationHandler.END
    
    correct_answer = query.data.split('_')[1]
    context.user_data['new_question']['correct_answer'] = correct_answer
    
    await query.edit_message_text(
        f"✅ To'g'ri javob: {correct_answer}\n\n"
        f"📁 <b>Kategoriyani kiriting:</b>\n\n"
        f"Misol:\n"
        f"- Umumiy qoidalar\n"
        f"- Yo'l belgilari\n"
        f"- Tezlik chegaralari\n"
        f"- Svetofor signallari\n\n"
        f"Bekor qilish uchun /cancel",
        parse_mode='HTML'
    )
    
    return ADDING_CATEGORY


async def receive_question_category(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Kategoriyani qabul qilish va savolni saqlash"""
    category = update.message.text.strip()
    
    if len(category) < 3:
        await update.message.reply_text(
            "❌ Kategoriya juda qisqa! Kamida 3 ta belgi kiriting.\n"
            "Qaytadan kiriting yoki /cancel"
        )
        return ADDING_CATEGORY
    
    context.user_data['new_question']['category'] = category
    
    # Savolni saqlash
    question_data = context.user_data['new_question']
    question_id = db.add_question(question_data)
    
    # Savolni ko'rsatish
    from utils.helpers import format_question
    question_text = format_question(question_data, show_answer=True)
    
    await update.message.reply_text(
        f"✅ <b>Savol muvaffaqiyatli qo'shildi!</b>\n\n"
        f"ID: #{question_id}\n\n"
        f"{question_text}\n\n"
        f"📁 Kategoriya: {category}",
        parse_mode='HTML'
    )
    
    # Yana savol qo'shish tugmasi
    keyboard = [
        [InlineKeyboardButton("➕ Yana savol qo'shish", callback_data="add_question_start")],
        [InlineKeyboardButton("📝 Savollar ro'yxati", callback_data="list_questions")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Keyingi amallarni tanlang:",
        reply_markup=reply_markup
    )
    
    # Contextni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END


async def cancel_question_adding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Savol qo'shishni bekor qilish"""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Savol qo'shish bekor qilindi.\n\n"
        "/admin buyrug'i bilan admin panelga qaytishingiz mumkin."
    )
    return ConversationHandler.END


async def list_questions(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Savollar ro'yxati"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    questions = db.get_all_questions()
    
    if not questions:
        await query.edit_message_text("📝 Hozircha savollar yo'q.")
        return
    
    keyboard = []
    for q in questions[:10]:  # Birinchi 10 ta savol
        keyboard.append([
            InlineKeyboardButton(
                f"#{q['id']}: {q['question'][:30]}...",
                callback_data=f"question_info_{q['id']}"
            )
        ])
    
    if len(questions) > 10:
        keyboard.append([InlineKeyboardButton(f"... va yana {len(questions) - 10} ta", callback_data="show_more_questions")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_questions")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📝 <b>Savollar ro'yxati</b>\n\n"
        f"Jami: {len(questions)} ta\n\n"
        f"Batafsil ma'lumot olish uchun savolni tanlang:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def question_info(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Savol haqida ma'lumot"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    question_id = int(query.data.split('_')[2])
    question = db.get_question(question_id)
    
    if not question:
        await query.edit_message_text("❌ Savol topilmadi.")
        return
    
    question_text = format_question(question, show_answer=True)
    question_text += f"\n\n📁 Kategoriya: {question.get('category', 'N/A')}"
    
    keyboard = [
        [InlineKeyboardButton("🗑 O'chirish", callback_data=f"delete_question_{question_id}")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="list_questions")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        question_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Savolni o'chirish"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    question_id = int(query.data.split('_')[2])
    
    # Tasdiqlash
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"confirm_delete_q_{question_id}"),
            InlineKeyboardButton("❌ Yo'q", callback_data=f"question_info_{question_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚠️ <b>Diqqat!</b>\n\n"
        "Bu savolni o'chirmoqchimisiz?",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def confirm_delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Savolni o'chirishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id, admin_id):
        await query.edit_message_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    question_id = int(query.data.split('_')[3])
    
    if db.remove_question(question_id):
        await query.edit_message_text("✅ Savol o'chirildi.")
    else:
        await query.edit_message_text("❌ Xatolik yuz berdi.")


async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database, admin_id: int):
    """Umumiy statistika"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id, admin_id):
        await update.message.reply_text("⛔ Sizda bu buyruqqa ruxsat yo'q!")
        return
    
    users = db.get_all_users()
    questions = db.get_all_questions()
    
    active_users = sum(1 for u in users if u.get('is_active', False))
    
    stats_text = (
        f"📊 <b>Umumiy statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {len(users)}\n"
        f"✅ Faol foydalanuvchilar: {active_users}\n"
        f"❓ Jami savollar: {len(questions)}\n"
    )
    
    await update.message.reply_text(stats_text, parse_mode='HTML')


# ========== FAYLDAN SAVOLLAR YUKLASH ==========

import os

async def upload_questions_file_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fayldan yuklashni boshlash"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "📁 <b>Fayldan savollar yuklash</b>\n\n"
        "Savollar fayli yuborishingiz mumkin:\n\n"
        "📄 <b>Qo'llab-quvvatlanadigan formatlar:</b>\n"
        "• .txt - Text fayl\n"
        "• .docx - Word hujjat\n"
        "• .xlsx - Excel jadval\n\n"
        "📋 <b>Text/Word format:</b>\n\n"
        "1. Savol matni?\n"
        "A) Variant A\n"
        "B) Variant B\n"
        "C) Variant C\n"
        "D) Variant D\n"
        "Javob: B\n"
        "Kategoriya: Umumiy\n\n"
        "2. Keyingi savol...\n\n"
        "Faylni yuboring yoki /cancel",
        parse_mode='HTML'
    )
    
    context.user_data['awaiting_file'] = True
    return ADDING_QUESTION


async def receive_questions_file(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Yuklangan faylni qayta ishlash"""
    if not update.message.document:
        await update.message.reply_text(
            "❌ Iltimos, hujjat fayl yuboring.\n\n"
            "Bekor qilish uchun /cancel"
        )
        return ADDING_QUESTION
    
    document = update.message.document
    file_name = document.file_name
    file_ext = os.path.splitext(file_name)[1].lower()
    
    # Fayl formatini tekshirish
    if file_ext not in ['.txt', '.docx', '.xlsx', '.doc']:
        await update.message.reply_text(
            f"❌ Qo'llab-quvvatlanmaydigan fayl: {file_ext}\n\n"
            "Faqat: .txt, .docx, .xlsx\n\n"
            "Boshqa fayl yuboring yoki /cancel"
        )
        return ADDING_QUESTION
    
    # Faylni yuklab olish
    await update.message.reply_text("⏳ Fayl yuklanmoqda...")
    
    try:
        file = await document.get_file()
        file_path = f"/tmp/{file_name}"
        await file.download_to_drive(file_path)
        
        # Faylni qayta ishlash
        await update.message.reply_text("🔄 Fayl qayta ishlanmoqda...")
        
        from utils.file_parser import process_uploaded_file
        questions, errors = await process_uploaded_file(file_path)
        
        # Faylni o'chirish
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Xatolar
        if errors and len(errors) > 0:
            error_text = "⚠️ <b>Ogohlantirishlar:</b>\n\n"
            error_text += "\n".join(errors[:5])
            if len(errors) > 5:
                error_text += f"\n\n... va yana {len(errors) - 5} ta"
            
            await update.message.reply_text(error_text, parse_mode='HTML')
        
        # Savollar topilmadi
        if not questions or len(questions) == 0:
            await update.message.reply_text(
                "❌ Faylda savollar topilmadi.\n\n"
                "Format:\n"
                "1. Savol?\n"
                "A) Variant\n"
                "B) Variant\n"
                "Javob: A\n\n"
                "Boshqa fayl yuboring yoki /cancel"
            )
            return ADDING_QUESTION
        
        # Savollarni ko'rsatish
        sample_count = min(3, len(questions))
        sample_text = "<b>Namuna (birinchi savollar):</b>\n\n"
        
        for i, q in enumerate(questions[:sample_count], 1):
            sample_text += f"{i}. {q['question'][:50]}...\n"
            sample_text += f"   To'g'ri: {q['correct_answer']}\n\n"
        
        # Tasdiqlash
        keyboard = [
            [InlineKeyboardButton(f"✅ Ha, {len(questions)} ta savolni qo'shish", callback_data="confirm_file_upload")],
            [InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data="cancel_file_upload")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Savollarni contextga saqlash
        context.user_data['pending_questions'] = questions
        
        await update.message.reply_text(
            f"📊 <b>Fayl muvaffaqiyatli yuklandi!</b>\n\n"
            f"✅ Topildi: <b>{len(questions)} ta savol</b>\n\n"
            f"{sample_text}\n"
            f"Savollarni ma'lumotlar bazasiga qo'shishni tasdiqlaysizmi?",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        return ConversationHandler.END
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Xatolik yuz berdi:\n{str(e)}\n\n"
            "Boshqa fayl yuboring yoki /cancel"
        )
        return ADDING_QUESTION


async def confirm_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Fayldan savollarni qo'shishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    pending_questions = context.user_data.get('pending_questions', [])
    
    if not pending_questions:
        await query.edit_message_text("❌ Savollar topilmadi. Qaytadan urinib ko'ring.")
        context.user_data.clear()
        return
    
    # Savollarni qo'shish
    added_count = 0
    for q_data in pending_questions:
        try:
            db.add_question(q_data)
            added_count += 1
        except Exception as e:
            print(f"Error adding question: {e}")
    
    context.user_data.clear()
    
    # Natija
    keyboard = [
        [InlineKeyboardButton("📝 Savollar ro'yxati", callback_data="list_questions")],
        [InlineKeyboardButton("➕ Yana savol qo'shish", callback_data="add_question_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✅ <b>Muvaffaqiyatli!</b>\n\n"
        f"📊 {added_count} ta savol qo'shildi!\n\n"
        f"Jami savollar: {db.get_questions_count()}",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def cancel_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fayldan yuklashni bekor qilish"""
    query = update.callback_query
    await query.answer()
    
    context.user_data.clear()
    
    await query.edit_message_text(
        "❌ Fayldan yuklash bekor qilindi.\n\n"
        "/admin buyrug'i bilan admin panelga qaytishingiz mumkin."
    )

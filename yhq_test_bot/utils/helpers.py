"""
Utility functions for YHQ Test Bot
Yordamchi funksiyalar
"""

import hashlib
import platform
import uuid
from typing import Optional


def get_device_id() -> str:
    """
    Qurilma ID'sini olish
    Bu funksiya Telegram client'da ishlamaydi, 
    shuning uchun user o'zi device_id yuborishi kerak
    """
    # Platform ma'lumotlari
    system = platform.system()
    node = platform.node()
    processor = platform.processor()
    
    # Unique ID yaratish
    device_info = f"{system}-{node}-{processor}"
    device_id = hashlib.md5(device_info.encode()).hexdigest()
    
    return device_id


def generate_unique_id() -> str:
    """Unikal ID yaratish"""
    return str(uuid.uuid4())


def format_question(question: dict, show_answer: bool = False) -> str:
    """Savolni formatlash"""
    text = f"❓ <b>Savol #{question['id']}</b>\n\n"
    text += f"{question['question']}\n\n"
    
    for key, value in question['options'].items():
        text += f"{key}) {value}\n"
    
    if show_answer:
        text += f"\n✅ <b>To'g'ri javob:</b> {question['correct_answer']}"
    
    return text


def format_user_info(user: dict) -> str:
    """Foydalanuvchi ma'lumotlarini formatlash"""
    status = "✅ Faol" if user.get('is_active', False) else "❌ Nofaol"
    
    text = f"👤 <b>Foydalanuvchi ma'lumotlari</b>\n\n"
    text += f"🆔 ID: <code>{user.get('user_id', 'N/A')}</code>\n"
    text += f"👨‍💼 Ism: {user.get('name', 'N/A')}\n"
    text += f"📱 Qurilma ID: <code>{user.get('device_id', 'N/A')}</code>\n"
    text += f"📅 Ro'yxatdan o'tgan: {user.get('registered_at', 'N/A')[:10]}\n"
    text += f"📊 Holat: {status}"
    
    return text


def format_statistics(stats: dict) -> str:
    """Statistikani formatlash"""
    text = "📊 <b>Sizning statistikangiz</b>\n\n"
    text += f"✅ To'g'ri javoblar: {stats['correct']}\n"
    text += f"❌ Noto'g'ri javoblar: {stats['wrong']}\n"
    text += f"📝 Jami savollar: {stats['total']}\n"
    text += f"🎯 Natija: {stats['percentage']}%"
    
    return text


def create_keyboard_markup(buttons: list) -> list:
    """Klaviatura yaratish"""
    keyboard = []
    row = []
    
    for i, button in enumerate(buttons):
        row.append(button)
        if (i + 1) % 2 == 0:  # Har 2 ta tugmadan keyin yangi qator
            keyboard.append(row)
            row = []
    
    if row:  # Qolgan tugmalarni qo'shish
        keyboard.append(row)
    
    return keyboard


def validate_question_data(data: dict) -> tuple[bool, Optional[str]]:
    """Savol ma'lumotlarini tekshirish"""
    required_fields = ['question', 'options', 'correct_answer', 'category']
    
    for field in required_fields:
        if field not in data:
            return False, f"'{field}' maydoni mavjud emas"
    
    if not isinstance(data['options'], dict):
        return False, "Variantlar lug'at formatida bo'lishi kerak"
    
    if len(data['options']) < 2:
        return False, "Kamida 2 ta variant bo'lishi kerak"
    
    if data['correct_answer'] not in data['options']:
        return False, "To'g'ri javob variantlar ichida mavjud emas"
    
    return True, None


def escape_markdown(text: str) -> str:
    """Markdown uchun maxsus belgilarni qochirish"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

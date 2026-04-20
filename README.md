# YHQ Test Bot - Yo'l Harakati Qoidalari Test Boti

Telegram bot yo'l harakati qoidalari bo'yicha test topshirish uchun.

## 🚀 Xususiyatlar

### Foydalanuvchilar uchun:
- ✅ Test topshirish
- 📊 Statistikani ko'rish
- 👤 Profil ma'lumotlari
- 📝 Natijalarni kuzatish

### Admin uchun:
- 👥 Foydalanuvchilarni boshqarish (qo'shish/o'chirish)
- ❓ Savollarni boshqarish (qo'shish/o'chirish)
- 📊 Umumiy statistika
- 🔐 Ruxsat berish tizimi (bitta qurilma uchun)

## 📋 Talablar

- Python 3.8+
- Telegram Bot Token (BotFather'dan)
- Admin Telegram ID

## 🔧 O'rnatish

### 1. Loyihani yuklab olish
```bash
cd yhq_test_bot
```

### 2. Virtual muhit yaratish (tavsiya etiladi)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Konfiguratsiya

`.env.example` faylidan nusxa oling:
```bash
cp .env.example .env
```

`.env` faylini tahrirlang va quyidagi ma'lumotlarni kiriting:

```env
# Telegram Bot Token (BotFather'dan oling)
BOT_TOKEN=your_bot_token_here

# Admin Telegram ID (o'z telegram ID'ingiz)
ADMIN_ID=your_telegram_id_here

# Database fayl nomi
DATABASE_PATH=database/bot_data.json
```

### 5. Telegram Bot Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) botini oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Bot username'ini kiriting (debe_yhq_bot kabi)
5. Token oling va `.env` fayliga kiriting

### 6. Telegram ID'ni topish

1. [@userinfobot](https://t.me/userinfobot) botini oching
2. `/start` buyrug'ini yuboring
3. Sizning ID'ingizni olasiz
4. Bu ID'ni `.env` faylidagi `ADMIN_ID` ga kiriting

## 🏃 Ishga tushirish

```bash
python main.py
```

Agar hammasi to'g'ri sozlangan bo'lsa, konsolda quyidagi xabar chiqadi:
```
Bot ishga tushmoqda...
```

## 📱 Foydalanish

### Foydalanuvchilar uchun:

1. Botni oching va `/start` buyrug'ini bosing
2. Agar siz ro'yxatdan o'tmagan bo'lsangiz, "Ro'yxatdan o'tish so'rovi yuborish" tugmasini bosing
3. Admin sizga ruxsat berguncha kuting
4. Ruxsat olgandan keyin, testni boshlashingiz mumkin

### Admin uchun:

1. `/admin` buyrug'ini bosing - Admin panel ochiladi
2. **Foydalanuvchilar** - Foydalanuvchilarni boshqarish
   - Yangi so'rovlarni ko'rish va tasdiqlash
   - Foydalanuvchilarni faollashtirish/o'chirish
   - Foydalanuvchilarni butunlay o'chirish
3. **Savollar** - Savollarni boshqarish
   - Yangi savol qo'shish
   - Savollarni ko'rish
   - Savollarni o'chirish

## 🗂 Loyiha tuzilmasi

```
yhq_test_bot/
│
├── database/
│   ├── db_manager.py      # Ma'lumotlar bazasi boshqaruvchisi
│   └── bot_data.json      # Ma'lumotlar bazasi (avtomatik yaratiladi)
│
├── handlers/
│   ├── user_handlers.py   # Foydalanuvchilar uchun handlerlar
│   └── admin_handlers.py  # Admin uchun handlerlar
│
├── utils/
│   └── helpers.py         # Yordamchi funksiyalar
│
├── main.py                # Asosiy fayl
├── requirements.txt       # Kerakli kutubxonalar
├── .env.example          # Konfiguratsiya namunasi
├── .env                  # Konfiguratsiya (o'zingiz yarating)
└── README.md             # Bu fayl
```

## 📊 Ma'lumotlar bazasi tuzilmasi

Bot JSON formatida ma'lumotlarni saqlaydi:

```json
{
  "users": {
    "123456789": {
      "device_id": "123456789",
      "name": "Ism Familiya",
      "registered_at": "2024-01-01T12:00:00",
      "is_active": true
    }
  },
  "questions": [
    {
      "id": 1,
      "question": "Savol matni?",
      "options": {
        "A": "Variant A",
        "B": "Variant B",
        "C": "Variant C",
        "D": "Variant D"
      },
      "correct_answer": "B",
      "category": "Umumiy qoidalar"
    }
  ],
  "user_progress": {
    "123456789": {
      "correct": 5,
      "wrong": 2,
      "current_question": 7,
      "answered_questions": [1, 2, 3, 4, 5, 6, 7]
    }
  }
}
```

## ➕ Savol qo'shish

### Admin orqali (tavsiya etiladi):
1. `/admin` buyrug'ini bosing
2. "Savollar" tugmasini bosing
3. "Savol qo'shish" tugmasini bosing
4. Ko'rsatmalarga amal qiling

### Ma'lumotlar bazasiga to'g'ridan-to'g'ri:
`database/bot_data.json` faylini oching va `questions` massiviga savol qo'shing:

```json
{
  "id": 1,
  "question": "O'zbekiston Respublikasi yo'llarida qanday harakat tartibi belgilangan?",
  "options": {
    "A": "Chap tomonlama harakat",
    "B": "O'ng tomonlama harakat",
    "C": "Ikki tomonlama harakat",
    "D": "Erkin harakat"
  },
  "correct_answer": "B",
  "category": "Umumiy qoidalar",
  "created_at": "2024-01-01T12:00:00"
}
```

## 🔒 Xavfsizlik

- Bot faqat admin tomonidan ruxsat berilgan foydalanuvchilarga ochiq
- Har bir foydalanuvchi faqat bitta qurilmadan foydalanishi mumkin
- Admin barcha foydalanuvchilarni nazorat qiladi

## 🐛 Xatolarni tuzatish

Agar bot ishlamasa:

1. Python versiyasini tekshiring: `python --version` (3.8+ bo'lishi kerak)
2. `.env` faylini tekshiring (token va ID to'g'ri kiritilganmi?)
3. Internet ulanishini tekshiring
4. Konsolda xato xabarlarini o'qing

## 📞 Yordam

Agar muammo bo'lsa:
1. Konsolda xato xabarini ko'ring
2. `.env` faylni qayta tekshiring
3. Botni qayta ishga tushiring

## 📝 Litsenziya

Bu loyiha ta'lim maqsadida yaratilgan.

## 👨‍💻 Muallif

YHQ Team

---

**Omad tilaymiz! 🚗💨**

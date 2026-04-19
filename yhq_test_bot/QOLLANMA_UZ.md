# 📚 YHQ Test Bot - To'liq Qo'llanma

## 📋 MUNDARIJA
1. [Boshlash](#1-boshlash)
2. [O'rnatish](#2-ornatish)
3. [Sozlash](#3-sozlash)
4. [Ishga tushirish](#4-ishga-tushirish)
5. [Admin funksiyalari](#5-admin-funksiyalari)
6. [Savol qo'shish](#6-savol-qoshish)
7. [Foydalanuvchilarni boshqarish](#7-foydalanuvchilarni-boshqarish)
8. [Muammolarni hal qilish](#8-muammolarni-hal-qilish)

---

## 1. BOSHLASH

### 1.1. Kerakli dasturlar

Sizga quyidagilar kerak:
- ✅ Python 3.8 yoki undan yuqori
- ✅ PyCharm IDE (tavsiya etiladi) yoki boshqa IDE
- ✅ Telegram account
- ✅ Internet ulanishi

### 1.2. Python o'rnatilganligini tekshirish

Terminal/CMD da quyidagi buyruqni kiriting:
```bash
python --version
# yoki
python3 --version
```

Agar `Python 3.8.x` yoki yuqori ko'rsatsa, davom eting.

---

## 2. O'RNATISH

### 2.1. Loyihani yuklab olish

1. `yhq_test_bot_final.zip` faylini yuklab oling
2. Faylni istalgan joyga chiqarib oling (masalan: `C:\Projects\` yoki `~/Projects/`)

### 2.2. PyCharm'da ochish

1. PyCharm'ni oching
2. `File` → `Open`
3. `yhq_test_bot` papkasini tanlang
4. `OK` tugmasini bosing

### 2.3. Virtual muhit yaratish (PyCharm'da)

PyCharm avtomatik ravishda virtual muhit yaratishni taklif qiladi:
1. Pastki o'ng burchakda `Python 3.x` yozuvini bosing
2. `Add Interpreter` → `Add Local Interpreter`
3. `Virtualenv` → `New`
4. `OK` tugmasini bosing

**Yoki Terminal orqali:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2.4. Kutubxonalarni o'rnatish

PyCharm Terminal'da:
```bash
pip install -r requirements.txt
```

Kutib turing... O'rnatiladi:
- ✅ python-telegram-bot (bot uchun)
- ✅ python-dotenv (konfiguratsiya uchun)

---

## 3. SOZLASH

### 3.1. Telegram Bot yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) botini oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: `YHQ Test Bot`)
4. Bot username'ini kiriting (masalan: `yhq_test_2024_bot`)
5. Token oling (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**MUHIM:** Tokenni hech kimga bermang!

### 3.2. Telegram ID'ni topish

1. Telegram'da [@userinfobot](https://t.me/userinfobot) botini oching
2. `/start` buyrug'ini yuboring
3. Sizning ID'ingizni ko'rasiz (masalan: `123456789`)

### 3.3. .env fayl yaratish

1. `.env.example` faylni nusxa oling va `.env` deb nomlang
2. `.env` faylini oching
3. Quyidagi ma'lumotlarni kiriting:

```env
# Telegram Bot Token (BotFather'dan)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Admin Telegram ID (o'z ID'ingiz)
ADMIN_ID=123456789

# Database fayl yo'li
DATABASE_PATH=database/bot_data.json
```

**DIQQAT:** 
- `BOT_TOKEN` - BotFather'dan olgan token
- `ADMIN_ID` - O'z Telegram ID'ingiz
- Hech qanday qo'shimcha belgi (probel, tirnoq) qo'shmang!

---

## 4. ISHGA TUSHIRISH

### 4.1. Savollarni import qilish (birinchi marta)

PyCharm Terminal'da:
```bash
python import_questions.py
```

Natija:
```
✅ 10 ta savol ma'lumotlar bazasiga qo'shildi!
📁 Fayl: database/bot_data.json
```

### 4.2. Botni ishga tushirish

PyCharm Terminal'da:
```bash
python main.py
```

Natija:
```
Bot ishga tushmoqda...
```

**Agar xatolik bo'lsa:**
- `.env` fayl to'g'ri to'ldirilganligini tekshiring
- Token va ID to'g'riligini tekshiring
- Internet ulanishini tekshiring

### 4.3. Botni tekshirish

1. Telegram'da o'z botingizni toping
2. `/start` buyrug'ini yuboring
3. Asosiy menyu ko'rinishi kerak

---

## 5. ADMIN FUNKSIYALARI

### 5.1. Admin panelga kirish

Telegram botida:
```
/admin
```

Natija:
```
🔐 Admin Panel

👥 Foydalanuvchilar: 0
❓ Savollar: 10

Quyidagi bo'limlardan birini tanlang:
[👥 Foydalanuvchilar] [❓ Savollar]
[📊 Statistika] [⚙️ Sozlamalar]
```

### 5.2. Admin panel menyu

- **👥 Foydalanuvchilar** - Foydalanuvchilarni boshqarish
- **❓ Savollar** - Savollarni boshqarish
- **📊 Statistika** - Umumiy statistika
- **⚙️ Sozlamalar** - Bot sozlamalari

---

## 6. SAVOL QO'SHISH

### 6.1. Savol qo'shish bosqichlari

#### Qadam 1: Admin panelni oching
```
/admin → ❓ Savollar → ➕ Savol qo'shish
```

#### Qadam 2: Savol matnini kiriting

Bot so'raydi:
```
📝 Yangi savol qo'shish

Savol matnini yuboring:

Misol: O'zbekiston Respublikasi yo'llarida 
qanday harakat tartibi belgilangan?
```

Siz yuboring:
```
Aholi punktlarida maksimal tezlik necha km/soat?
```

#### Qadam 3: Variantlarni kiriting

Bot so'raydi:
```
📋 Endi variantlarni kiriting:

Quyidagi formatda yuboring:
A) Variant 1
B) Variant 2
C) Variant 3
D) Variant 4
```

Siz yuboring:
```
A) 40 km/soat
B) 50 km/soat
C) 60 km/soat
D) 70 km/soat
```

**MUHIM:**
- Har bir variant yangi qatordan boshlanishi kerak
- Format: `A)` dan keyin probel
- Kamida 2 ta variant bo'lishi kerak

#### Qadam 4: To'g'ri javobni tanlang

Bot ko'rsatadi:
```
✅ Variantlar saqlandi!

Variantlar:
A) 40 km/soat
B) 50 km/soat
C) 60 km/soat
D) 70 km/soat

To'g'ri javobni tanlang:
[A] [B] [C] [D]
```

Tugmani bosing: `C`

#### Qadam 5: Kategoriyani kiriting

Bot so'raydi:
```
📁 Kategoriyani kiriting:

Misol:
- Umumiy qoidalar
- Yo'l belgilari
- Tezlik chegaralari
```

Siz yuboring:
```
Tezlik chegaralari
```

#### Qadam 6: Tasdiqlash

Bot ko'rsatadi:
```
✅ Savol muvaffaqiyatli qo'shildi!

ID: #11

❓ Savol #11

Aholi punktlarida maksimal tezlik necha km/soat?

A) 40 km/soat
B) 50 km/soat
C) 60 km/soat
D) 70 km/soat

✅ To'g'ri javob: C

📁 Kategoriya: Tezlik chegaralari
```

### 6.2. Savol qo'shishni bekor qilish

Istalgan vaqtda:
```
/cancel
```

### 6.3. Ko'p savol qo'shish

Bir savolni qo'shgandan keyin:
```
[➕ Yana savol qo'shish] tugmasini bosing
```

Yoki:
```
/admin → ❓ Savollar → ➕ Savol qo'shish
```

### 6.4. Mavjud savollarni ko'rish

```
/admin → ❓ Savollar → 📝 Savollar ro'yxati
```

Natija:
```
📝 Savollar ro'yxati

Jami: 11 ta

Batafsil ma'lumot olish uchun savolni tanlang:
[#1: O'zbekiston Respublikasi yo'l...]
[#2: Haydovchi yonida qanday hujjat...]
...
```

### 6.5. Savolni o'chirish

1. Savollar ro'yxatidan savolni tanlang
2. `🗑 O'chirish` tugmasini bosing
3. Tasdiqlang: `✅ Ha, o'chirish`

---

## 7. FOYDALANUVCHILARNI BOSHQARISH

### 7.1. Yangi foydalanuvchi qo'shish

#### Foydalanuvchi tomoni:

1. Foydalanuvchi botga `/start` yuboradi
2. Bot ko'rsatadi:
```
⚠️ Siz hali ro'yxatdan o'tmagansiz.

Botdan foydalanish uchun admin ruxsatini so'rang.

[📝 Ro'yxatdan o'tish so'rovi yuborish]
```

3. Foydalanuvchi tugmani bosadi

#### Admin tomoni:

Admin ga xabar keladi:
```
🔔 Yangi ruxsat so'rovi

👤 Ism: Aziz Karimov
🆔 User ID: 987654321
📱 Device ID: 987654321
👨‍💼 Username: @aziz_karimov

Foydalanuvchiga ruxsat berasizmi?

[✅ Ruxsat berish] [❌ Rad etish]
```

Admin tugmani bosadi:
- `✅ Ruxsat berish` - Foydalanuvchi qo'shiladi
- `❌ Rad etish` - So'rov rad etiladi

### 7.2. Foydalanuvchilar ro'yxati

```
/admin → 👥 Foydalanuvchilar
```

Natija:
```
👥 Foydalanuvchilar ro'yxati

Jami: 5 ta

✅ Aziz Karimov (ID: 987654321)
✅ Bekzod Tursunov (ID: 876543210)
❌ Dilshod Rahimov (ID: 765432109)
...
```

### 7.3. Foydalanuvchi haqida ma'lumot

Foydalanuvchini tanlang:

```
👤 Foydalanuvchi ma'lumotlari

🆔 ID: 987654321
👨‍💼 Ism: Aziz Karimov
📱 Qurilma ID: 987654321
📅 Ro'yxatdan o'tgan: 2024-01-15
📊 Holat: ✅ Faol

📊 Statistika:
✅ To'g'ri: 45
❌ Noto'g'ri: 5
🎯 Natija: 90%

[🚫 O'chirish] [🗑 Butunlay o'chirish]
```

**Tugmalar:**
- `🚫 O'chirish` - Foydalanuvchini vaqtincha o'chiradi (qayta faollashtirish mumkin)
- `🗑 Butunlay o'chirish` - Foydalanuvchini butunlay o'chiradi (qaytarib bo'lmaydi)

### 7.4. Foydalanuvchini qayta faollashtirish

O'chirilgan foydalanuvchini tanlang:
```
[✅ Faollashtirish] tugmasini bosing
```

---

## 8. MUAMMOLARNI HAL QILISH

### 8.1. Bot ishlamayapti

**Muammo:** Bot ishga tushmayapti

**Yechim:**
1. Python versiyasini tekshiring:
   ```bash
   python --version
   ```
   3.8+ bo'lishi kerak

2. Kutubxonalar o'rnatilganligini tekshiring:
   ```bash
   pip list
   ```

3. `.env` faylni tekshiring:
   - BOT_TOKEN to'g'ri kiritilganmi?
   - ADMIN_ID to'g'ri kiritilganmi?
   - Hech qanday qo'shimcha probel yo'qmi?

4. Internetga ulanganligini tekshiring

### 8.2. "Invalid token" xatosi

**Muammo:** `Invalid token` xatosi chiqyapti

**Yechim:**
1. BotFather'dan yangi token oling
2. `.env` faylda `BOT_TOKEN` ni yangilang
3. Botni qayta ishga tushiring

### 8.3. Admin panel ochilmayapti

**Muammo:** `/admin` buyrug'i ishlamayapti

**Yechim:**
1. `.env` faylda `ADMIN_ID` to'g'ri kiritilganligini tekshiring
2. O'z Telegram ID'ingizni qayta tekshiring [@userinfobot](https://t.me/userinfobot) da
3. Botni qayta ishga tushiring

### 8.4. Savollar ko'rinmayapti

**Muammo:** Testda savollar yo'q

**Yechim:**
1. Savollar import qilinganligini tekshiring:
   ```bash
   python import_questions.py
   ```

2. `database/bot_data.json` faylini oching
3. `questions` massivida savollar borligini tekshiring

4. Agar yo'q bo'lsa, admin orqali savol qo'shing

### 8.5. Database xatosi

**Muammo:** `database/bot_data.json` faylida xato

**Yechim:**
1. Faylni o'chiring
2. Botni qayta ishga tushiring (avtomatik yangi fayl yaratadi)
3. Savollarni qayta import qiling

### 8.6. ConversationHandler xatosi

**Muammo:** Savol qo'shishda xato

**Yechim:**
1. `/cancel` buyrug'i bilan jarayonni bekor qiling
2. Qaytadan boshlang
3. Formatni to'g'ri kiriting

---

## 9. QO'SHIMCHA MA'LUMOTLAR

### 9.1. Fayllar tuzilmasi

```
yhq_test_bot/
├── database/
│   ├── db_manager.py      # Database boshqaruvchisi
│   └── bot_data.json      # Ma'lumotlar bazasi
├── handlers/
│   ├── user_handlers.py   # Foydalanuvchi handlerlari
│   └── admin_handlers.py  # Admin handlerlari
├── utils/
│   └── helpers.py         # Yordamchi funksiyalar
├── main.py                # Asosiy fayl
├── import_questions.py    # Savollar import qilish
├── requirements.txt       # Kutubxonalar ro'yxati
├── .env                   # Konfiguratsiya (o'zingiz yaratish)
└── README.md              # Qo'llanma
```

### 9.2. Buyruqlar ro'yxati

**Barcha foydalanuvchilar uchun:**
- `/start` - Botni boshlash
- `/cancel` - Jarayonni bekor qilish

**Faqat admin uchun:**
- `/admin` - Admin panel

### 9.3. Klaviatura tugmalari

**Asosiy menyu:**
- 📝 Testni boshlash
- 📊 Statistika
- ℹ️ Qo'llanma
- 👤 Profil

**Admin menyu:**
- 👥 Foydalanuvchilar
- ❓ Savollar
- 📊 Statistika
- ⚙️ Sozlamalar

### 9.4. Ma'lumotlar bazasi

**Joylashuv:** `database/bot_data.json`

**Tuzilma:**
```json
{
  "users": {
    "123456789": {
      "device_id": "123456789",
      "name": "Aziz Karimov",
      "registered_at": "2024-01-15T10:30:00",
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
      "category": "Kategoriya"
    }
  ],
  "user_progress": {
    "123456789": {
      "correct": 45,
      "wrong": 5,
      "answered_questions": [1, 2, 3, ...]
    }
  }
}
```

### 9.5. Xavfsizlik

- ✅ Faqat admin savollar qo'sha oladi
- ✅ Har bir foydalanuvchi faqat 1 qurilmadan foydalana oladi
- ✅ Admin barcha foydalanuvchilarni nazorat qiladi
- ✅ Bot token maxfiy saqlanadi

---

## 10. YORDAM

### Muammo yuzaga kelsa:

1. Qo'llanmani qayta o'qing
2. `.env` faylni tekshiring
3. Terminal'dagi xato xabarlarini o'qing
4. Botni qayta ishga tushiring

### Aloqa:

Texnik yordam uchun murojaat qiling.

---

**Omad tilaymiz! 🚗💨**

Bot tayyor va ishlamoqda! ✨

# ⚡ TEZKOR BOSHLASH

## 1️⃣ O'RNATISH (5 daqiqa)

```bash
# 1. Papkani oching
cd yhq_test_bot

# 2. Virtual muhit yarating
python -m venv venv

# 3. Faollashtiring
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Kutubxonalarni o'rnating
pip install -r requirements.txt
```

## 2️⃣ SOZLASH (3 daqiqa)

### A) Telegram Bot yarating
1. [@BotFather](https://t.me/BotFather) ga `/newbot`
2. Token oling: `1234567890:ABC...`

### B) Telegram ID'ni oling
1. [@userinfobot](https://t.me/userinfobot) ga `/start`
2. ID ni ko'ring: `123456789`

### C) .env faylni to'ldiring
```bash
# .env.example dan nusxa oling
cp .env.example .env

# .env ni tahrirlang:
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789
DATABASE_PATH=database/bot_data.json
```

## 3️⃣ ISHGA TUSHIRISH (1 daqiqa)

```bash
# Savollarni import qiling (birinchi marta)
python import_questions.py

# Botni ishga tushiring
python main.py
```

✅ **Tayyor!** Telegram'da botingizni toping va `/start` bosing!

---

## 📝 SAVOL QO'SHISH (Admin uchun)

Telegram botida:

```
1. /admin
2. ❓ Savollar
3. ➕ Savol qo'shish
4. Savol matnini kiriting
5. Variantlarni kiriting (A) B) C) D))
6. To'g'ri javobni tanlang
7. Kategoriyani kiriting
8. ✅ Tayyor!
```

**Misol:**

```
Savol: Aholi punktlarida maksimal tezlik?

Variantlar:
A) 40 km/soat
B) 50 km/soat
C) 60 km/soat
D) 70 km/soat

To'g'ri: C
Kategoriya: Tezlik chegaralari
```

---

## 👥 FOYDALANUVCHI QO'SHISH

### Foydalanuvchi tomoni:
1. Botda `/start`
2. "Ro'yxatdan o'tish so'rovi yuborish" tugmasini bosish

### Admin tomoni:
1. Adminга xabar keladi
2. "✅ Ruxsat berish" tugmasini bosish

---

## ❓ TEZ-TEZ SO'RALADIGAN SAVOLLAR

**Bot ishlamayapti?**
- Python 3.8+ o'rnatilganligini tekshiring
- .env fayldagi token va ID ni tekshiring
- Internet ulanishini tekshiring

**Admin panel ochilmayapti?**
- .env dagi ADMIN_ID ni tekshiring
- O'z Telegram ID'ingizni to'g'ri kiriting

**Savollar yo'q?**
- `python import_questions.py` ni bajaring

**Savol qo'shishda xato?**
- `/cancel` bosing va qaytadan boshlang
- Format: `A) Variant` (probel muhim!)

---

## 📚 To'liq qo'llanma

Batafsil ma'lumot uchun `QOLLANMA_UZ.md` faylini o'qing.

---

**Omad! 🚀**

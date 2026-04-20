# 📁 FAYLDAN SAVOLLAR YUKLASH - Qo'llanma

## 🎯 IKKALA USUL

Bot orqali savollar qo'shishning **2 usuli** bor:

1. **➕ Bitta savol qo'shish** - Telegram orqali, qo'lda
2. **📁 Fayldan yuklash** - Ko'p savollarni bir vaqtda

---

## 📝 USUL 1: Bitta savol qo'shish (Telegram orqali)

### Qadam-baqadam:

```
1. /admin
2. ❓ Savollar
3. ➕ Bitta savol qo'shish
4. Savol matnini kiriting
5. Variantlarni kiriting
6. To'g'ri javobni tanlang
7. Kategoriyani kiriting
8. ✅ Tayyor!
```

### Misol:

**Savol:**
```
Aholi punktlarida maksimal tezlik necha km/soat?
```

**Variantlar:**
```
A) 40 km/soat
B) 50 km/soat
C) 60 km/soat
D) 70 km/soat
```

**To'g'ri javob:** `C`

**Kategoriya:** `Tezlik chegaralari`

---

## 📁 USUL 2: Fayldan yuklash

### 2.1. Qo'llab-quvvatlanadigan formatlar:

- ✅ `.txt` - Text fayl (Notepad)
- ✅ `.docx` - Word hujjat
- ✅ `.xlsx` - Excel jadval

### 2.2. Text fayl formati (.txt)

**Format:**
```
1. Savol matni?
A) Variant A
B) Variant B
C) Variant C
D) Variant D
Javob: B
Kategoriya: Kategoriya nomi

2. Keyingi savol?
A) Variant A
B) Variant B
...
```

**MUHIM:**
- Har bir savol raqam bilan boshlanadi: `1.`, `2.`, `3.`
- Variantlar: `A)`, `B)`, `C)`, `D)` (katta harf + qavs)
- To'g'ri javob: `Javob: B` (yoki `A`, `C`, `D`)
- Kategoriya: `Kategoriya: Nomi` (ixtiyoriy)
- Savollar orasida bo'sh qator bo'lishi kerak

**Namuna fayl:** `NAMUNA_SAVOLLAR.txt` - loyihada mavjud!

### 2.3. Word fayl formati (.docx)

Text fayl bilan bir xil format, faqat Word'da yozilgan.

### 2.4. Excel fayl formati (.xlsx)

**Ustunlar:**

| Savol | A | B | C | D | Javob | Kategoriya |
|-------|---|---|---|---|-------|-----------|
| Savol matni? | Variant A | Variant B | Variant C | Variant D | B | Kategoriya |

**MUHIM:**
- Birinchi qator - header (ustunlar nomi)
- Ikkinchi qatordan boshlab savollar
- Javob ustunida faqat harf: A, B, C yoki D

---

## 🚀 FAYLDAN YUKLASH (Qadam-baqadam)

### Qadam 1: Admin panelni oching
```
/admin → ❓ Savollar → 📁 Fayldan yuklash
```

### Qadam 2: Fayl tayyorlang

**Variant A: Text fayl yaratish (oddiy)**
1. Notepad'ni oching
2. Namunaga qarab savollarni yozing
3. `savollar.txt` deb saqlang

**Variant B: Word fayl**
1. Word'ni oching
2. Savollarni yozing
3. `savollar.docx` deb saqlang

**Variant C: Excel fayl**
1. Excel'ni oching
2. Jadval formatda to'ldiring
3. `savollar.xlsx` deb saqlang

### Qadam 3: Faylni botga yuboring

Telegram botida:
```
📁 Fayldan savollar yuklash

Faylni yuboring...
```

**Faylni yuboring:** 📎 (clip belgisi) → Fayl tanlang → Yuboring

### Qadam 4: Kutib turing

Bot ko'rsatadi:
```
⏳ Fayl yuklanmoqda...
🔄 Fayl qayta ishlanmoqda...
```

### Qadam 5: Tasdiqlang

Bot ko'rsatadi:
```
📊 Fayl muvaffaqiyatli yuklandi!

✅ Topildi: 10 ta savol

Namuna (birinchi savollar):
1. O'zbekiston Respublikasi...
   To'g'ri: B

Savollarni qo'shishni tasdiqlaysizmi?

[✅ Ha, 10 ta savolni qo'shish]
[❌ Yo'q, bekor qilish]
```

**Tasdiqlang:** `✅ Ha, ... ta savolni qo'shish`

### Qadam 6: Tayyor!

```
✅ Muvaffaqiyatli!

📊 10 ta savol qo'shildi!

Jami savollar: 20

[📝 Savollar ro'yxati]
[➕ Yana savol qo'shish]
```

---

## ⚠️ MUHIM QOIDALAR

### ✅ TO'G'RI:

```
1. Savol matni?
A) Variant
B) Variant
C) Variant
D) Variant
Javob: B
Kategoriya: Umumiy
```

### ❌ NOTO'G'RI:

```
Savol matni?           ❌ Raqam yo'q
a) Variant             ❌ Kichik harf
A) Variant             
Javob B                ❌ Ikki nuqta yo'q
```

### Format qoidalari:

1. **Savol raqami:** `1.` - Raqam + nuqta
2. **Variantlar:** `A)` - Katta harf + qavs + probel
3. **To'g'ri javob:** `Javob: B` - "Javob" + ikki nuqta + probel + harf
4. **Kategoriya:** `Kategoriya: Nomi` - Ixtiyoriy
5. **Savollar orasida** - Bo'sh qator (Enter)

---

## 🔧 MUAMMOLARNI HAL QILISH

### ❌ "Faylda savollar topilmadi"

**Sabab:** Format noto'g'ri

**Yechim:**
1. Namuna faylni oching (`NAMUNA_SAVOLLAR.txt`)
2. Format bo'yicha yozing
3. Qayta yuboring

### ❌ "Qo'llab-quvvatlanmaydigan fayl"

**Sabab:** Fayl formati noto'g'ri

**Yechim:**
- Faqat `.txt`, `.docx`, `.xlsx` formatlarini ishlating
- Fayl kengaytmasini tekshiring

### ❌ "Savol #5: To'g'ri javob xato"

**Sabab:** To'g'ri javob variantlarda yo'q

**Yechim:**
- To'g'ri javob A, B, C yoki D bo'lishi kerak
- Variantlarda shu harf mavjud bo'lishi kerak

---

## 💡 MASLAHATLAR

### Ko'p savollarni yuklash:

1. **Namunadan nusxa oling**
   - `NAMUNA_SAVOLLAR.txt` faylni oching
   - Nusxa oling (Ctrl+A, Ctrl+C)
   - Yangi faylga qo'ying (Ctrl+V)

2. **Savollarni tahrirlang**
   - Namuna savollarni o'zgartiring
   - O'z savollaringizni qo'shing

3. **Tekshiring**
   - Format to'g'riligini tekshiring
   - Variantlar to'liqligini tekshiring
   - To'g'ri javoblar to'g'riligini tekshiring

4. **Yuboring**
   - Botga yuboring
   - Natijani kuting

### Tezkor yuklash:

- **10-20 ta savol:** Text fayl (`.txt`)
- **50-100 ta savol:** Word fayl (`.docx`)
- **100+ savol:** Excel fayl (`.xlsx`)

---

## 📊 NAMUNA FAYLLAR

### Text fayl (NAMUNA_SAVOLLAR.txt):

```
1. O'zbekiston Respublikasi yo'llarida qanday harakat tartibi belgilangan?
A) Chap tomonlama harakat
B) O'ng tomonlama harakat
C) Ikki tomonlama harakat
D) Erkin harakat
Javob: B
Kategoriya: Umumiy qoidalar

2. Haydovchi yonida qanday hujjatlarni olib yurishi shart?
A) Faqat haydovchilik guvohnomasi
B) Haydovchilik guvohnomasi va transport vositasi qayd guvohnomasi
C) Haydovchilik guvohnomasi, qayd guvohnomasi, sug'urta polisi
D) Faqat texnik pasport
Javob: C
Kategoriya: Umumiy qoidalar
```

### Excel fayl:

| Savol | A | B | C | D | Javob | Kategoriya |
|-------|---|---|---|---|-------|-----------|
| O'zbekiston Respublikasi yo'llarida qanday harakat tartibi belgilangan? | Chap tomonlama | O'ng tomonlama | Ikki tomonlama | Erkin | B | Umumiy qoidalar |
| Haydovchi yonida qanday hujjatlarni olib yurishi shart? | Faqat guvohnoma | Guvohnoma va qayd | Guvohnoma, qayd, sug'urta | Faqat pasport | C | Umumiy qoidalar |

---

## ✅ TEKSHIRISH RO'YXATI

Fayl yuborishdan oldin:

- [ ] Format to'g'ri (namunaga mos)
- [ ] Har bir savolda 2-4 ta variant
- [ ] To'g'ri javob ko'rsatilgan
- [ ] To'g'ri javob variantlarda mavjud
- [ ] Kategoriya kiritilgan (ixtiyoriy)
- [ ] Savollar orasida bo'sh qator
- [ ] Fayl formati: .txt, .docx yoki .xlsx

---

**Omad! 📁✨**

Savol qo'shish oson va tez!

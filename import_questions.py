"""
Savollarni Word faylidan import qilish skripti
"""

import json
import os


def create_sample_questions():
    """
    Word fayldan olgan savollarni ma'lumotlar bazasiga qo'shish uchun namuna
    """
    
    # Birinchi 10 ta savolni qo'shamiz (namuna sifatida)
    questions = [
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
            "category": "Umumiy qoidalar"
        },
        {
            "id": 2,
            "question": "Haydovchi yonida qanday hujjatlarni olib yurishi shart?",
            "options": {
                "A": "Faqat haydovchilik guvohnomasi",
                "B": "Haydovchilik guvohnomasi va transport vositasi qayd guvohnomasi",
                "C": "Haydovchilik guvohnomasi, qayd guvohnomasi, sug'urta polisi",
                "D": "Faqat texnik pasport"
            },
            "correct_answer": "C",
            "category": "Umumiy qoidalar"
        },
        {
            "id": 3,
            "question": "Xavfsizlik kamarini taqish qanday transport vositalarida majburiy?",
            "options": {
                "A": "Faqat avtomobillarda",
                "B": "Konstruktsiyasida xavfsizlik kamarlari bo'lgan barcha transport vositalarida",
                "C": "Faqat shahar tashqarisida",
                "D": "Faqat yuk avtomobillarida"
            },
            "correct_answer": "B",
            "category": "Umumiy qoidalar"
        },
        {
            "id": 4,
            "question": "Mototsikl va mopedda harakatlanayotgan haydovchi va yo'lovchilar nima kiyishi kerak?",
            "options": {
                "A": "Maxsus kiyim",
                "B": "Maxsus motoshlem",
                "C": "Himoya ko'zoynak",
                "D": "Hech narsa shart emas"
            },
            "correct_answer": "B",
            "category": "Umumiy qoidalar"
        },
        {
            "id": 5,
            "question": "Transport vositasining egasi deb kimga aytiladi?",
            "options": {
                "A": "Transport vositasini boshqaruvchi shaxs",
                "B": "Mulk huquqi yoki boshqa ashyoviy huquqlar asosida egalik qiluvchi shaxs",
                "C": "Transport vositasini sotib olgan shaxs",
                "D": "Transport vositasini ta'mirlaydigan shaxs"
            },
            "correct_answer": "B",
            "category": "Umumiy qoidalar"
        },
        {
            "id": 6,
            "question": "Ogohlantiruvchi yo'l belgilari qanday maqsadda o'rnatiladi?",
            "options": {
                "A": "Harakatni taqiqlash uchun",
                "B": "Oldinda xavfli joy borligini bildirish uchun",
                "C": "Tezlikni cheklash uchun",
                "D": "Yo'nalishni ko'rsatish uchun"
            },
            "correct_answer": "B",
            "category": "Yo'l belgilari"
        },
        {
            "id": 7,
            "question": "'Temir yo'l kesishmasi' belgisi aholi punktlarida kesishmadan qancha masofada o'rnatiladi?",
            "options": {
                "A": "25-50 metr",
                "B": "50-100 metr",
                "C": "100-150 metr",
                "D": "150-200 metr"
            },
            "correct_answer": "B",
            "category": "Yo'l belgilari"
        },
        {
            "id": 8,
            "question": "'Asosiy yo'l' belgisi qanday vazifani bajaradi?",
            "options": {
                "A": "Tezlikni cheklaydi",
                "B": "Chorrahalarda oldin o'tish huquqini beradi",
                "C": "To'xtashni taqiqlaydi",
                "D": "Harakatni to'xtatadi"
            },
            "correct_answer": "B",
            "category": "Yo'l belgilari"
        },
        {
            "id": 9,
            "question": "Aholi punktlarida yengil avtomobillar uchun maksimal ruxsat etilgan tezlik necha km/soat?",
            "options": {
                "A": "40 km/soat",
                "B": "50 km/soat",
                "C": "60 km/soat",
                "D": "70 km/soat"
            },
            "correct_answer": "C",
            "category": "Tezlik chegaralari"
        },
        {
            "id": 10,
            "question": "Qizil svetofor signali nimani bildiradi?",
            "options": {
                "A": "Harakatlanishga ruxsat",
                "B": "Harakatlanish taqiqlangan",
                "C": "Ehtiyot bo'lish kerak",
                "D": "Tezlikni oshirish kerak"
            },
            "correct_answer": "B",
            "category": "Svetofor signallari"
        }
    ]
    
    return questions


def import_questions_to_db(db_path='database/bot_data.json'):
    """
    Savollarni ma'lumotlar bazasiga import qilish
    """
    
    # Ma'lumotlar bazasini o'qish yoki yaratish
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "users": {},
            "questions": [],
            "user_progress": {},
            "settings": {}
        }
    
    # Savollarni qo'shish
    questions = create_sample_questions()
    data["questions"] = questions
    
    # Ma'lumotlar bazasini saqlash
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(questions)} ta savol ma'lumotlar bazasiga qo'shildi!")
    print(f"📁 Fayl: {db_path}")


if __name__ == '__main__':
    import_questions_to_db()

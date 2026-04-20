"""
Database manager for YHQ Test Bot
Ma'lumotlar bazasi boshqaruvchisi
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "database/bot_data.json"):
        self.db_path = db_path
        self.data = self._load_database()
    
    def _load_database(self) -> Dict:
        """Ma'lumotlar bazasini yuklash"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._create_default_structure()
        else:
            return self._create_default_structure()
    
    def _create_default_structure(self) -> Dict:
        """Standart ma'lumotlar bazasi tuzilmasi"""
        return {
            "users": {},  # user_id: {device_id, name, registered_at, is_active}
            "questions": [],  # Savollar ro'yxati
            "user_progress": {},  # user_id: {correct, wrong, current_question}
            "settings": {
                "created_at": datetime.now().isoformat()
            }
        }
    
    def save(self):
        """Ma'lumotlar bazasini saqlash"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # ========== FOYDALANUVCHILAR BILAN ISHLASH ==========
    
    def add_user(self, user_id: int, device_id: str, name: str) -> bool:
        """Yangi foydalanuvchi qo'shish"""
        user_id_str = str(user_id)
        if user_id_str in self.data["users"]:
            return False
        
        self.data["users"][user_id_str] = {
            "device_id": device_id,
            "name": name,
            "registered_at": datetime.now().isoformat(),
            "is_active": True
        }
        self.save()
        return True
    
    def remove_user(self, user_id: int) -> bool:
        """Foydalanuvchini o'chirish"""
        user_id_str = str(user_id)
        if user_id_str in self.data["users"]:
            del self.data["users"][user_id_str]
            # Foydalanuvchi progressini ham o'chirish
            if user_id_str in self.data["user_progress"]:
                del self.data["user_progress"][user_id_str]
            self.save()
            return True
        return False
    
    def is_user_authorized(self, user_id: int, device_id: str) -> bool:
        """Foydalanuvchi ruxsat etilganligini tekshirish"""
        user_id_str = str(user_id)
        if user_id_str not in self.data["users"]:
            return False
        
        user = self.data["users"][user_id_str]
        return user.get("is_active", False) and user.get("device_id") == device_id
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchi ma'lumotlarini olish"""
        return self.data["users"].get(str(user_id))
    
    def get_all_users(self) -> List[Dict]:
        """Barcha foydalanuvchilar ro'yxati"""
        users = []
        for user_id, user_data in self.data["users"].items():
            users.append({
                "user_id": int(user_id),
                **user_data
            })
        return users
    
    def activate_user(self, user_id: int) -> bool:
        """Foydalanuvchini faollashtirish"""
        user_id_str = str(user_id)
        if user_id_str in self.data["users"]:
            self.data["users"][user_id_str]["is_active"] = True
            self.save()
            return True
        return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """Foydalanuvchini o'chirish (deaktivatsiya)"""
        user_id_str = str(user_id)
        if user_id_str in self.data["users"]:
            self.data["users"][user_id_str]["is_active"] = False
            self.save()
            return True
        return False
    
    # ========== SAVOLLAR BILAN ISHLASH ==========
    
    def add_question(self, question_data: Dict) -> int:
        """Yangi savol qo'shish"""
        question_id = len(self.data["questions"]) + 1
        question_data["id"] = question_id
        question_data["created_at"] = datetime.now().isoformat()
        self.data["questions"].append(question_data)
        self.save()
        return question_id
    
    def remove_question(self, question_id: int) -> bool:
        """Savolni o'chirish"""
        for i, q in enumerate(self.data["questions"]):
            if q["id"] == question_id:
                self.data["questions"].pop(i)
                self.save()
                return True
        return False
    
    def get_question(self, question_id: int) -> Optional[Dict]:
        """Bitta savolni olish"""
        for q in self.data["questions"]:
            if q["id"] == question_id:
                return q
        return None
    
    def get_all_questions(self) -> List[Dict]:
        """Barcha savollar"""
        return self.data["questions"]
    
    def get_questions_count(self) -> int:
        """Savollar sonini olish"""
        return len(self.data["questions"])
    
    def update_question(self, question_id: int, question_data: Dict) -> bool:
        """Savolni yangilash"""
        for i, q in enumerate(self.data["questions"]):
            if q["id"] == question_id:
                question_data["id"] = question_id
                question_data["updated_at"] = datetime.now().isoformat()
                self.data["questions"][i] = question_data
                self.save()
                return True
        return False
    
    # ========== FOYDALANUVCHI PROGRESSI ==========
    
    def init_user_progress(self, user_id: int):
        """Foydalanuvchi progressini boshlash"""
        user_id_str = str(user_id)
        if user_id_str not in self.data["user_progress"]:
            self.data["user_progress"][user_id_str] = {
                "correct": 0,
                "wrong": 0,
                "current_question": 0,
                "answered_questions": [],
                "started_at": datetime.now().isoformat()
            }
            self.save()
    
    def get_user_progress(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchi progressini olish"""
        return self.data["user_progress"].get(str(user_id))
    
    def update_user_progress(self, user_id: int, is_correct: bool, question_id: int):
        """Foydalanuvchi progressini yangilash"""
        user_id_str = str(user_id)
        if user_id_str not in self.data["user_progress"]:
            self.init_user_progress(user_id)
        
        progress = self.data["user_progress"][user_id_str]
        
        if is_correct:
            progress["correct"] += 1
        else:
            progress["wrong"] += 1
        
        if question_id not in progress["answered_questions"]:
            progress["answered_questions"].append(question_id)
        
        progress["current_question"] = question_id
        progress["last_activity"] = datetime.now().isoformat()
        
        self.save()
    
    def reset_user_progress(self, user_id: int):
        """Foydalanuvchi progressini qayta boshlash"""
        user_id_str = str(user_id)
        if user_id_str in self.data["user_progress"]:
            del self.data["user_progress"][user_id_str]
            self.init_user_progress(user_id)
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Foydalanuvchi statistikasi"""
        progress = self.get_user_progress(user_id)
        if not progress:
            return {
                "total": 0,
                "correct": 0,
                "wrong": 0,
                "percentage": 0
            }
        
        total = progress["correct"] + progress["wrong"]
        percentage = (progress["correct"] / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "correct": progress["correct"],
            "wrong": progress["wrong"],
            "percentage": round(percentage, 2)
        }

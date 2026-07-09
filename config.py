# config.py — ระบบตั้งค่าและรหัสความปลอดภัย
# เจ้าของกรรมสิทธิ์: ธันวา ภูปิงบุตร

import os
from cryptography.fernet import Fernet

# === รหัสล็อคหลัก — ซ่อน ไม่โชว์ในโค้ดสาธารณะ ===
_MASTER_LOCK = os.getenv("LOADAI_MASTER_LOCK", "hidden_encrypted_value")
_VERIFY_KEY = Fernet(_MASTER_LOCK).encrypt(b"3DLoadAI244")

def verify_system_access(input_secret: str) -> bool:
    """ตรวจสอบรหัส — ไม่เปิดเผยรหัสจริง"""
    try:
        return Fernet(_MASTER_LOCK).decrypt(_VERIFY_KEY).decode() == input_secret
    except:
        return False

# === การตั้งค่าระบบ ===
class Config:
    SYSTEM_NAME = "3D LoadAI"
    VERSION = "1.0.0"
    OWNER = "ธันวา ภูปิงบุตร"
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8080))
    
    # คีย์ API ภายนอก — อ่านจากไฟล์ลับ ไม่ยัดลงโค้ด
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # จำกัดการเข้าถึง API
    API_RATE_LIMIT = "100/minute"


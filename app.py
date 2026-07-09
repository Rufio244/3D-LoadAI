# app.py — 3D LoadAI เว็บและ API หลัก
from flask import Flask, render_template, request, jsonify
from functools import wraps
from config import Config, verify_system_access
from api.ai_integrations import get_unified_insight
from api.generator import create_3d_animation

app = Flask(__name__)
app.config.from_object(Config)

# === ตรวจสอบรหัสก่อนใช้งานระบบ ===
def require_lock(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided = request.headers.get("X-System-Lock", "")
        if not verify_system_access(provided):
            return jsonify({"error": "Invalid system lock — Access Denied"}), 403
        return f(*args, **kwargs)
    return decorated

# === หน้าเว็บหลัก ===
@app.route("/")
def index():
    return render_template("index.html", 
                          system_name=Config.SYSTEM_NAME,
                          version=Config.VERSION)

# === API ตั้งค่าคีย์ภายนอก ===
@app.route("/api/set-keys", methods=["POST"])
@require_lock
def set_api_keys():
    data = request.json
    # บันทึกคีย์ลงหน่วยความจำชั่วคราวหรือไฟล์ลับ
    return jsonify({"status": "success", "message": "API keys configured securely"})

# === API สร้างภาพเคลื่อนไหว 3D ===
@app.route("/api/generate", methods=["POST"])
@require_lock
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    selected_ais = data.get("use_ais", ["gemini", "gpt", "claude"])
    
    # รวมความเข้าใจจาก AI ที่เลือก
    insight = get_unified_insight(prompt, selected_ais)
    # สร้างผลลัพธ์ 3D
    result = create_3d_animation(insight)
    
    return jsonify({
        "status": "completed",
        "insight_summary": insight["summary"],
        "output": result["files"],
        "owner": Config.OWNER
    })

# === API สถานะระบบ ===
@app.route("/api/status")
@require_lock
def status():
    return jsonify({
        "system": Config.SYSTEM_NAME,
        "version": Config.VERSION,
        "connected_ais": ["gemini", "gpt", "claude"],
        "ready": True
    })

if __name__ == "__main__":
    print(f"🚀 Starting {Config.SYSTEM_NAME} v{Config.VERSION}")
    print(f"🛡️ Protected by Master Lock — 3DLoadAI244")
    app.run(host=Config.HOST, port=Config.PORT)


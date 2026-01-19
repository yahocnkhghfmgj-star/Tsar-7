from flask import Flask, request, jsonify
import os
import telebot
from datetime import datetime

# 🔑 ضع توكن البوت هنا (احصل عليه من @BotFather)
BOT_TOKEN = "8303404858:AAE2wAmDd17zZ7MDoQ-4Gu9DH3zqETaFaUk"
# تأكد من اسم تطبيقك في Render
WEBHOOK_URL = f"https://tsar-7-5.onrender.com/{BOT_TOKEN}"

# إنشاء البوت والتطبيق
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 📱 الصفحة الرئيسية
@app.route("/")
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>✅ البوت يعمل</title>
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 100px;
                font-family: 'Arial', sans-serif;
            }}
            .status {{
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                margin: 30px auto;
                width: 80%;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .btn {{
                background: linear-gradient(45deg, #4CAF50, #8BC34A);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 50px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
            }}
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            }}
        </style>
    </head>
    <body>
        <h1>🤖 بوت تليجرام يعمل بنجاح</h1>
        <div class="status">
            <p>🟢 <strong>الحالة: نشط</strong></p>
            <p>🔗 <strong>الرابط:</strong> https://tsar-7-3.onrender.com</p>
            <p>🕐 <strong>الوقت:</strong> {current_time}</p>
            <p>🤖 <strong>البوت:</strong> Telegram Bot</p>
            <p>🚀 <strong>المنفذ:</strong> {os.environ.get('PORT', 10000)}</p>
        </div>
        <a href="/setwebhook" class="btn">✅ تفعيل البوت الآن</a>
        <a href="/test" class="btn">📡 اختبار البوت</a>
        <a href="/health" class="btn">❤️ التحقق من الصحة</a>
        <p style="margin-top: 30px;">بعد التفعيل، أرسل <code>/start</code> للبوت في تليجرام</p>
    </body>
    </html>
    """

# 🔗 تفعيل البوت
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    try:
        bot.remove_webhook()
        success = bot.set_webhook(url=WEBHOOK_URL)
        if success:
            return f'''
            <div style="background:linear-gradient(135deg, #4CAF50, #2E7D32);color:white;padding:50px;text-align:center;border-radius:15px;">
                <h1>✅ تم تفعيل البوت بنجاح!</h1>
                <p>البوت جاهز لاستقبال الرسائل</p>
                <p>🔗 <strong>{WEBHOOK_URL}</strong></p>
                <p>📊 <strong>الحالة:</strong> Webhook مفعل</p>
                <p><a href="/" style="background:white;color:green;padding:10px 20px;border-radius:25px;text-decoration:none;margin-top:20px;display:inline-block;">العودة للصفحة الرئيسية</a></p>
            </div>
            '''
        else:
            return "<h1>❌ فشل في تفعيل Webhook</h1>"
    except Exception as e:
        return f"<h1>❌ خطأ: {str(e)}</h1>"

# 📨 استقبال رسائل البوت
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 🧪 صفحة اختبار
@app.route("/test")
def test():
    return jsonify({
        "status": "active",
        "bot": "telegram",
        "webhook": WEBHOOK_URL,
        "webhook_set": bot.get_webhook_info().url if hasattr(bot, 'get_webhook_info') else "غير معروف",
        "time": datetime.now().isoformat(),
        "port": os.environ.get("PORT", 10000),
        "host": os.environ.get("HOST", "0.0.0.0")
    })

# ❤️ صفحة التحقق من الصحة
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "telegram-bot-webhook"
    })

# 🎯 أوامر البوت
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(message, f"🎉 أهلاً {message.from_user.first_name}!\n✅ البوت يعمل على Render\n🔗 الموقع: https://tsar-7-3.onrender.com\n📅 الوقت: {datetime.now().strftime('%H:%M:%S')}")

@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.reply_to(message, "🆘 الأوامر المتاحة:\n/start - بدء التشغيل\n/help - المساعدة\n/info - معلومات\n\nأرسل أي نص وسأرد عليك!")

@bot.message_handler(commands=["info"])
def handle_info(message):
    bot.reply_to(message, f"📊 معلومات البوت:\n👤 اسمك: {message.from_user.first_name}\n🆔 هويتك: {message.from_user.id}\n🤖 حالة البوت: نشط\n🖥️ الخادم: Render")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"📨 تلقيت: {message.text}\n\n👤 من: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}")

# ⚡ تشغيل التطبيق
if __name__ == "__main__":
    print("="*50)
    print("🚀 بدأ تشغيل البوت...")
    print(f"🔗 ويب هوك: {WEBHOOK_URL}")
    
    # الحصول على المنفذ من متغير البيئة
    port = int(os.environ.get("PORT", 10000))
    print(f"🔌 المنفذ المستخدم: {port}")
    
    # محاولة تفعيل webhook (اختياري)
    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=WEBHOOK_URL, timeout=60)
        print("✅ تم محاولة تفعيل Webhook تلقائياً")
        print(f"ℹ️ معلومات Webhook: {bot.get_webhook_info()}")
    except Exception as e:
        print(f"⚠️ تحذير (Webhook): {e}")
    
    # تشغيل التطبيق
    print(f"🌐 بدأ التشغيل على {os.environ.get('HOST', '0.0.0.0')}:{port}")
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=port,
        debug=False,
        threaded=True
    )
    print("="*50)
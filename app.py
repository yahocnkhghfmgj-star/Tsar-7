from flask import Flask, request, jsonify
import os
import telebot
from datetime import datetime

# 🔑 ضع توكن البوت هنا (احصل عليه من @BotFather)
BOT_TOKEN = "8303404858:AAE2wAmDd17zZ7MDoQ-4Gu9DH3zqETaFaUk"
WEBHOOK_URL = f"https://tsar-7-3.onrender.com/{BOT_TOKEN}"

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
                background: #000;
                color: #0f0;
                text-align: center;
                padding: 100px;
                font-family: Arial;
            }}
            .status {{
                background: #111;
                padding: 20px;
                margin: 20px auto;
                width: 80%;
                border: 2px solid #0f0;
            }}
            .btn {{
                background: #0f0;
                color: #000;
                padding: 15px 30px;
                text-decoration: none;
                font-weight: bold;
                border-radius: 5px;
                display: inline-block;
                margin: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>🤖 بوت تليجرام يعمل</h1>
        <div class="status">
            <p>🟢 <strong>الحالة: نشط</strong></p>
            <p>🔗 <strong>الرابط:</strong> https://tsar-7-3.onrender.com</p>
            <p>🕐 <strong>الوقت:</strong> {current_time}</p>
            <p>🤖 <strong>البوت:</strong> Telegram Bot</p>
        </div>
        <a href="/setwebhook" class="btn">✅ تفعيل البوت الآن</a>
        <a href="/test" class="btn">📡 اختبار البوت</a>
        <p>بعد التفعيل، أرسل <code>/start</code> للبوت في تليجرام</p>
    </body>
    </html>
    """

# 🔗 تفعيل البوت
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        return f'''
        <div style="background:green;color:white;padding:50px;text-align:center">
            <h1>✅ تم تفعيل البوت!</h1>
            <p>البوت جاهز لاستقبال الرسائل</p>
            <p>🔗 {WEBHOOK_URL}</p>
            <p><a href="/" style="color:yellow">العودة للصفحة الرئيسية</a></p>
        </div>
        '''
    except Exception as e:
        return f"<h1>❌ خطأ: {str(e)}</h1>"

# 📨 استقبال رسائل البوت
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return "ok", 200
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return "error", 500

# 🧪 صفحة اختبار
@app.route("/test")
def test():
    return jsonify({
        "status": "active",
        "bot": "telegram",
        "webhook": WEBHOOK_URL,
        "time": datetime.now().isoformat()
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
    
    # تفعيل البوت تلقائياً
    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        print("✅ تم تفعيل البوت تلقائياً")
    except Exception as e:
        print(f"⚠️ تحذير: {e}")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
    print("="*50)
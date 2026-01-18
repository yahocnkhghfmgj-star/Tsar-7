from flask import Flask, jsonify, request
import time
import os
import telebot
from datetime import datetime

# ============ إعدادات البوت ============
TOKEN = "8303404858:AAE2wAmDd17zZ7MDoQ-4Gu9DH3zqETaFaUk"  # ⚠️ استبدل هذا بالتوكن الحقيقي
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ============ الصفحة الرئيسية ============
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✅ تم الحل | Render</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            max-width: 90%;
            width: 600px;
        }
        h1 {
            color: #4CAF50;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .success {
            font-size: 5em;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .status {
            background: #333;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: right;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✅</div>
        <h1>تم حل المشكلة بنجاح!</h1>
        <p>التطبيق + البوت يعملان الآن على Render</p>
        
        <div class="status">
            <p><strong>الحالة:</strong> <span style="color:#4CAF50">نشط ✅</span></p>
            <p><strong>الخادم:</strong> Render Web Service</p>
            <p><strong>الوقت:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p><strong>الذاكرة:</strong> """ + str(os.getpid()) + """</p>
        </div>
        
        <p>🔗 <a href="/setwebhook" style="color:yellow">اضغط هنا لتفعيل البوت</a></p>
    </div>
</body>
</html>
"""

# ============ صفحات المساعدة ============
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "tsar-7-3",
        "timestamp": time.time(),
        "message": "✅ النظام يعمل بشكل صحيح"
    })

@app.route('/setwebhook')
def set_webhook():
    try:
        webhook_url = f"https://tsar-7-3.onrender.com/{TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        return f"""
        <html>
        <body style="background:green;color:white;text-align:center;padding:100px">
            <h1>✅ تم ربط المسودة بنجاح!</h1>
            <p>عنوان الويب هوك: {webhook_url}</p>
            <p>⏱️ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>❌ خطأ: {str(e)}</h1>"

# ============ ويب هوك البوت ============
@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'ERROR', 500

# ============ أوامر البوت ============
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"🎉 مرحباً! البوت يعمل على Render\n🔗 الموقع: https://tsar-7-3.onrender.com")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"📨: {message.text}")

# ============ تشغيل التطبيق ============
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    
    # تعيين ويب هوك تلقائياً
    if TOKEN != "ضع_توكن_البوت_هنا":
        webhook_url = f"https://tsar-7-3.onrender.com/{TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"✅ تم تعيين ويب هوك: {webhook_url}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
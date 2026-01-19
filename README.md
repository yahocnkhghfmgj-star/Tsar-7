import os
from flask import Flask, request, jsonify
import telebot
from datetime import datetime
import json

# 🔐 التوكن (تم إضافته مباشرة للإختبار)
BOT_TOKEN = "8303404858:AAEuChfUBXoZtvb1dek9oIU7_0nByin8Cpo"

# 🔗 Webhook URL ثابت
WEBHOOK_URL = "https://tsar-7-6.onrender.com"

# إنشاء التطبيق والبوت
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 📱 الصفحة الرئيسية
@app.route("/")
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot_info = get_bot_info()
    
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>✅ بوت تليجرام - tsar-7-5</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                background: linear-gradient(135deg, #1a237e, #4a148c);
                color: white;
                font-family: 'Cairo', sans-serif;
                min-height: 100vh;
                padding: 20px;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            header {{
                text-align: center;
                margin-bottom: 40px;
                padding: 30px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                color: #4fc3f7;
            }}
            
            .subtitle {{
                font-size: 1.2rem;
                opacity: 0.9;
                margin-bottom: 20px;
            }}
            
            .status-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .status-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #4fc3f7;
            }}
            
            .status-card h3 {{
                color: #4fc3f7;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .status-card p {{
                margin: 8px 0;
                font-size: 1rem;
            }}
            
            .info-badge {{
                display: inline-block;
                background: rgba(79, 195, 247, 0.2);
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 0.9rem;
                margin-left: 10px;
            }}
            
            .buttons {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
                margin: 30px 0;
            }}
            
            .btn {{
                background: linear-gradient(45deg, #4fc3f7, #2979ff);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s;
                border: none;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }}
            
            .btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            }}
            
            .btn-success {{
                background: linear-gradient(45deg, #00c853, #64dd17);
            }}
            
            .btn-warning {{
                background: linear-gradient(45deg, #ff9100, #ffab00);
            }}
            
            .btn-info {{
                background: linear-gradient(45deg, #00b0ff, #0091ea);
            }}
            
            .instructions {{
                background: rgba(0, 0, 0, 0.3);
                padding: 25px;
                border-radius: 15px;
                margin-top: 40px;
            }}
            
            .instructions h3 {{
                color: #4fc3f7;
                margin-bottom: 15px;
            }}
            
            .instructions ol {{
                margin-right: 20px;
            }}
            
            .instructions li {{
                margin: 10px 0;
            }}
            
            code {{
                background: rgba(0, 0, 0, 0.5);
                padding: 2px 8px;
                border-radius: 5px;
                font-family: monospace;
                direction: ltr;
                display: inline-block;
            }}
            
            footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                opacity: 0.8;
                font-size: 0.9rem;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 10px;
                }}
                
                h1 {{
                    font-size: 2rem;
                }}
                
                .btn {{
                    width: 100%;
                    justify-content: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 بوت تليجرام يعمل بنجاح</h1>
                <p class="subtitle">تم تجهيز البوت بالكامل وجاهز للاستخدام</p>
            </header>
            
            <div class="status-grid">
                <div class="status-card">
                    <h3>📊 حالة النظام</h3>
                    <p><strong>التطبيق:</strong> tsar-7-5 <span class="info-badge">نشط</span></p>
                    <p><strong>الوقت:</strong> {current_time}</p>
                    <p><strong>الخادم:</strong> Render</p>
                    <p><strong>الحالة:</strong> <span style="color: #4fc3f7;">●</span> جاهز</p>
                </div>
                
                <div class="status-card">
                    <h3>🤖 معلومات البوت</h3>
                    <p><strong>التوكن:</strong> <span style="font-family: monospace; font-size: 0.9rem;">{BOT_TOKEN[:15]}...</span></p>
                    <p><strong>Webhook:</strong> <span style="font-family: monospace; font-size: 0.9rem;">{WEBHOOK_URL}</span></p>
                    <p><strong>الإصدار:</strong> v1.0</p>
                </div>
                
                <div class="status-card">
                    <h3>⚡ الإجراءات السريعة</h3>
                    <p>🔗 الواجهة: <code>https://tsar-7-5.onrender.com</code></p>
                    <p>📡 اختبار API: <code>/test</code></p>
                    <p>❤️ التحقق: <code>/health</code></p>
                    <p>🔧 تفعيل: <code>/setwebhook</code></p>
                </div>
            </div>
            
            <div class="buttons">
                <a href="/setwebhook" class="btn btn-success">
                    <span>✅</span> تفعيل البوت الآن
                </a>
                <a href="/test" class="btn">
                    <span>📡</span> اختبار البوت
                </a>
                <a href="/health" class="btn btn-info">
                    <span>❤️</span> التحقق من الصحة
                </a>
                <a href="/checkwebhook" class="btn btn-warning">
                    <span>🔍</span> فحص Webhook
                </a>
            </div>
            
            <div class="instructions">
                <h3>📋 خطوات التشغيل</h3>
                <ol>
                    <li>انقر على زر "تفعيل البوت الآن"</li>
                    <li>انتظر رسالة التأكيد (يجب أن ترى ✅)</li>
                    <li>افتح Telegram وابحث عن البوت</li>
                    <li>أرسل <code>/start</code> للبدء</li>
                    <li>أرسل <code>/help</code> لرؤية الأوامر</li>
                </ol>
                
                <p style="margin-top: 15px; color: #4fc3f7;">
                    <strong>ملاحظة:</strong> البوت مجهز بالتوكن التالي: 
                    <code style="background: rgba(79, 195, 247, 0.3);">{BOT_TOKEN[:10]}...</code>
                </p>
            </div>
            
            <footer>
                <p>تم التطوير باستخدام Flask + pyTelegramBotAPI</p>
                <p>© 2024 - تطبيق tsar-7-5 | جميع الحقوق محفوظة</p>
            </footer>
        </div>
    </body>
    </html>
    """

# 🔧 دالة للحصول على معلومات البوت
def get_bot_info():
    try:
        bot_info = bot.get_me()
        return {
            "id": bot_info.id,
            "username": bot_info.username,
            "first_name": bot_info.first_name
        }
    except:
        return {"error": "لا يمكن الاتصال بالبوت"}

# 🔗 تفعيل البوت
@app.route("/setwebhook", methods=["GET"])
def set_webhook():
    try:
        bot.remove_webhook()
        success = bot.set_webhook(
            url=WEBHOOK_URL,
            max_connections=50,
            allowed_updates=["message", "callback_query", "inline_query"]
        )
        
        if success:
            return f'''
            <div style="background:linear-gradient(135deg, #00c853, #64dd17);color:white;padding:50px;text-align:center;border-radius:20px;margin:50px;">
                <h1 style="font-size:2.5rem;margin-bottom:20px;">✅ تم تفعيل البوت بنجاح!</h1>
                <p style="font-size:1.2rem;margin:15px 0;">البوت جاهز لاستقبال الرسائل</p>
                <div style="background:rgba(255,255,255,0.2);padding:20px;border-radius:10px;margin:20px;text-align:left;direction:ltr;">
                    <p><strong>🔗 Webhook URL:</strong></p>
                    <code style="background:rgba(0,0,0,0.5);padding:10px;display:block;border-radius:5px;">{WEBHOOK_URL}</code>
                </div>
                <p style="margin:20px;">📊 يمكنك الآن إرسال <code>/start</code> للبوت في Telegram</p>
                <a href="/" style="background:white;color:#00c853;padding:15px 30px;border-radius:50px;text-decoration:none;font-weight:bold;display:inline-block;margin-top:20px;">
                    العودة للصفحة الرئيسية
                </a>
            </div>
            '''
        else:
            return "<h1 style='text-align:center;color:red;margin:50px;'>❌ فشل في تفعيل Webhook</h1>"
    except Exception as e:
        return f"<h1 style='text-align:center;color:red;margin:50px;'>❌ خطأ: {str(e)}</h1>"

# 📨 استقبال رسائل البوت
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return jsonify({"status": "success", "message": "تم استلام الرسالة"}), 200
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 🧪 صفحة اختبار
@app.route("/test")
def test():
    try:
        bot_info = get_bot_info()
        return jsonify({
            "status": "active",
            "application": "tsar-7-5",
            "bot_info": bot_info,
            "webhook": WEBHOOK_URL,
            "webhook_info": bot.get_webhook_info().url if hasattr(bot, 'get_webhook_info') else "غير معروف",
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": os.sys.version,
                "flask_version": "2.3.3",
                "telebot_version": "4.14.0"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ❤️ صفحة التحقق من الصحة
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "tsar-7-5",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "services": {
            "web_server": "active",
            "telegram_bot": "connected" if BOT_TOKEN else "disconnected",
            "webhook": "configured"
        }
    })

# 🔍 فحص حالة Webhook
@app.route("/checkwebhook")
def check_webhook():
    try:
        webhook_info = bot.get_webhook_info()
        return jsonify({
            "status": "success",
            "webhook_info": {
                "url": webhook_info.url,
                "has_custom_certificate": webhook_info.has_custom_certificate,
                "pending_update_count": webhook_info.pending_update_count,
                "max_connections": webhook_info.max_connections,
                "allowed_updates": webhook_info.allowed_updates
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🎯 أوامر البوت
@bot.message_handler(commands=["start"])
def handle_start(message):
    welcome_text = f"""
🎉 أهلاً {message.from_user.first_name}!

✅ البوت يعمل بنجاح على خادم Render
🔗 التطبيق: tsar-7-5
📅 الوقت: {datetime.now().strftime('%H:%M:%S')}
👤 معرفك: {message.from_user.id}

📝 الأوامر المتاحة:
/start - بدء التشغيل
/help - المساعدة
/info - معلومات البوت

💬 أرسل أي نص وسأرد عليك!
"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=["help"])
def handle_help(message):
    help_text = """
🆘 **قائمة الأوامر:**

/start - بدء التشغيل وعرض الترحيب
/help - عرض هذه الرسالة
/info - معلومات عن البوت والخادم

🔧 **مميزات البوت:**
- الرد على جميع الرسائل النصية
- عرض معلومات المستخدم
- العمل على خادم Render
- واجهة ويب متكاملة

💡 **نصائح:**
- البوت يعمل 24/7
- يمكنك إرسال أي نص
- الصفحة الرئيسية: https://tsar-7-5.onrender.com
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=["info"])
def handle_info(message):
    info_text = f"""
📊 **معلومات البوت:**

👤 **المستخدم:**
- الاسم: {message.from_user.first_name}
- المعرف: {message.from_user.id}
- اليوزر: @{message.from_user.username if message.from_user.username else 'غير متوفر'}

🤖 **البوت:**
- الحالة: نشط ✅
- الخادم: Render
- التطبيق: tsar-7-5
- الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🌐 **الروابط:**
- الصفحة: https://tsar-7-5.onrender.com
- الاختبار: https://tsar-7-5.onrender.com/test
- الصحة: https://tsar-7-5.onrender.com/health
"""
    bot.reply_to(message, info_text)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    response = f"""
📨 **تم استلام رسالتك:**

{message.text}

👤 **من:** {message.from_user.first_name}
🆔 **ID:** {message.from_user.id}
🕐 **الوقت:** {datetime.now().strftime('%H:%M:%S')}

💬 يمكنك استخدام /help لرؤية جميع الأوامر
"""
    bot.reply_to(message, response)

# ⚡ تشغيل التطبيق
if __name__ == "__main__":
    print("="*60)
    print("🚀 بدأ تشغيل بوت تليجرام...")
    print(f"🤖 البوت: {BOT_TOKEN[:15]}...")
    print(f"🔗 Webhook: {WEBHOOK_URL}")
    print(f"🌐 التطبيق: tsar-7-5")
    print("="*60)
    
    # محاولة تفعيل Webhook تلقائياً
    try:
        bot.remove_webhook()
        import time
        time.sleep(2)
        bot.set_webhook(url=WEBHOOK_URL)
        print("✅ تم تفعيل Webhook تلقائياً")
    except Exception as e:
        print(f"⚠️ تحذير: {e}")
    
    # تشغيل التطبيق
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True
    )

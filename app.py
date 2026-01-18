from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

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
        <p>التطبيق يعمل الآن على Render بدون أخطاء</p>
        
        <div class="status">
            <p><strong>الحالة:</strong> <span style="color:#4CAF50">نشط ✅</span></p>
            <p><strong>الخادم:</strong> Render Web Service</p>
            <p><strong>الوقت:</strong> """ + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p><strong>الذاكرة:</strong> """ + str(os.getpid()) + """</p>
        </div>
        
        <p>يمكنك الآن إضافة الميزات التي تريدها بدون مشاكل</p>
    </div>
</body>
</html>
"""

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "ali10_1",
        "timestamp": time.time(),
        "message": "✅ النظام يعمل بشكل صحيح"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "code": 200,
        "message": "OK",
        "data": {
            "version": "1.0.0",
            "uptime": time.time(),
            "environment": "production"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
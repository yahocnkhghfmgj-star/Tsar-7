from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>✅ الموقع يعمل</title>
    <style>
        body {
            background: black;
            color: #0f0;
            text-align: center;
            padding: 100px;
            font-family: Arial;
        }
        h1 { color: #0f0; }
        .box {
            background: #111;
            padding: 20px;
            margin: 20px auto;
            width: 80%;
            border: 2px solid #0f0;
        }
    </style>
</head>
<body>
    <h1>✅ تم النشر بنجاح</h1>
    <div class="box">
        <p>الحالة: <strong style="color:#0f0">نشط</strong></p>
        <p>الوقت: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        <p>الخادم: Render</p>
    </div>
    <p>التطبيق يعمل بدون أخطاء ✅</p>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
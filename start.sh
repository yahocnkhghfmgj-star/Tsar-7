#!/bin/bash
# Script لبدء التشغيل على Render
echo "🚀 بدأ تشغيل البوت..."

# انتظر قليلاً قبل البدء
sleep 2

# استخدم gunicorn لتشغيل التطبيق
gunicorn --bind 0.0.0.0:$PORT --workers=2 --threads=4 --timeout=120 app:app
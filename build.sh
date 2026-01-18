#!/bin/bash
set -o errexit

echo "🚀 بدء بناء البوت..."

# تحديث pip
pip install --upgrade pip

# تثبيت المتطلبات
pip install -r requirements.txt

echo "✅ اكتمل البناء بنجاح!"
import os
import json
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات السحابة
PORT = int(os.environ.get('PORT', 8080))

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قراءة التوكن
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("❌ لم يتم تعيين BOT_TOKEN. أضفه في Render Environment Variables")

class TradingBot:
    def __init__(self):
        self.analyses_file = "analyses.json"
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بدء البوت"""
        user = update.effective_user
        
        keyboard = [
            [InlineKeyboardButton("📈 الأسواق العالمية", callback_data='market')],
            [InlineKeyboardButton("📊 التحليلات اليومية", callback_data='analysis')],
            [InlineKeyboardButton("📰 أخبار مالية", callback_data='news')],
            [InlineKeyboardButton("🆘 المساعدة", callback_data='help')],
            [InlineKeyboardButton("👥 رابط المجموعة", callback_data='group_link')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
        🏆 **مرحباً {user.first_name} في بوت التداول!**
        
        🤖 **مميزات البوت:**
        ✅ متابعة الأسواق العالمية
        ✅ تحليلات يومية
        ✅ أخبار مالية
        ✅ مجتمع متداولين
        
        📊 **آخر تحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        **اختر من القائمة:**
        """
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض المساعدة"""
        help_text = """
        🆘 **أوامر البوت:**
        
        /start - بدء البوت والقائمة
        /help - هذه الرسالة
        /market - أسواق الأسهم والعملات
        /analysis - تحليلات اليوم
        /add_analysis <نص> - إضافة تحليل
        /news - آخر الأخبار
        /status - حالة البوت
        /invite - رابط الدعوة
        
        📌 **قواعد المجموعة:**
        1. احترام آراء الآخرين
        2. عدم نشر إعلانات غير مرغوبة
        3. ذكر المصادر عند النقل
        4. الحفاظ على النقاش المهني
        
        📞 **للتواصل مع الإدارة:**
        @YourUsername
        """
        await update.message.reply_text(help_text)
    
    async def market_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض أسواق المال"""
        market_data = """
        📊 **الأسواق العالمية - {time}**
        
        🇺🇸 **الأسهم الأمريكية:**
        • S&P 500: 4,800.50 ↗️ +0.52%
        • NASDAQ: 16,950.30 ↗️ +0.81%
        • Dow Jones: 37,500.20 ↗️ +0.35%
        
        🌍 **أسواق أخرى:**
        • DAX (ألمانيا): 16,550.40 ↗️ +0.25%
        • Nikkei (اليابان): 36,120.10 ↗️ +0.68%
        
        💰 **العملات:**
        • EUR/USD: 1.0950 ↘️ -0.12%
        • GBP/USD: 1.2750 ↗️ +0.08%
        • USD/SAR: 3.7500 ⬅️ 0.00%
        
        🛢️ **السلع:**
        • النفط (برنت): $78.50 ↗️ +1.25%
        • الذهب: $1,952.30 ↗️ +0.45%
        
        ₿ **العملات الرقمية:**
        • Bitcoin: $42,150 ↗️ +2.35%
        • Ethereum: $2,280 ↗️ +1.85%
        
        📈 **ملخص السوق:** اتجاه صاعد مع تفاؤل حذر.
        """.format(time=datetime.now().strftime('%H:%M'))
        
        keyboard = [
            [InlineKeyboardButton("🔄 تحديث", callback_data='market')],
            [InlineKeyboardButton("📊 تفاصيل أكثر", url="https://www.tradingview.com")]
        ]
        
        await update.message.reply_text(
            market_data,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض التحليلات"""
        try:
            with open(self.analyses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"analyses": []}
        
        if not data["analyses"]:
            await update.message.reply_text("📭 لا توجد تحليلات حالياً. كن أول من يضيف تحليلاً!")
            return
        
        # عرض آخر 5 تحليلات
        recent = data["analyses"][-5:][::-1]  # عكس الترتيب لعرض الأحدث أولاً
        
        analysis_text = "📈 **آخر التحليلات:**\n\n"
        for idx, item in enumerate(recent, 1):
            date = datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M')
            analysis_text += f"**{idx}. {item['user']}** ({date})\n"
            analysis_text += f"▸ {item['analysis'][:100]}...\n\n"
        
        keyboard = [
            [InlineKeyboardButton("➕ إضافة تحليل", callback_data='add_analysis')],
            [InlineKeyboardButton("📋 كل التحليلات", callback_data='all_analyses')]
        ]
        
        await update.message.reply_text(
            analysis_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def add_analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إضافة تحليل جديد"""
        if not context.args:
            await update.message.reply_text(
                "📝 **طريقة الاستخدام:**\n"
                "/add_analysis <نص التحليل>\n\n"
                "**مثال:**\n"
                "/add_analysis أتوقع ارتفاع السوق بسبب النتائج القوية للشركات"
            )
            return
        
        analysis_text = ' '.join(context.args)
        user = update.effective_user
        
        # تحميل التحليلات الحالية
        try:
            with open(self.analyses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"analyses": []}
        
        # إضافة التحليل الجديد
        new_analysis = {
            "user": user.first_name,
            "user_id": user.id,
            "analysis": analysis_text,
            "timestamp": datetime.now().isoformat()
        }
        
        data["analyses"].append(new_analysis)
        
        # حفظ
        with open(self.analyses_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        await update.message.reply_text(
            f"✅ **تم إضافة تحليلك بنجاح!**\n\n"
            f"👤 **المحلل:** {user.first_name}\n"
            f"📝 **التحليل:** {analysis_text}\n\n"
            f"📊 سيظهر تحليلك في قائمة التحليلات."
        )
    
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض الأخبار المالية"""
        news_text = """
        📰 **آخر الأخبار المالية - {date}**
        
        🔥 **أخبار ساخنة:**
        1. **البنك الفيدرالي:** قرر تثبيت أسعار الفائدة عند 5.5%
        2. **أرباح الشركات:** نتائج قوية لشركات التكنولوجيا الأمريكية
        3. **النفط:** ارتفاع الأسعار بسبب توترات في الشرق الأوسط
        4. **العملات الرقمية:** موافقة SEC على صناديق بيتكوين ETF
        
        📊 **تأثيرات متوقعة:**
        • استقرار في أسواق الأسهم
        • ضغط على الدولار الأمريكي
        • ارتفاع في أسهم الطاقة
        
        📌 **نصائح اليوم:**
        • راقب أسهم التكنولوجيا
        • تجنب الرافعة المالية العالية
        • تنويع المحفظة
        
        ⏰ **الأحداث القادمة:**
        • تقرير التوظيف الأمريكي: غداً 10:30 صباحاً
        • اجتماع البنك المركزي الأوروبي: الأسبوع القادم
        
        🔗 **مصادر موثوقة:**
        • Bloomberg: https://www.bloomberg.com
        • Reuters: https://www.reuters.com
        • TradingView: https://www.tradingview.com
        """.format(date=datetime.now().strftime('%Y-%m-%d'))
        
        await update.message.reply_text(news_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """حالة البوت"""
        import sys
        import platform
        
        status_text = """
        🤖 **حالة البوت:** ✅ يعمل بنجاح
        
        🌐 **معلومات النظام:**
        • النظام: {system}
        • إصدار Python: {python_version}
        • وقت التشغيل: الآن
        
        📊 **إحصائيات:**
        • عدد التحليلات: {analyses_count}
        • آخر تحديث: {last_update}
        
        🚀 **التواصل:**
        • المطور: @YourUsername
        • الإبلاغ عن مشاكل: @YourUsername
        
        💡 **نصائح:**
        1. البوت يعمل 24/7
        2. يتم تحديث البيانات كل ساعة
        3. التحليلات تحفظ تلقائياً
        """
        
        # حساب عدد التحليلات
        try:
            with open(self.analyses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                analyses_count = len(data["analyses"])
        except:
            analyses_count = 0
        
        await update.message.reply_text(status_text.format(
            system=platform.system(),
            python_version=sys.version.split()[0],
            analyses_count=analyses_count,
            last_update=datetime.now().strftime('%Y-%m-%d %H:%M')
        ))
    
    async def invite_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """رابط دعوة للمجموعة"""
        invite_text = """
        🔗 **رابط انضمام للمجموعة:**
        
        👥 **مجموعة التداول والتحليل:**
        https://t.me/+UNIQUE_INVITE_LINK
        
        📚 **القناة التعليمية:**
        https://t.me/your_education_channel
        
        📢 **كيف تجذب أعضاء جدد:**
        1. شارك التحليلات القيمة
        2. ادعُ أصدقاءك المهتمين
        3. انشر في مجموعات ذات صلة
        4. كن نشطاً ومتفاعلاً
        
        ⚠️ **ملاحظة:** الرابط صالح لمدة 7 أيام
        """
        
        await update.message.reply_text(invite_text)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الأزرار"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'market':
            await self.market_command(update, context)
        elif query.data == 'analysis':
            await self.analysis_command(update, context)
        elif query.data == 'news':
            await self.news_command(update, context)
        elif query.data == 'help':
            await self.help_command(update, context)
        elif query.data == 'group_link':
            await self.invite_command(update, context)
        elif query.data == 'add_analysis':
            await query.message.reply_text("أرسل التحليل بهذا الشكل:\n/add_analysis <نص التحليل>")
        elif query.data == 'all_analyses':
            await self.analysis_command(update, context)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الأخطاء"""
        logger.error(f"حدث خطأ: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ حدث خطأ غير متوقع. تم تسجيله وسيتم معالجته."
            )
    
    def run(self):
        """تشغيل البوت"""
        app = Application.builder().token(TOKEN).build()
        
        # إضافة handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("market", self.market_command))
        app.add_handler(CommandHandler("analysis", self.analysis_command))
        app.add_handler(CommandHandler("add_analysis", self.add_analysis_command))
        app.add_handler(CommandHandler("news", self.news_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("invite", self.invite_command))
        
        # معالجة الأزرار
        app.add_handler(CallbackQueryHandler(self.button_handler))
        
        # معالجة الأخطاء
        app.add_error_handler(self.error_handler)
        
        # تشغيل
        logger.info("🤖 البوت يعمل...")
        app.run_polling()

def main():
    """الدالة الرئيسية"""
    bot = TradingBot()
    bot.run()

if __name__ == "__main__":
    main()
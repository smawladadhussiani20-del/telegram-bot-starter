https://github.com/"smawladadhussiani20-del/telegram-bot-starter/blob/main/bot.py"
# -*- coding: utf-8 -*-
"""
ربات تلگرام آموزشی - خرید از آمازون با تتر برای افغانستان
Tutorial Bot - Amazon with Tether for Afghanistan
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# فعال کردن logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# داده‌های آموزشی
LESSONS = {
    "intro": "🎓 **خوش آمدید به ربات آموزشی تتر و آمازون**\n\nاین ربات برای آموزش کامل خرید از آمازون با تتر برای افغانستان است.\n\nلطفاً یکی از دروس را انتخاب کنید:",
    
    "lesson1": """
📚 **درس ۱: آمازون چیست؟**

آمازون یک فروشگاه آنلاین بسیار بزرگ است که:
✓ محصولات مختلفی فروخته می‌شود
✓ در بسیاری کشورها کار می‌کند
✓ خرید آنلاین و ارسال به خانه

🌍 **نوع‌های آمازون:**
• Amazon.com (آمریکا)
• Amazon.ae (امارات)
• Amazon.co.uk (انگلیس)

برای افغانستان معمولاً از Amazon.com یا Amazon.ae استفاده می‌شود.

💡 **نکته:** آمازون یک سایت معتبر و امن است و میلیون‌ها نفر از آن خرید می‌کنند.
    """,
    
    "lesson2": """
💳 **درس ۲: تتر چیست؟**

تتر (USDT) یک ارز دیجیتال است که:
✓ با دلار آمریکایی برابر است (1 USDT = 1 USD)
✓ می‌تواند به دلار تبدیل شود
✓ به‌صورت آنلاین منتقل می‌شود

🔄 **تتر برای خرید از آمازون:**
1. تتر را خریداری کنید (ریال → USDT)
2. تتر را به دلار تبدیل کنید (USDT → USD)
3. از دلار برای پرداخت در آمازون استفاده کنید

💡 **نکته:** آمازون مستقیماً تتر را قبول نمی‌کند، باید به دلار تبدیل شود.
    """,
    
    "lesson3": """
🛠️ **درس ۳: مراحل خرید از آمازون**

📋 **مرحله ۱: حساب آمازون بسازید**
1. به amazon.com برید
2. Create Account کلیک کنید
3. ایمیل وارد کنید
4. رمز عبور انتخاب کنید
5. نام و آدرس خود را وارد کنید

💳 **مرحله ۲: روش پرداخت**
1. کارت بانکی بین‌المللی یا
2. کارت مجازی یا
3. Payoneer/Wise

📦 **مرحله ۳: انتخاب محصول**
1. محصول را جستجو کنید
2. بررسی قیمت و فروشنده
3. Add to Cart کلیک کنید

✅ **مرحله ۴: پرداخت**
1. Checkout کلیک کنید
2. آدرس تحویل را بررسی کنید
3. روش پرداخت را انتخاب کنید
4. سفارش را تأیید کنید

💡 **نکته:** قبل از پرداخت، همه هزینه‌ها را بررسی کنید.
    """,
    
    "lesson4": """
💰 **درس ۴: کارت مجازی برای آمازون**

کارت مجازی یک کارت دیجیتال است که:
✓ برای پرداخت آنلاین استفاده می‌شود
✓ مثل کارت بانکی عمل می‌کند
✓ برای آمازون مناسب است

📱 **سرویس‌های معتبر:**
1. 2Checkout
2. Stripe
3. PayPal Virtual Card
4. Payoneer

🔒 **نکات امنی:**
• فقط از سایت‌های معتبر استفاده کنید
• هرگز رمز را به کسی ندهید
• هزینه‌ها را قبل از استفاده بررسی کنید

💡 **نکته:** کارت مجازی برای خرید آنلاین بسیار امن است.
    """,
    
    "lesson5": """
🚚 **درس ۵: ارسال به افغانستان**

چون آمازون معمولاً به افغانستان نمی‌فرستد، باید:

📍 **Forwarding Service استفاده کنید:**
1. خدمات ارسال یک آدرس در خارج می‌دهند
2. شما سفارش را به آن آدرس می‌فرستید
3. آنها برای شما به افغانستان می‌فرستند

🌐 **سرویس‌های معتبر:**
• MyUS
• Planet Express
• Shipito

💰 **هزینه‌ها:**
• قیمت محصول
• هزینه ارسال از آمازون
• هزینه forwarding
• ممکن است گمرک اضافی

💡 **نکته:** کل هزینه را قبل از سفارش محاسبه کنید.
    """,
    
    "lesson6": """
⚠️ **درس ۶: اشتباهات رایج**

❌ **این اشتباهات را نکنید:**

1. ❌ آدرس اشتباه وارد کردن
2. ❌ استفاده از کارت نامعتبر
3. ❌ بستن سفارش قبل از بررسی هزینه
4. ❌ خرید از فروشنده‌های مشکوک
5. ❌ نادیده گرفتن هزینه ارسال
6. ❌ استفاده از سایت‌های غیرمعتبر

✅ **راه‌های امن:**
✓ همیشه از سایت رسمی amazon.com استفاده کنید
✓ از فروشنده‌های معتبر خرید کنید
✓ نظرات فروشنده را بخوانید
✓ اولاً یک خرید کوچک انجام دهید

💡 **نکته:** احتیاط بیش از حد بهتر است!
    """,
    
    "lesson7": """
🎯 **درس ۷: خلاصه و خطوات نهایی**

📋 **مراحل خرید از آمازون با تتر:**

1️⃣ تتر خریداری کنید
   → صرافی معتبر (Binance, Nobitex, وغیره)

2️⃣ تتر را به دلار تبدیل کنید
   → Wise, صرافی محلی، یا Payoneer

3️⃣ کارت مجازی تهیه کنید
   → 2Checkout, Stripe, PayPal

4️⃣ حساب آمازون بسازید
   → amazon.com

5️⃣ محصول را انتخاب کنید
   → جستجو، مقایسه قیمت

6️⃣ forwarding service استفاده کنید
   → MyUS, Planet Express

7️⃣ سفارش را تأیید کنید
   → بررسی آدرس و هزینه

8️⃣ کالا را دریافت کنید
   → در افغانستان

💡 **نکته:** کل مسیر حدود ۷-۱۰ روز طول می‌کشد.

❓ **سوالات؟** از من بپرسید!
    """,
    
    "faq": """
❓ **سوالات متداول**

**س: آیا آمازون معتبر است؟**
جـ: بله، آمازون یک سایت جهانی و بسیار معتبر است.

**س: آیا تتر استفاده کردن برای آمازون قانونی است؟**
جـ: بله، تتر قانونی است. اما آمازون مستقیماً تتر را نمی‌پذیرد، باید به دلار تبدیل شود.

**س: هزینه چقدر است؟**
جـ: معمولاً 5-15% اضافه از قیمت محصول برای ارسال و کمیسیون.

**س: چند روز طول می‌کشد؟**
جـ: معمولاً 7-10 روز.

**س: اگر محصول معیوب باشد؟**
جـ: آمازون خریتان را برمی‌گرداند یا تعویض می‌کند.

**س: آیا باید کارت بانکی داشته باشم؟**
جـ: نه، می‌توانید کارت مجازی یا Payoneer استفاده کنید.

**س: اگر سفارش گمشود؟**
جـ: forwarding service مسئول است و باید جبران کند.
    """,
}

# دکمه‌های اصلی
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 درس ۱: آمازون چیست؟", callback_data="lesson1")],
        [InlineKeyboardButton("💳 درس ۲: تتر چیست؟", callback_data="lesson2")],
        [InlineKeyboardButton("🛠️ درس ۳: مراحل خرید", callback_data="lesson3")],
        [InlineKeyboardButton("💰 درس ۴: کارت مجازی", callback_data="lesson4")],
        [InlineKeyboardButton("🚚 درس ۵: ارسال به افغانستان", callback_data="lesson5")],
        [InlineKeyboardButton("⚠️ درس ۶: اشتباهات رایج", callback_data="lesson6")],
        [InlineKeyboardButton("🎯 درس ۷: خلاصه نهایی", callback_data="lesson7")],
        [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq")],
        [InlineKeyboardButton("🔄 دوباره شروع", callback_data="start")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور شروع"""
    user = update.effective_user
    welcome_message = f"""
👋 سلام {user.first_name}!

🎓 **خوش آمدید به ربات آموزشی تتر و آمازون**

این ربات برای آموزش کامل و رایگان خرید از آمازون با تتر برای افغانستان طراحی شده است.

📚 **۷ درس آموزشی:**
1. آمازون چیست؟
2. تتر چیست؟
3. مراحل خرید از آمازون
4. کارت مجازی برای آمازون
5. ارسال به افغانستان
6. اشتباهات رایج
7. خلاصه و خطوات نهایی

❓ همچنین سوالات متداول موجود است.

👇 **لطفاً یکی از دروس را انتخاب کنید:**
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت دکمه‌ها"""
    query = update.callback_query
    await query.answer()
    
    lesson_key = query.data
    
    if lesson_key == "start":
        await query.edit_message_text(
            text=LESSONS["intro"],
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
    elif lesson_key in LESSONS:
        keyboard = [
            [InlineKeyboardButton("◀️ بازگشت به منو", callback_data="start")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=LESSONS[lesson_key],
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            text="❌ درس یافت نشد!",
            reply_markup=get_main_keyboard()
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور کمک"""
    help_text = """
🆘 **راهنمای استفاده:**

/start - شروع و دیدن تمام دروس
/help - این پیام
/contact - تماس با ما

📚 **دروس موجود:**
• درس ۱: آمازون چیست؟
• درس ۲: تتر چیست؟
• درس ۳: مراحل خرید
• درس ۴: کارت مجازی
• درس ۵: ارسال به افغانستان
• درس ۶: اشتباهات رایج
• درس ۷: خلاصه نهایی
• سوالات متداول

💡 **نکته:** برای دیدن دروس، /start را وارد کنید و دکمه‌ها را کلیک کنید.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دستور تماس"""
    contact_text = """
📞 **تماس با ما:**

👤 **نویسنده:** smawladadhussiani20-del
🌐 **GitHub:** https://github.com/smawladadhussiani20-del
📧 **برای تماس:** پیام را در تلگرام بفرستید

💬 **اگر سوال دارید یا به دروس دیگری نیاز دارید، با ما تماس بگیرید.**

❤️ **اگر این ربات مفید بود، لطفاً آن را به دوستان خود معرفی کنید.**
    """
    await update.message.reply_text(contact_text, parse_mode='Markdown')

def main() -> None:
    """شروع ربات"""
    # توکن خود را اینجا وارد کنید
"TOKEN =https://github.com/smawladadhussiani20-del/telegram-bot-starter/blob/main/bot.py"
    # ایجاد Application
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # شروع polling
    application.run_polling()

if __name__ == '__main__':
    main()

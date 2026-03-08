import asyncio
import smtplib
from email.mime.text import MIMEText
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- بياناتك الشخصية (جاهزة) ---
API_ID = 25880715
API_HASH = "0d1e0a5fe75236df18295a0f8b22b458"
BOT_TOKEN = "8650334560:AAFZUZ9Ilgl4OIx5riTB86Mrzo0i2ytsH5w"
# ----------------------------

app = Client("SHALAL_BOT", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# قاعدة بيانات مؤقتة في الرام
db = {}

def main_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 ايميل الدعم", callback_data="set_target"),
         InlineKeyboardButton("➕ اضف ايميلك", callback_data="add_sender")],
        [InlineKeyboardButton("📝 الموضوع", callback_data="set_sub"),
         InlineKeyboardButton("📋 الكليشه", callback_data="set_msg")],
        [InlineKeyboardButton("🔢 عدد الرسائل", callback_data="set_count"),
         InlineKeyboardButton("⏱️ الثواني", callback_data="set_del")],
        [InlineKeyboardButton("🚀 بدء الارسال", callback_data="start_burn")],
        [InlineKeyboardButton("👤 المطور: سالم", url="https://t.me/hlhrI")]
    ])

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    uid = message.from_user.id
    if uid not in db:
        db[uid] = {"target": None, "senders": [], "sub": "No Subject", "msg": "No Message", "count": 10, "delay": 2, "step": None}
    
    await message.reply_text(
        "**مرحباً بك في بوت الشد الخارجي 🚀**\n\nاضبط إعداداتك ثم اضغط بدء الإرسال.\n\n**Dev: @hlhrI**",
        reply_markup=main_markup()
    )

@app.on_callback_query()
async def callbacks(client, query: CallbackQuery):
    uid = query.from_user.id
    data = query.data
    
    if data == "set_target":
        db[uid]["step"] = "target"
        await query.message.edit_text("🎯 أرسل إيميل الدعم المستهدف:")
    elif data == "add_sender":
        db[uid]["step"] = "sender"
        await query.message.edit_text("📧 أرسل إيميلك وباسورد التطبيق بالشكل التالي:\n`email:password`\n\n*ملاحظة: استخدم باسورد التطبيقات لـ Gmail*")
    elif data == "set_sub":
        db[uid]["step"] = "sub"
        await query.message.edit_text("📝 أرسل موضوع الرسالة:")
    elif data == "set_msg":
        db[uid]["step"] = "msg"
        await query.message.edit_text("📋 أرسل الكليشه (محتوى الرسالة):")
    elif data == "set_count":
        db[uid]["step"] = "count"
        await query.message.edit_text("🔢 أرسل عدد الرسائل المطلوب إرسالها:")
    elif data == "set_del":
        db[uid]["step"] = "delay"
        await query.message.edit_text("⏱️ أرسل عدد الثواني بين كل رسالة:")
    elif data == "start_burn":
        if not db[uid]["senders"] or not db[uid]["target"]:
            await query.answer("⚠️ بيانات ناقصة! أضف إيميلاتك والهدف أولاً.", show_alert=True)
        else:
            asyncio.create_task(burn_process(client, query.message, uid))

async def burn_process(client, msg, uid):
    data = db[uid]
    success, failed = 0, 0
    await msg.edit_text("⏳ جاري بدء الاتصال بالسيرفرات...")
    
    for i in range(int(data["count"])):
        # تبديل تلقائي بين الإيميلات المضافة
        sender_info = data["senders"][i % len(data["senders"])]
        try:
            email_user, password = sender_info.split(":")
            email_msg = MIMEText(data["msg"])
            email_msg["Subject"] = data["sub"]
            email_msg["From"] = email_user
            email_msg["To"] = data["target"]
            
            # محاولة الإرسال (Gmail كافتراضي)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_user, password)
                server.sendmail(email_user, data["target"], email_msg.as_string())
            success += 1
        except Exception as e:
            failed += 1
        
        status_text = (
            "**🚀 عملية الشد جارية الآن...**\n\n"
            f"✅ ناجح: {success}\n"
            f"❌ فشل: {failed}\n"
            f"📊 التقدم: {((success+failed)/int(data['count']))*100:.1f}%\n\n"
            f"🎯 الهدف: `{data['target']}`"
        )
        try: await msg.edit_text(status_text)
        except: pass
        
        await asyncio.sleep(int(data["delay"]))
        if (success + failed) >= int(data["count"]): break

    await client.send_message(uid, f"✅ تم الانتهاء!\nإجمالي النجاح: {success}\nبواسطة: @hlhrI")

@app.on_message(filters.text & filters.private)
async def handle_inputs(client, message):
    uid = message.from_user.id
    if uid not in db or not db[uid]["step"]: return

    step = db[uid]["step"]
    val = message.text

    if step == "target": db[uid]["target"] = val
    elif step == "sender": db[uid]["senders"].append(val)
    elif step == "sub": db[uid]["sub"] = val
    elif step == "msg": db[uid]["msg"] = val
    elif step == "count": db[uid]["count"] = int(val) if val.isdigit() else 10
    elif step == "delay": db[uid]["delay"] = int(val) if val.isdigit() else 2

    db[uid]["step"] = None
    await message.reply_text(f"✅ تم حفظ {step} بنجاح!", reply_markup=main_markup())

print("--- البوت شغال الآن بحقوق سالم @hlhrI ---")
app.run()
  

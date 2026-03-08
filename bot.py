import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# --- الإعدادات الأساسية ---
# التوكن الخاص بك جاهز للعمل مباشرة
API_TOKEN = '8235473555:AAHoCxzq-JBBOsN1850XXzVl9PfA_VQ-0fU' 

# في Render لا نحتاج لبروكسي، الاتصال مباشر وسريع
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# --- لوحة التحكم (المنيو) ---
def main_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("ايميل الدعم", callback_data="set_support"),
        types.InlineKeyboardButton("اضف ايميل", callback_data="add_email"),
        types.InlineKeyboardButton("الموضوع", callback_data="set_subject"),
        types.InlineKeyboardButton("الكليشه", callback_data="set_body"),
        types.InlineKeyboardButton("الثواني", callback_data="set_seconds"),
        types.InlineKeyboardButton("بدء الارسال", callback_data="start_send"),
        types.InlineKeyboardButton("مسح الكل", callback_data="clear_all")
    ]
    keyboard.add(*buttons)
    return keyboard

# --- الأوامر الأساسية ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "مرحباً بك يا شلال في بوت الشد الخارجي 🚀\nالآن البوت يعمل بنجاح على سيرفرات Render.",
        reply_markup=main_menu()
    )

# تشغيل البوت
if __name__ == '__main__':
    from aiogram import executor
    print("جاري تشغيل البوت بنجاح...")
    executor.start_polling(dp, skip_updates=True)

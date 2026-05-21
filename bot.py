import telebot
from PIL import Image
import os
from telebot import types
import shutil

# سحب البيانات من إعدادات السيرفر
TOKEN = os.environ.get('TOKEN')
MY_ID = os.environ.get('MY_ID')

bot = telebot.TeleBot(TOKEN)
user_selection = {}

# حذف أي ويب هوك قديم لضمان عمل البوت
try:
    bot.delete_webhook()
except:
    pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if str(message.chat.id) == str(MY_ID):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("JPG", callback_data="jpg"),
            types.InlineKeyboardButton("PNG", callback_data="png"),
            types.InlineKeyboardButton("WEBP", callback_data="webp"),
            types.InlineKeyboardButton("ISO", callback_data="iso")
        )
        bot.reply_to(message, "مرحباً يا بطل! اختر صيغة التحويل، ثم أرسل الصورة:", reply_markup=markup)
    else:
        bot.reply_to(message, "غير مسموح لك باستخدام البوت.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_selection[call.message.chat.id] = call.data
    bot.answer_callback_query(call.id, f"تم اختيار: {call.data.upper()}")
    bot.send_message(call.message.chat.id, f"تمام، أرسل الصورة الآن لتحويلها إلى {call.data.upper()}.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if chat_id not in user_selection:
        bot.reply_to(message, "من فضلك اضغط /start أولاً.")
        return

    bot.reply_to(message, "جاري المعالجة...")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    input_path = 'temp.input'
    with open(input_path, 'wb') as f:
        f.write(downloaded_file)

    fmt = user_selection[chat_id]
    
    try:
        if fmt == 'iso':
            os.makedirs('temp_iso', exist_ok=True)
            shutil.copy(input_path, 'temp_iso/image.jpg')
            os.system("genisoimage -o output.iso temp_iso")
            
            with open('output.iso', 'rb') as doc:
                bot.send_document(chat_id, doc, caption="تم التغليف داخل ملف ISO!")
            os.remove('output.iso')
            shutil.rmtree('temp_iso')
        else:
            img = Image.open(input_path).convert('RGB')
            output_path = f'converted.{fmt}'
            img.save(output_path, fmt.upper())
            
            with open(output_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption=f"تم التعديل بنجاح إلى {fmt.upper()}!")
            os.remove(output_path)
            
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

print("البوت يعمل الآن...")
bot.polling(none_stop=True)

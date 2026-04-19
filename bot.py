import telebot
import google.generativeai as genai
import os

# MA'LUMOTLAR
TELEGRAM_TOKEN = '8381704996:AAGIos6JYar7I_BAwmiGk0W59b8TI69oCmw'
GEMINI_API_KEY = 'AIzaSyBjcv0vTKyB5vEkvQTYPGGSxAfXzllLDqE'

# GEMINI SOZLASH
genai.configure(api_key=GEMINI_API_KEY)

# Mavjud modellarni tekshirish va eng mosini tanlash
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Agar gemini-1.5-flash bo'lsa shuni, bo'lmasa gemini-pro ni tanlaydi
    model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else 'models/gemini-pro'
    model = genai.GenerativeModel(model_name)
    print(f"Tanlangan model: {model_name}")
except Exception as e:
    print(f"Modellarni olishda xato: {e}")
    model = genai.GenerativeModel('gemini-pro') # Default

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Bot qayta sozlandi va ishga tushdi. Savolingizni bering.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "SI javob qaytara olmadi (Xavfsizlik filtri bo'lishi mumkin).")
            
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()

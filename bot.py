import telebot
import google.generativeai as genai
import os

# 1. MA'LUMOTLARINGIZ
TELEGRAM_TOKEN = '8381704996:AAGIos6JYar7I_BAwmiGk0W59b8TI69oCmw'
GEMINI_API_KEY = 'AIzaSyBjcv0vTKyB5vEkvQTYPGGSxAfXzllLDqE'

# 2. GEMINI SOZLAMALARI
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Eng barqaror modelni tanlaymiz
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Gemini sozlashda xato: {e}")

# 3. TELEGRAM BOT SOZLAMALARI
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men Gemini AI asosida ishlaydigan aqlli botman. Savolingizni yozing!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Bot ishlayotganini ko'rsatish
        bot.send_chat_action(message.chat.id, 'typing')
        
        # SI dan javob olish
        response = model.generate_content(message.text)
        
        # Agar javob bo'sh bo'lmasa, yuborish
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Kechirasiz, javob topa olmadim.")
            
    except Exception as e:
        # BU YERDA XATONI TELEGRAMGA CHIQARAMIZ
        error_message = str(e)
        if "403" in error_message:
            bot.reply_to(message, "Xatolik 403: Google API bu hududda (server joylashgan joyda) ishlamayapti. Railway server manzilini o'zgartirish kerak.")
        elif "400" in error_message:
            bot.reply_to(message, "Xatolik 400: API kalit noto'g'ri yoki yaroqsiz.")
        else:
            bot.reply_to(message, f"Tizimda xatolik yuz berdi: {error_message}")
        print(f"Log xatoligi: {e}")

# 4. BOTNI ISHGA TUSHIRISH
if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()

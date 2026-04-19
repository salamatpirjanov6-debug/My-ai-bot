import telebot
import google.generativeai as genai

# SIZNING MA'LUMOTLARINGIZ
TELEGRAM_TOKEN = '8381704996:AAGIos6JYar7I_BAwmiGk0W59b8TI69oCmw'
GEMINI_API_KEY = 'AIzaSyBjcv0vTKyB5vEkvQTYPGGSxAfXzllLDqE'

# Gemini (Sun'iy Intellekt) ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Tezkor va bepul model

# Telegram botni sozlash
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# /start buyrug'i berilganda
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men aqlli botman. Menga xohlagan savolingizni berishingiz mumkin.")

# Foydalanuvchi matn yozganda
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Bot "yozmoqda..." statusini ko'rsatishi uchun
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Gemini-dan javob olish
        response = model.generate_content(message.text)
        
        # Javobni foydalanuvchiga yuborish
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.reply_to(message, "Kechirasiz, hozir javob bera olmayman. Keyinroq urinib ko'ring.")

# Botni ishga tushirish
if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()

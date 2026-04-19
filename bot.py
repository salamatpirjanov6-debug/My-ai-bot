import telebot
import google.generativeai as genai

# MA'LUMOTLAR
TELEGRAM_TOKEN = '8381704996:AAGIos6JYar7I_BAwmiGk0W59b8TI69oCmw'
GEMINI_API_KEY = 'AIzaSyBjcv0vTKyB5vEkvQTYPGGSxAfXzllLDqE'

# GEMINI SOZLASH
genai.configure(api_key=GEMINI_API_KEY)
# Bu yerda model nomini barqaror 'gemini-pro' ga almashtirdik
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men ishga tushdim. Savolingizni bering.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        # SI dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()

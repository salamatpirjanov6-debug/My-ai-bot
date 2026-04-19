import telebot
import google.generativeai as genai

# MA'LUMOTLAR
TELEGRAM_TOKEN = '8381704996:AAGIos6JYar7I_BAwmiGk0W59b8TI69oCmw'
GEMINI_API_KEY = 'AIzaSyBjcv0vTKyB5vEkvQTYPGGSxAfXzllLDqE'

# GEMINI SOZLASH
genai.configure(api_key=GEMINI_API_KEY)

# Mavjud modellarni aniqlash
model = None
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model = genai.GenerativeModel(m.name)
            print(f"Siz uchun mos kelgan model: {m.name}")
            break
    if not model:
        # Agar avtomatik topilmasa, majburiy gemini-pro ni ishlatamiz
        model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Model qidirishda xato: {e}")
    model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Tayyor! Bot qayta sozlandi va hozir javob berishga tayyor.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        
        # Ba'zan SI javobi bloklanishi mumkin (Safety settings)
        try:
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Kechirasiz, bu mavzuda javob bera olmayman (SI filtri).")
            
    except Exception as e:
        bot.reply_to(message, f"Tizim xatosi: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()

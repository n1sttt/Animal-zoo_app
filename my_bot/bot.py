import os
import random
import telebot
from dotenv import load_dotenv
from telebot import types
Завантаження токена з файлу .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
raise ValueError("Токен BOT_TOKEN не знайдено у файлі .env")
bot = telebot.TeleBot(TOKEN)
Список тварин із п'ятьма характеристиками
animals = [
{
"name": "Аксолотль",
"habitat": "Прісні водойми Мексики",
"food": "Черв'яки, комахи та дрібні водні тварини",
"favorite": "Черв'яки",
"lifespan": "10–15 років",
"fact": "Аксолотль здатний відновлювати втрачені кінцівки."
},
{
"name": "Кролик",
"habitat": "Луки, ліси та степи",
"food": "Трава, сіно та листя",
"favorite": "Свіжа зелень",
"lifespan": "8–12 років",
"fact": "Кролики можуть повертати вуха в різні боки, щоб краще чути."
},
{
"name": "Пінгвін",
"habitat": "Південна півкуля",
"food": "Риба, криль та кальмари",
"favorite": "Риба та криль",
"lifespan": "15–20 років",
"fact": "Пінгвіни не вміють літати, але чудово плавають."
},
{
"name": "Лев",
"habitat": "Савани Африки",
"food": "М'ясо",
"favorite": "М'ясо копитних тварин",
"lifespan": "10–15 років у дикій природі",
"fact": "Леви живуть групами, які називаються прайдами."
},
{
"name": "Коала",
"habitat": "Евкаліптові ліси Австралії",
"food": "Листя евкаліпта",
"favorite": "Листя евкаліпта",
"lifespan": "10–15 років у дикій природі",
"fact": "Коали можуть спати до 18–20 годин на добу."
}
]
Команда початку роботи
@bot.message_handler(commands=["start"])
def start(message):
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    types.KeyboardButton("/animal"),
    types.KeyboardButton("/quiz")
)
keyboard.add(types.KeyboardButton("/help"))

bot.send_message(
    message.chat.id,
    "Вітаю! Я ZooHelper — бот про тварин.\n\n"
    "Тут ти можеш дізнаватися цікаві факти "
    "про тварин та перевіряти свої знання!",
    reply_markup=keyboard
)
Команда допомоги
@bot.message_handler(commands=["help"])
def help_command(message):
bot.send_message(
message.chat.id,
"Команди ZooHelper:\n\n"
"/start — початок роботи з ботом.\n"
"/help — список команд.\n"
"/animal — випадкова тварина.\n"
"/quiz — вікторина про тварин."
)
Команда випадкової тварини
@bot.message_handler(commands=["animal"])
def animal_command(message):
animal = random.choice(animals)
text = (
    f"🐾 {animal['name']}\n\n"
    f"🌍 Середовище проживання: {animal['habitat']}\n"
    f"🍽 Харчування: {animal['food']}\n"
    f"❤️ Улюблена їжа: {animal['favorite']}\n"
    f"⏳ Тривалість життя: {animal['lifespan']}\n"
    f"💡 Цікавий факт: {animal['fact']}"
)

bot.send_message(message.chat.id, text)
Команда вікторини
@bot.message_handler(commands=["quiz"])
def quiz_command(message):
animal = random.choice(animals)
correct = animal["habitat"]
options = list(set(
    a["habitat"] for a in animals
    if a["habitat"] != correct
))

answers = random.sample(options, 2) + [correct]
random.shuffle(answers)

keyboard = types.InlineKeyboardMarkup()

for answer in answers:
    keyboard.add(
        types.InlineKeyboardButton(
            text=answer,
            callback_data=f"quiz|{correct}|{answer}"
        )
    )

bot.send_message(
    message.chat.id,
    f"🧠 Вікторина!\n\nДе живе тварина: {animal['name']}?",
    reply_markup=keyboard
)
Перевірка відповіді у вікторині
@bot.callback_query_handler(
func=lambda call: call.data.startswith("quiz|")
)
def check_answer(call):
_, correct, answer = call.data.split("|", 2)
if answer == correct:
    result = "✅ Правильно! Чудова робота!"
else:
    result = f"❌ Неправильно! Правильна відповідь: {correct}"

bot.answer_callback_query(call.id)

bot.edit_message_reply_markup(
    call.message.chat.id,
    call.message.message_id,
    reply_markup=None
)

bot.send_message(call.message.chat.id, result)
Запуск бота
print("ZooHelper запущено!")
bot.infinity_polling()

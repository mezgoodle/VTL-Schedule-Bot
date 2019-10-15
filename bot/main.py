import telebot
import sqlite3
from bot.config import TG_TOKEN, database

conn = sqlite3.connect(database)
print(conn)
bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/today', '/tomorrow')
    bot.send_message(message.from_user.id, 'Вітаємо! Це бот, що показує розклад по групам ВТЛ. Для почтаку встанови код своєї групи(/group_[назва групи]), наприклад, /group_pm1. Потім за допомогою клавіатури або команд дізнавайся, який у тебе зараз урок', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Клавіатуру вимкнено', reply_markup=hide_markup)

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, """
        /today - Розклад на сьогодні
/tomorrow - Розклад на завтра
/week - Розклад на тиждень
/nextweek - Розклад на наступний тиждень
/help - Список усіх команд
/timetable - Розклад дзвінків
/who - Підказує ім'я вчителя
/group - Встановити групу
/stop - Вимкнути клавіатуру
    """)

@bot.message_handler(commands=['timetable'])
def handle_timetable(message):
    bot.send_message(message.chat.id, """
        1. 08.30 - 09.15
2. 09.25 - 10.10
3. 10.20 - 11.05
4. 11.20 - 12.05
5. 12.25 - 13.10
6. 13.30 - 14.15
7. 14.25 - 15.10
8. 15.15 - 16.00
    """)

# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     if message.text == "a":
#         bot.send_message(message.chat.id,"B")
#     elif  message.text == "B":
#         bot.send_message(message.chat.id, "a")
#     else:
#         bot.send_message(message.chat.id, "Lose")

bot.polling(none_stop=True, interval=0)
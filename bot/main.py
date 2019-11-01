import telebot
import sqlite3
from bot.config import TG_TOKEN, database

conn = sqlite3.connect(database)
print(conn)
bot = telebot.TeleBot(TG_TOKEN)

# Group dictionary
GROUP_DICT = {
    '/group_pm1': 'pm1',
    '/group_pm2': 'pm2',
    '/group_pm3': 'pm3',
    '/group_pm4': 'pm4',
    '/group_lin3': 'lin3',
    '/group_lin4': 'lin4',
    '/group_itn1': 'itn1',
    '/group_itn2': 'itn2',
    '/group_itn3': 'itn3',
    '/group_itn4': 'itn4',
    '/group_pn1': 'pn1',
    '/group_pn2': 'pn2',
    '/group_ite3': 'ite3',
    '/group_itr4': 'itr4',
}

# Group identification
GROUP_ID = ''

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/today', '/tomorrow')
    bot.send_message(message.from_user.id, 'Вітаємо! Це бот, що показує розклад по групам ВТЛ. Для почтаку встанови код своєї групи(/group_[назва групи]), наприклад, /group_pm1. Потім за допомогою клавіатури або команд дізнавайся, який у тебе зараз урок', reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Клавіатуру вимкнено', reply_markup=hide_markup)

@bot.message_handler(commands=['group'])
def handle_group_damn(message):
    bot.send_message(message.from_user.id, 'Для почтаку встанови код своєї групи(/group_[назва групи]), наприклад, /group_pm1.')

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
https://telegra.ph/Kodi-grup-dlya-vtl-schedule-bot-10-25 - Коди груп
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

@bot.message_handler(content_types=['text'])
def handle_group(message):
    #bot.send_message(message.chat.id, str(type(message.text))) DEBUG
    if str(message.text)[-1].isdigit():
        bot.send_message(message.chat.id, GROUP_DICT[message.text])
        print(GROUP_DICT[message.text])
    else:
        print('FALSE')
        bot.send_message(message.chat.id, 'Надіюсь, ти правильно написав команду\U0001f600. Якщо не знаєш, що писати, переглянь /help.')

# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     if message.text == "a":
#         bot.send_message(message.chat.id,"B")
#     elif  message.text == "B":
#         bot.send_message(message.chat.id, "a")
#     else:
#         bot.send_message(message.chat.id, "Lose")

bot.polling(none_stop=True, interval=0)
import telebot
import sqlite3
from bot.config import TG_TOKEN, database
from datetime import datetime, date, time

# Connection to database

# Datetime
today = datetime.now()
# print(today.strftime("%w"))

# Group identification
GROUP_ID = ''

# Day`s name dictionary
dayName_DICT = {
    1: 'Понеділок',
    2: 'Вівторок',
    3: 'Середа',
    4: 'Четвер',
    5: "П`ятниця",
}

def today_schedule(message):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"
    cursor.execute(sql, (GROUP_ID, today.strftime('%w')))
    if today.strftime('%w') == '6' or today.strftime('%w') == '0':
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
    else:
        string_d = dayName_DICT[int(today.strftime('%w'))] + '\n'
        string = ''
        for element in cursor.fetchall():
            print(element)
            string += str(element[4]) + ' - ' + element[2] + ', ' + element[3] + ', ' + element[1] + '\n'
        bot.send_message(message.chat.id, f"*{string_d}*" + string, parse_mode='Markdown')
# print(conn)

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

@bot.message_handler(commands=['today'])
def handle_today(message):
    today_schedule(message)

@bot.message_handler(commands=['who'])
def handle_today(message):
    if int(today.strftime("%w")) < 5 or int(today.strftime("%w")) == 0:
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
    else:
        print(cursor.fetchall())

@bot.message_handler(content_types=['text'])
def handle_group(message):
    if str(message.text)[-1].isdigit():
        bot.send_message(message.chat.id, 'Вітаю! Ви встановили код групи - ' + GROUP_DICT[message.text])
        global GROUP_ID
        GROUP_ID = GROUP_DICT[message.text]
    else:
        bot.send_message(message.chat.id, 'Надіюсь, ти правильно написав команду\U0001f600. Якщо не знаєш, що писати, переглянь /help.')


bot.polling(none_stop=True, interval=0)
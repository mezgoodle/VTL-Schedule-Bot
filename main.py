import sqlite3
from datetime import datetime, time
from util.config import TG_TOKEN, database
from flask import Flask, request

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Take bot`s token
bot = telebot.TeleBot(TG_TOKEN)

# Group dictionary
GROUP_ID = {}

# Day`s name dictionary
dayName_DICT = {
    1: 'Понеділок',
    2: 'Вівторок',
    3: 'Середа',
    4: 'Четвер',
    5: "П`ятниця",
}

# Letters array
LETTERS_ARRAY = ['e', 'r', 'n', 'm']

# Time Array
TIME_ARRAY = [
    [time(8, 30, 0), time(9, 15, 0), time(9, 15, 0), time(9, 25, 0)],
    [time(9, 25, 0), time(10, 10, 0), time(10, 10, 0), time(10, 20, 0)],
    [time(10, 20, 0), time(11, 5, 0), time(11, 5, 0), time(11, 20, 0)],
    [time(11, 20, 0), time(12, 5, 0), time(12, 5, 0), time(12, 25, 0)],
    [time(12, 25, 0), time(13, 10, 0), time(13, 10, 0), time(13, 30, 0)],
    [time(13, 30, 0), time(14, 15, 0), time(14, 15, 0), time(14, 25, 0)],
    [time(14, 25, 0), time(15, 10, 0), time(15, 10, 0), time(15, 15, 0)],
    [time(15, 15, 0), time(16, 0, 0)],
]

# Time borders
early_time = time(8, 30, 0)
late_time = time(16, 0, 0)


# Connection to database
def connection_to_database():
    conn = sqlite3.connect(database)
    return conn.cursor()


# Datetime
def take_date():
    return datetime.now()


# Check if today is weekend
def check_today(today):
    today = today
    if today.strftime('%w') == '6' or today.strftime('%w') == '0':
        return True
    else:
        return False

# Generation InlineKeyboardMarkup
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton('ФМН-1', callback_data='/group_pm1'),
        InlineKeyboardButton('ФМН-2', callback_data='/group_pm2'),
        InlineKeyboardButton('ФМН-3', callback_data='/group_pm3'),
        InlineKeyboardButton('ФМН-4', callback_data='/group_pm4'),
        InlineKeyboardButton('ЛІН-3', callback_data='/group_lin3'),
        InlineKeyboardButton('ЛІН-4', callback_data='/group_lin4'),
        InlineKeyboardButton('ТПН-1', callback_data='/group_tpn1'),
        InlineKeyboardButton('ПН-2', callback_data='/group_pn2'),
        InlineKeyboardButton('ІТН-1', callback_data='/group_itn1'),
        InlineKeyboardButton('ІТН-2', callback_data='/group_itn2'),
        InlineKeyboardButton('ІТН-3', callback_data='/group_itn3'),
        InlineKeyboardButton('ІТН-4', callback_data='/group_itn4'),
        InlineKeyboardButton('ІТЕ-3', callback_data='/group_ite3'),
        InlineKeyboardButton('ІТР-4', callback_data='/group_itr4'),
    )
    return markup


# Need for making answer for schedule row
def creation_string(data):
    string = ''
    for element in data:
        string += str(element[4]) + ' - ' + element[2] + ', ' + element[3] + ', ' + element[1] + '\n'
    return string


# First 'sql' variable template
sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"


# Today schedule function
def today_schedule(message):
    today = take_date()
    cursor = connection_to_database()
    cursor.execute(sql, (GROUP_ID[message.from_user.id], today.strftime('%w')))
    if check_today(today):
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
    else:
        string_d = dayName_DICT[int(today.strftime('%w'))] + '\n'
        string = creation_string(cursor.fetchall())
        bot.send_message(message.chat.id, f"*{string_d}*" + string, parse_mode='Markdown')


# Tomorrow schedule function
def tomorrow_schedule(message):
    today = take_date()
    cursor = connection_to_database()
    cursor.execute(sql, (GROUP_ID[message.from_user.id], str(int(today.strftime('%w')) + 1)))
    if str(int(today.strftime('%w')) + 1) == '6' or str(int(today.strftime('%w')) + 1) == '7':
        bot.send_message(message.chat.id, 'Завтра вихідний\U0001F973, відпочивай!')
    else:
        string_d = dayName_DICT[int(today.strftime('%w')) + 1] + '\n'
        string = creation_string(cursor.fetchall())
        bot.send_message(message.chat.id, f"*{string_d}*" + string, parse_mode='Markdown')


# Week schedule function
def week_schedule(message):
    today = take_date()
    cursor = connection_to_database()
    sql = "SELECT * FROM schedule WHERE group_name=?"
    cursor.execute(sql, ([GROUP_ID[message.from_user.id]]))
    if today.strftime('%w') == '6':
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
    else:
        string_all = ''
        for i in range(1, 6):
            string_all += dayName_DICT[i] + '\n'
            string_all += one_day(i, message) + '\n'
        bot.send_message(message.chat.id, string_all)


# Teacher`s name function
def who_is_now(message, today):
    cursor = connection_to_database()
    current_time = today  # + timedelta(hours=2)
    # Only if you are going to use PythonAnywhere service and if you are in Ukraine. For example, if I launch bot on
    # my localhost, I needn`t +2 hours to current time, and can use today.time()
    if current_time.time() > late_time:
        bot.send_message(message.chat.id, 'Навчання вже закінчилось, відпочивай!\U0001F973')
        return
    elif current_time.time() < early_time:
        bot.send_message(message.chat.id, 'Навчання ще не почалось, готуйся!\U0001F973')
        return
    i = 0
    for timeInterval in TIME_ARRAY:
        if timeInterval[0] <= current_time.time() <= timeInterval[1]:
            cursor.execute(sql, (GROUP_ID[message.from_user.id], current_time.strftime('%w')))
            data = cursor.fetchall()
            try:
                if data[0][4] != 2:
                    bot.send_message(message.chat.id, data[i][3])
                else:
                    bot.send_message(message.chat.id, data[i - 1][3])
            except IndexError:
                if i == 7 and current_time.strftime('%w') == '5':
                    bot.send_message(message.chat.id, 'Не знаєш ім\'я свого класного керівника?')
                else:
                    bot.send_message(message.chat.id, 'Навчання вже закінчилось, відпочивай!\U0001F973')
            except:
                bot.send_message(message.chat.id, 'Ця функція наразі на стадії доопрацювання, спробуйте пізніше')
            return
        i += 1
    bot.send_message(message.chat.id,
                     'Напевно, зараз перерва. Сходи в їдальню та готуйся до наступного уроку\U0001F642')


# Helpful function for 'week' function
def one_day(day_is, message):
    cursor = connection_to_database()
    cursor.execute(sql, (GROUP_ID[message.from_user.id], day_is))
    string = ''
    for element in cursor.fetchall():
        string += str(element[4]) + ' - ' + element[2] + ', ' + element[3] + ', ' + element[1] + '\n'
    return string


# Remainder time function
def detect_time():
    today = take_date()
    if today.time() < early_time:
        return 'Навчання ще не почалось, готуйся!\U0001F973'
    elif today.time() > late_time:
        return 'Навчання вже закінчилось, відпочивай!\U0001F601'
    now = today.hour * 3600 + today.minute * 60 + today.second
    for timeInterval in TIME_ARRAY:
        if timeInterval[0] <= today.time() <= timeInterval[1]:
            upper_time = timeInterval[1].hour * 3600 + timeInterval[1].minute * 60 + timeInterval[1].second
            minutes = int((upper_time - now) / 60)
            seconds = (upper_time - now) - minutes * 60
            return [minutes, seconds, 'уроку']
        if timeInterval[2] <= today.time() <= timeInterval[3]:
            upper_time = timeInterval[3].hour * 3600 + timeInterval[3].minute * 60 + timeInterval[3].second
            minutes = int((upper_time - now) / 60)
            seconds = (upper_time - now) - minutes * 60
            return [minutes, seconds, 'перерви']


# print(conn) For testing database connection


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
    '/group_tpn1': 'tpn1',
    '/group_pn2': 'pn2',
    '/group_ite3': 'ite3',
    '/group_itr4': 'itr4',
}


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Сьогодні', "Завтра")
    bot.send_message(message.from_user.id,
                     'Вітаємо! Це бот, що показує розклад по групам ВТЛ. Для почтаку встанови код своєї групи('
                     '/group_[назва групи]), наприклад, /group_pm1. Потім за допомогою клавіатури або команд '
                     'дізнавайся, який у тебе зараз урок',
                     reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Клавіатуру вимкнено', reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """
        /today - Розклад на сьогодні
/tomorrow - Розклад на завтра
/week - Розклад на тиждень
/help - Список усіх команд
/timetable - Розклад дзвінків
/who - Підказує ім'я вчителя
/group - Встановити групу
/left - Показує скільки залишилось до кінця уроку(перерви)
/stop - Вимкнути клавіатуру
https://telegra.ph/Kodi-grup-dlya-vtl-schedule-bot-10-25 - Коди груп
Якщо у розкладі є неточності, пишіть @feedback_sch_vtl_bot
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
    if not message.from_user.id in GROUP_ID:
        GROUP_ID[message.from_user.id] = ''
    if GROUP_ID[message.from_user.id] != '':
        today_schedule(message)
    else:
        bot.send_message(message.chat.id,
                         'Для початку встанови код групи(/group_[назва групи]), наприклад, /group_pm1.\U0001F601')


@bot.message_handler(commands=['tomorrow'])
def handle_tomorrow(message):
    if not message.from_user.id in GROUP_ID:
        GROUP_ID[message.from_user.id] = ''
    if GROUP_ID[message.from_user.id] != '':
        tomorrow_schedule(message)
    else:
        bot.send_message(message.chat.id,
                         'Для початку встанови код групи(/group_[назва групи]), наприклад, /group_pm1.\U0001F601')


@bot.message_handler(commands=['week'])
def handle_week(message):
    if not message.from_user.id in GROUP_ID:
        GROUP_ID[message.from_user.id] = ''
    if GROUP_ID[message.from_user.id] != '':
        week_schedule(message)
    else:
        bot.send_message(message.chat.id,
                         'Для початку встанови код групи(/group_[назва групи]), наприклад, /group_pm1.\U0001F601')


@bot.message_handler(commands=['who'])
def handle_who(message):
    today = take_date()
    if not message.from_user.id in GROUP_ID:
        GROUP_ID[message.from_user.id] = ''
    if GROUP_ID[message.from_user.id] != '':
        if check_today(today):
            bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
        else:
            who_is_now(message, today)
    else:
        bot.send_message(message.chat.id,
                         'Для початку встанови код групи(/group_[назва групи]), наприклад, /group_pm1.\U0001F601')


@bot.message_handler(commands=['group'])
def handle_group(message):
    bot.send_message(message.chat.id, 'Натисніть і оберіть вашу групу:', reply_markup=gen_markup())


@bot.message_handler(commands=['left'])
def handle_left(message):
    today = take_date()
    if check_today(today):
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
        return
    result = detect_time()
    if isinstance(result, str):
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, f'До кінця {result[2]} {result[0]} хв., {result[1]} сек.')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Сьогодні':
        handle_today(message)
        return
    elif message.text == 'Завтра':
        handle_tomorrow(message)
        return
    if (str(message.text)[-1].isdigit()) and (str(message.text) in GROUP_DICT) and (
            str(message.text)[-2] in LETTERS_ARRAY):
        GROUP_ID[message.from_user.id] = GROUP_DICT[message.text]
        bot.send_message(message.chat.id, 'Вітаю! Ви встановили код групи - ' + GROUP_DICT[message.text])
    else:
        bot.send_message(message.chat.id,
                         'Надіюсь, ти правильно написав команду\U0001f600. Якщо не знаєш, що писати, переглянь /help.')


@bot.callback_query_handler(func=lambda call: True)
def callback_handle(call):
    bot.answer_callback_query(call.id, 'Вітаю! Ви встановили код групи - ' + GROUP_DICT[call.data])
    GROUP_ID[call.message.chat.id] = GROUP_DICT[call.data]


# ==============
# server = Flask(__name__)


# @server.route('/' + TG_TOKEN, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://vtl-schedule-bot.herokuapp.com/' + TG_TOKEN)
#     return "!", 200


# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
# For production
# ==============

# The work of the bot itself
# For development
bot.polling(none_stop=True, interval=0)

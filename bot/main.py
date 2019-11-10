import telebot
import sqlite3
from bot.config import TG_TOKEN, database
from datetime import datetime, time, timedelta

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

# Books array
BOOK_ARRAY = ['e', 'r', 'n', 'm']

# Time Array
TIME_ARRAY = [
    [time(8, 30, 0), time(9, 15, 0)],
    [time(9, 25, 0), time(10, 10, 0)],
    [time(10, 20, 0), time(11, 5, 0)],
    [time(11, 20, 0), time(12, 5, 0)],
    [time(12, 25, 0), time(13, 10, 0)],
    [time(13, 30, 0), time(14, 15, 0)],
    [time(14, 25, 0), time(15, 10, 0)],
    [time(15, 10, 0), time(16, 0, 0)],
]


def connection_to_database():
    # Connection to database
    conn = sqlite3.connect(database)
    return conn.cursor()


def take_date():
    # Datetime
    return datetime.now()


def creation_string(data):
    string = ''
    for element in data:
        string += str(element[4]) + ' - ' + element[2] + ', ' + element[3] + ', ' + element[1] + '\n'
    return string


def today_schedule(message):
    today = take_date()
    cursor = connection_to_database()
    sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"
    cursor.execute(sql, (GROUP_ID[message.from_user.id], today.strftime('%w')))
    if today.strftime('%w') == '6' or today.strftime('%w') == '0':
        bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
    else:
        string_d = dayName_DICT[int(today.strftime('%w'))] + '\n'
        string = creation_string(cursor.fetchall())
        bot.send_message(message.chat.id, f"*{string_d}*" + string, parse_mode='Markdown')


def tomorrow_schedule(message):
    today = take_date()
    cursor = connection_to_database()
    sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"
    cursor.execute(sql, (GROUP_ID[message.from_user.id], str(int(today.strftime('%w')) + 1)))
    if str(int(today.strftime('%w')) + 1) == '6' or str(int(today.strftime('%w')) + 1) == '7':
        bot.send_message(message.chat.id, 'Завтра вихідний\U0001F973, відпочивай!')
    else:
        string_d = dayName_DICT[int(today.strftime('%w')) + 1] + '\n'
        string = creation_string(cursor.fetchall())
        bot.send_message(message.chat.id, f"*{string_d}*" + string, parse_mode='Markdown')


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


def who_is_now(message):
    cursor = connection_to_database()
    early_time = time(8, 0, 0)
    late_time = time(16, 0, 0)
    current_time = datetime.now()  # + timedelta(hours=2)
    # Only if you are goint to use PythonAnywhere service and if you are in Ukraine. For example, if i launch bot on
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
            today = take_date()
            sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"
            cursor.execute(sql, (GROUP_ID[message.from_user.id], today.strftime('%w')))
            data = cursor.fetchall()
            if len(data) < i:
                bot.send_message(message.chat.id, 'Навчання вже закінчилось, відпочивай!\U0001F973')
                return
            if data[0][4] != 2:
                bot.send_message(message.chat.id, data[i][3])
            else:
                bot.send_message(message.chat.id, data[i - 1][3])
            return
        i += 1
    bot.send_message(message.chat.id,
                     'Напевно, зараз перерва. Сходи в їдальню та готуйся до наступного уроку\U0001F642')


def one_day(day_is, message):
    cursor = connection_to_database()
    sql = "SELECT * FROM schedule WHERE group_name=? AND day_is=?"
    cursor.execute(sql, (GROUP_ID[message.from_user.id], day_is))
    string = ''
    for element in cursor.fetchall():
        string += str(element[4]) + ' - ' + element[2] + ', ' + element[3] + ', ' + element[1] + '\n'
    return string


# print(conn) For testing database connection


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
    '/group_tpn1': 'tpn1',
    '/group_pn2': 'pn2',
    '/group_ite3': 'ite3',
    '/group_itr4': 'itr4',
}


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/today', '/tomorrow')
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
        if today.strftime('%w') == '6' or today.strftime('%w') == '0':
            bot.send_message(message.chat.id, 'Сьогодні вихідний\U0001F973, відпочивай!')
        else:
            who_is_now(message)
    else:
        bot.send_message(message.chat.id,
                         'Для початку встанови код групи(/group_[назва групи]), наприклад, /group_pm1.\U0001F601')


@bot.message_handler(commands=['group'])
def handle_group(message):
    bot.send_message(message.chat.id, '''
    Список груп:
/group_pm1 - ФМН-1,
/group_pm2 - ФМН-2,
/group_pm3 - ФМН-3,
/group_pm4 - ФМН-4,
/group_lin3 - ЛІН-3,
/group_lin4 - ЛІН-4,
/group_itn1 - ІТН-1,
/group_itn2 - ІТН-2,
/group_itn3 - ІТН-3,
/group_itn4 - ІТН-4,
/group_tpn1 - ТПН-1,
/group_pn2 - ПН-2,
/group_ite3 - ІТЕ-3,
/group_itr4 - ІТР-4
    ''')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if (str(message.text)[-1].isdigit()) and (str(message.text) in GROUP_DICT) and (
            str(message.text)[-2] in BOOK_ARRAY):
        GROUP_ID[message.from_user.id] = GROUP_DICT[message.text]
        bot.send_message(message.chat.id, 'Вітаю! Ви встановили код групи - ' + GROUP_DICT[message.text])
    else:
        bot.send_message(message.chat.id,
                         'Надіюсь, ти правильно написав команду\U0001f600. Якщо не знаєш, що писати, переглянь /help.')


bot.polling(none_stop=True, interval=0)

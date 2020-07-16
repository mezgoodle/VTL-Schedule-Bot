# Schedule bot

Welcome to this repository! This is the [Telegram](https://telegram.org/) bot for showing schedule in [VTL](https://vtl.in.ua/).

>[link](https://t.me/vtl_schedule_bot) to bot

## Table of contents

- [Motivation](#motivation)
- [Code style](#code-style)
- [Screenshots](#screenshots)
- [Tech framework used](#tech-framework-used)
- [Features](#features)
- [Code Example](#code-example)
- [Installation](#installation)
- [API Reference](#api-reference)
- [Deploy](#deploy)
- [Contribute](#contribute)
- [Credits](#credits)
- [Contact](#contact)
- [License](#license)

## Motivation

It all started when I started studying at [KPI](https://kpi.ua/). Of course, in the first year it is **very difficult** to understand how studying at the university works. Just in the telegram there was a [bot](https://t.me/KPI_schedule_bot) showing the schedule. And then I had the *idea* to create the same for my school.

## Code style

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/330cb34d0f5a47c08e7920b3ae6e6770)](https://www.codacy.com/manual/mezgoodle/VTL-Schedule-Bot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mezgoodle/VTL-Schedule-Bot&amp;utm_campaign=Badge_Grade)

## Screenshots

![Screenshot 1](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot1.png)

![Screenshot 2](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot2.png)

![Screenshot 3](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot3.png)

![Screenshot 4](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot4.png)

![Screenshot 5](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot5.png)

![Screenshot 6](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot6.png)

![Screenshot 7](https://raw.githubusercontent.com/mezgoodle/images/master/vtl-schedule-bot7.png)

## Tech framework used

**Built with**
 - [Python](https://www.python.org/)
 - [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
 - [sqlite3](https://docs.python.org/3/library/sqlite3.html)
 
 ## Dependencies
 
 > You can see all dependencies in `requirements.txt` [here](https://github.com/mezgoodle/VTL-Schedule-Bot/network/dependencies)

## Features

- /today - get schedule for today.

- /tomorrow  - get schedule for tomorrow.

- /week - get schedule for week.

- /group - choose your group from *keyboard*.

- /timetable - get timetable of lessons.

- /who - get teacher`s name of current lesson.

- /left - get shows how much time is left until the end of the lesson / break.

- /start - set the reply *keyboard*.

- /stop - remove the *keyboard* from **start** event.

## Code Example

 - Set web hooks

```python
# Listener (handler) for telegram's /set event
server = Flask(__name__)


@server.route('/' + TG_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://vtl-schedule-bot.herokuapp.com/' + TG_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
```

## Installation

1. Clone this repository

```bash
git clone https://github.com/mezgoodle/weather-bot.git
```

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

3. Rename `.env_sample` to `.env` and fill the variables like:

```bash
TELEGRAM_TOKEN = "<YOUR_TELEGRAM_TOKEN>"
```

4. Type in terminal:

```bash
python main.py
```

## API Reference

Here I am using two main API services:
 - [Telegram Bot API](https://core.telegram.org/bots/api)

## Deploy

I use direct connection for deploying to [Heroku](https://www.heroku.com/). 

## Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits

Repositories and links which inspired me to build this project:
 - https://t.me/KPI_schedule_bot

## Contact

If you have questions write me here: 
  *   [Telegram](https://t.me/sylvenis)
  *   [Gmail](mailto:mezgoodle@gmail.com)
  *   [Facebook](https://www.facebook.com/profile.php?id=100005721694357)

## License

![GitHub](https://img.shields.io/github/license/mezgoodle/weather-bot)

MIT © [mezgoodle](https://github.com/mezgoodle)

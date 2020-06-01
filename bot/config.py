from dotenv import load_dotenv
import os
load_dotenv()

TG_TOKEN = os.getenv('TOKEN')
database = "../bot.db"
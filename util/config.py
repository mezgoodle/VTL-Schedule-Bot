from dotenv import load_dotenv
import os
load_dotenv()

TG_TOKEN = os.getenv('TOKEN')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(BASE_DIR, '../bot.db')
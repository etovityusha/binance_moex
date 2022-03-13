import os
from dotenv import load_dotenv

load_dotenv()

TINKOFF_TOKEN = os.getenv('TINKOFF_TOKEN')
BASE_URL = 'http://127.0.0.1:6110'

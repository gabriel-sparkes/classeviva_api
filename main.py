from user import *
from dotenv import load_dotenv
import os

load_dotenv()

user = User(os.getenv("CVV_UID"), os.getenv("CVV_PWD"))
user.login()
for lol in user.get_communications("read"):
    print(lol["testo"].strip() + "\n" + "-"*20)
user.logout()
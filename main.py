from user import *
from dotenv import load_dotenv
import os

load_dotenv()

user = User(os.getenv("CVV_UID"), os.getenv("CVV_PWD"))
user.login()
print(user.get_marks())
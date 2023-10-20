import requests
import time
from bs4 import BeautifulSoup

LOGIN = "https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php?a=aLoginPwd"
LOGOUT = "https://web.spaggiari.eu/home/app/default/logout.php"
MARKS = "https://web.spaggiari.eu/cvv/app/default/genitori_note.php"
COMMUNICATIONS = "https://web.spaggiari.eu/sif/app/default/bacheca_personale.php"
USERNAME = "https://web.spaggiari.eu/tools/app/default/get_username.php"
AGENDA = "https://web.spaggiari.eu/fml/app/default/agenda_studenti.php?ope=get_events"

s = requests.Session()

class User:
    def __init__(self, uid: str, pwd: str):
        self.session = requests.Session()
        self.uid = uid
        self.pwd = pwd

    def login(self):
        self.session.post(LOGIN, {"uid": self.uid, "pwd": self.pwd})

    def logout(self):
        self.session.get(LOGOUT)

    def is_logged_in(self):
        try:
            return self.session.get(USERNAME).json() is not None
        except:
            return False
        
    def get_username(self):
        return self.session.get(USERNAME).json()
        
    def get_agenda(self, days):
        payload = {
            "start": int(time.time()),
            "end": int(time.time()) + 86400*(days+1)
        }
        return self.session.post(AGENDA, payload).json()
    
    def get_marks(self):
        subjects = {}
        last_subject = ""
        text = self.session.get(MARKS).text
        soup = BeautifulSoup(text, "html.parser")
        tags = soup.select('tr[valign="middle"]:has(td.registro) ~ tr:not(:has(td.registro)), tr[valign="middle"]:has(td.registro)')
        for tag in tags:
            if "registro" in tag.td.get("class", {}):
                subjects[tag.text.strip()] = []
        for tag in tags:
            if tag.text.strip() in subjects:
                last_subject = tag.text.strip()
                continue
            date = tag.select_one('[title=":campo_2:"]').text.strip()
            mark = tag.select_one(".s_reg_testo.cella_trattino").text.strip()
            mark_type = tag.select_one('p:not([title=":campo_2:"]) span').text.strip()
            comment = tag.select_one('span[style="font-weight: bold"]').text.strip()
            subjects[last_subject].append({"date": date, "mark": mark, "type": mark_type, "comment": comment})
        return subjects
    
    def get_communications(self, which=""):
        if which == "new":
            return self.session.post(COMMUNICATIONS, {"action": "get_comunicazioni", "ncna": "1"}).json()["msg_new"]
        elif which == "read":
            return self.session.post(COMMUNICATIONS, {"action": "get_comunicazioni", "ncna": "1"}).json()["read"]
        return self.session.post(COMMUNICATIONS, {"action": "get_comunicazioni", "ncna": "1"}).json()
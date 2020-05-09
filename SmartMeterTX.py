import requests
import json

AUTH_URL = "https://smartmetertexas.com/api/user/authenticate"
DAILY_URL = "https://smartmetertexas.com/api/adhoc/dailysynch"
TIMEOUT = 30

# pinned certificate trust
CERT = "www-smartmetertexas-com-chain.pem"


class SmartMeterTX:
    logged_in = False

    def __init__(self, auth_url=AUTH_URL, daily_url=DAILY_URL, timeout=TIMEOUT):
        self.session = requests.Session()
        self.auth_url = auth_url
        self.daily_url = daily_url
        self.timeout = timeout
        # self.session.headers["referrer"] = "https://www.smartmetertexas.com/home"
        # self.session.headers["origin"] = "https://www.smartmetertexas.com"
        # self.session.headers["user-agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.142 Safari/537.36"

    def api_call(self, url, json):
        try:
            return self.session.post(url=url, json=json, timeout=self.timeout, verify=CERT)
        except Exception as ex:
            print(repr(ex))
            raise

    def login(self, username, password):
        creds = {
            "username": username,
            "password": password
        }

        r = self.api_call(self.auth_url, json=creds)
        if (r.status_code != 200):
            print("Login failed.")
            return False
        else:
            self.token = r.json()['token']
            print("Login successful!")
            self.session.headers["Authorization"] = f"Bearer {self.token}"
            self.logged_in = True
            return r

    def get_daily_read(self, essid, start_date, end_date):
        if self.logged_in == False:
            print("You must login first.")
            return False
        if type(essid) == str:
            essid = [essid]

        json = {
            "ESIID": essid,
            "endDate": end_date,
            "readDate": None,
            "reportFormat": "JSON",
            "startDate": start_date,
            "versionDate": None,
            "versionNum": None
        }

        r = self.api_call(self.daily_url, json=json)
        if (r.status_code != 200 or "error" in r.text.lower()):
            print("Error fetching daily read.")
            print(r.text)
            return False
        else:
            return r.json()

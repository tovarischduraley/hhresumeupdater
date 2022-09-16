import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HHResumeUpdater(metaclass=Singleton):
    redirect_url = os.getenv('REDIRECT_URL')
    resume_id = os.getenv('RESUME_ID')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    client_code = os.getenv('CLIENT_CODE')

    """
    Todo:
    Implement get_code()
    """

    def get_access_token(self):
        url = "https://hh.ru/oauth/token"

        response = requests.post(url=url, data={"grant_type": "authorization_code",
                                                "client_id": self.client_id,
                                                "client_secret": self.client_secret,
                                                "code": self.client_code})

        if response.status_code == 200:
            return response.json()
            # return response.json()
        print("Response text", response.text)
        print("Response code", response.status_code)


updater = HHResumeUpdater()

# https://hh.ru/oauth/authorize?response_type=code&client_id=CLIENT_ID
#
# copy code from this http://yourapphost/?code=CODE
#
# curl -k -X POST -H 'User-Agent: api-test-agent' -d 'grant_type=authorization_code&client_id=CLIENT_ID&client_secret=CLIENT_SECRET&code=CODE' https://hh.ru/oauth/token
#
# resp = {
#     "token_type": "bearer",
#     "access_token": "",
#     "refresh_token": "UKK5I63M7T65H21K14DS2DPCSUG2HDSNLQ6407S5HD206KSH9PJRAVLVSAOR2RD7",
#     "expires_in": 1209599  # = 2 weeks
# }

if __name__ == '__main__':
    updater.get_access_token()

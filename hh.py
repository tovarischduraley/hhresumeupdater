import os
from time import sleep
from typing import Optional
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

    def get_code(self):
        url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={self.client_id}"
        response = requests.get(url=url)
        print("Response text: \n", response.text)
        print("Response url: \n", response.url)

    def authenticate(self) -> dict:
        url = "https://hh.ru/oauth/token"

        response = requests.post(url=url, data={"grant_type": "authorization_code",
                                                "client_id": self.client_id,
                                                "client_secret": self.client_secret,
                                                "code": self.client_code})

        if response.status_code == 200:
            return response.json()

        print("Response text", response.text)
        print("Response code", response.status_code)

    def update_resume(self, access_token: str):
        url = f"https://api.hh.ru/resumes/{self.resume_id}/publish"
        headers = {'Authorization': 'Bearer ' + access_token}

        def update(sleep_time: Optional[int] = 0) -> None:
            sleep(sleep_time)
            response = requests.post(url=url, headers=headers)
            if response.status_code == 200:
                print('Success: ', 'Resume was updated')
                update(60 * 60 * 4 + 60 * 1)
            if response.status_code == 429:
                print('Error: ', 'You are trying to update your resume too often')
                update(10 * 60)
            if response.status_code == 403:
                print('Error: ', 'Token TTL has expired. Get a new token')
                exit(1)

        update()


if __name__ == '__main__':
    updater = HHResumeUpdater()
    try:
        updater.get_code()
    except Exception as e:
        print(f"Caught Exception: {e}")

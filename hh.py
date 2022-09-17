import os
import sys
from time import sleep
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()


def get_tokens(code: str) -> dict:
    response = requests.post(url=token_url, data={"grant_type": "authorization_code",
                                                  "client_id": client_id,
                                                  "client_secret": client_secret,
                                                  "code": code})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get tokens. Status code: ", response.status_code)


def refresh_access_token(refresh_token: str) -> dict:
    response = requests.post(url=token_url, data={"grant_type": "refresh_token",
                                                  "refresh_token": refresh_token})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to refresh token. Status code: ", response.status_code)


def update(access_token: str):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.post(url=update_resume_url, headers=headers)
    return response.status_code


def update_resume(sleep_time: Optional[int] = 0, **kwargs):
    sleep(sleep_time)
    response_code = update(kwargs['access_token'])
    if response_code == 200:
        print('Success: Resume was updated')
        update_resume(sleep_time=60 * 60 * 4 + 60 * 1, **kwargs)
    if response_code == 429:
        print('Error: You are trying to update your resume too often')
        update_resume(1, **kwargs)
    if response_code == 403:
        print('Error: Token TTL has expired. Get a new token')
        refreshed = refresh_access_token(kwargs['refresh_token'])
        update_resume(**refreshed)
    raise Exception("Failed to update resume. Status code: ", response_code)


if __name__ == '__main__':
    try:
        redirect_url = os.getenv('REDIRECT_URL')
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        update_resume_url = f"https://api.hh.ru/resumes/{sys.argv[1]}/publish"
        token_url = "https://hh.ru/oauth/token"

        tokens = get_tokens(code=sys.argv[2])
        update_resume(**tokens)

    except Exception as e:
        print(f"Caught Exception: {e}")

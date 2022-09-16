from time import sleep
from typing import Optional
import requests
import hh

resume_id = hh.HHResumeUpdater.resume_id
access_token = hh.HHResumeUpdater.access_token
url = 'https://api.hh.ru/resumes/' + resume_id + '/publish'
headers = {'Authorization': 'Bearer ' + access_token}


def update_resume(sleep_time: Optional[int] = 0) -> None:

    sleep(sleep_time)
    r = requests.post(url, headers=headers)

    if r.status_code == 429:
        print('Error: ', 'You are trying to update your resume too often')
        update_resume(10 * 60)
    if r.status_code == 403:
        print('Error: ', 'Token TTL has expired. Get a new token on https://dev.hh.ru/admin/')
        exit(1)
    if r.status_code == 200:
        print('Success: ', 'Resume was updated')
        update_resume(60 * 60 * 4 + 60 * 1)


if __name__ == '__main__':
    try:
        update_resume()
    except Exception as e:
        print(f"Caught Exception: {e}")

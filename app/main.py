import asyncio
import datetime
import logging
import os
import sys
from asyncio import sleep

import aiohttp

import auth
logging.getLogger().setLevel(os.environ.get("LOG_LEVEL", logging.INFO))



async def update_resume(
        session: aiohttp.ClientSession,
        resume_id: str,
        access_token: str,
        refresh_token: str,
):
    while True:
        async with session.post(
                url=f"https://api.hh.ru/resumes/{resume_id}/publish",
                headers={'Authorization': 'Bearer ' + access_token}
        ) as response:
            match response.status:
                case 204:
                    # If update is successful
                    # Updating resume every 4 hours + 1 minute by default
                    logging.debug(f'Resume id={resume_id} updated successfully')
                    tts = 60 * 60 * 4 + 60
                    logging.debug(f'Sleeping for {datetime.timedelta(seconds=tts)}')
                    await sleep(tts)
                case 429:
                    # If updating is too often -> wait 10 min
                    logging.info(f'Resume id={resume_id} updates too often ')
                    tts = 60 * 10
                    logging.info(f'Sleeping for {datetime.timedelta(seconds=tts)}')
                    await sleep(tts)
                case 403:
                    logging.debug('Token expired. Getting a new token...')
                    access_token, refresh_token = await auth.refresh_tokens(refresh_token)
                case _:
                    resp = await response.json()
                    logging.error(resp)
                    raise Exception(f"Failed to update resume id={resume_id}. Status code: {response.status}")


async def main():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    code = os.environ.get("CODE", None)
    if code is None:
        logging.info(f"1) Go to link {auth.BASE_AUTH_URL + f'&client_id={client_id}'}")
        logging.info("2) Authorize")
        logging.info("3) Copy 'code' from url and add to .env 'CODE=<your_code>'")
        return
    try:
        access_token, refresh_token = await auth.get_tokens(code=code, client_id=client_id, client_secret=client_secret)
    except auth.NotAuthorizedError:
        logging.error(f"Wrong CODE. Refresh your .env {auth.BASE_AUTH_URL + f'&client_id={client_id}'}")
        return

    tasks = []
    async with aiohttp.ClientSession() as session:
        for resume_id in sys.argv[1:]:
            tasks.append(asyncio.create_task(
                update_resume(
                    session=session,
                    resume_id=resume_id,
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            ))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

import logging

import aiohttp

TOKEN_URL = "https://hh.ru/oauth/token"
BASE_AUTH_URL = "https://hh.ru/oauth/authorize?response_type=code"

class NotAuthorizedError(Exception):
    pass


async def get_tokens(code: str, client_id: str, client_secret: str) -> tuple[str, str]:
    form_data = aiohttp.FormData({
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    })
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=TOKEN_URL,
                data=form_data
        ) as response:
            if response.status == 200:
                logging.debug("Auth succeed!")
                resp = await response.json()
                return resp["access_token"], resp["refresh_token"]
            if response.status == 400:
                resp = await response.json()
                if resp["error_description"] == "code has already been used":
                    raise NotAuthorizedError("Code has already been used")
                if resp["error_description"] == "code not found":
                    raise NotAuthorizedError("Code not found")
            raise Exception("Failed to get tokens. Status code: ", response.status)


async def refresh_tokens(refresh_token: str) -> tuple[str, str]:
    form_data = aiohttp.FormData({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=TOKEN_URL,
                data=form_data
        ) as response:
            if response.status == 200:
                logging.debug("Tokens refreshed")
                resp = await response.json()
                return resp["access_token"], resp["refresh_token"]
            raise Exception("Failed to refresh token. Status code: ", response.status)

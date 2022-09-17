#  HeadHunter resume updater #

## Set up ##

1. Install dependencies
```bash
pip3 install -r requirements.txt
```
2. Create .env file
3. Place hhapp consts to .env file
```bash
REDIRECT_URL=some_redirect_url
CLIENT_ID=some_client_id
CLIENT_SECRET=some_client_secret
```
4. Get the code from redirect url
```
https://hh.ru/oauth/authorize?response_type=code&client_id=CLIENT_ID
```
5. Get resume_id from resume page url
6. Run script with following args
```
python hh.py <resume_id> <code>
```
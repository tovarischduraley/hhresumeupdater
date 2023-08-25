#  HeadHunter resume updater #

## Set up ##

1. Create HH App ([link](https://dev.hh.ru/admin/))
2. Autorize in https://hh.ru/oauth/authorize?response_type=code&client_id=<YOUR_CLIENT_ID>
3. Get CODE from URL after login
4. Create .env file with following variables
```
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   CODE=your_code
   RESUMES_IDS='resume_id_1 resume_id_2 resume_id_3'
```
5. Launch app
```bash
docker-compose up --build
```

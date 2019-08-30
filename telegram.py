import requests
from decouple import config

base = 'https://api.telegram.org'
token = config('TOKEN');
url = f'{base}/bot{token}/getUpdates'

res = requests.get(url)
data = res.json()

# 1. 내 chat_id 가져오기
chat_id = data['result'][0]['message']['chat']['id']

# 2. 해당하는 chat_id에 메시지 전송하기
message = '파이썬 어렵넹'
sendMessageUrl = f'{base}/bot{token}/sendMessage?text={message}&chat_id={chat_id}'

requests.get(sendMessageUrl)
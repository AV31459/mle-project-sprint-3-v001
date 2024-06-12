import requests
import time
import os
import random

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Максимальное число запросов в одном 'пакете'
MAX_REQUEST_VOLLEY = 100

# Максимальный таймаут между 'пакетами' запросов (сек)
MAX_TIMEOUT = 60

SEP = '-' * 40 + '\n'

# Адрес приложения
app_url = (
    f'http://{os.getenv("HOST_EXTERNAL")}:{os.getenv("APP_PORT_EXTERNAL")}'
    '/predict'
)

# Загружаем примеры валидных входных данных для запроса
with open(os.getenv('MODEL_X_EXAMPLE'), 'rb') as fd:
    x_example = pd.read_json(fd, orient='table')

print(f'Taregtng application at: {app_url}')

while True:
    volley_size = random.randint(0, MAX_REQUEST_VOLLEY)
    print(SEP + f'Firing a volley of {volley_size} requests... ', end='')

    for _ in range(volley_size):
        response = requests.post(
            app_url,
            json=x_example.sample().iloc[0].to_dict()
        )
        if response.status_code == 200:
            continue
        print('\n Наташа, мы его уронили...')
        print(f'Status code: {response.status_code}', end='')
        print(f'Body: {response.json()}')

    print('done.')

    sleep_time = random.randint(0, MAX_TIMEOUT)
    print(f'Sleeping for {sleep_time} seconds...')
    time.sleep(sleep_time)

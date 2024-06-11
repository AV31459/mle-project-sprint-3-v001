# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружении

**NB: ML-модель сохранена в версии python 3.10 (3.10.12). При тестировании сервиса (без docker контейнера) в другой версии python загрузка модели из cloudpickle-файла моежет работать некорректно.**

Находясь в корневой директории проекта:   
Устанавливаем и активируем виртуальное окружение, устанавливаем зависимости
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Для работы сервиса в файле `.env` должны быть заданы переменные окружения:
- APP_LOG_LEVEL
- MODEL_PATH
- MODEL_X_EXAMPLE
- MODEL_Y_EXAMPLE

Описание переменных и значения по умолчанию находятся в шаблоне `.env_example`.    
На основе шаблона `.env_example` cоздаем и, при необходимости, редактируем файл конфигурации `.env`.     
```
$ cp .env_example .env
$ vi .env
```
Запуск uvicorn сервера:
```
$ uvicorn --app-dir=app app:app --host=127.0.0.1 --port=7000
```
Альтернативный способ (в`.env` должны быть заданы HOST_EXTERNAL, APP_PORT_EXTERNAL)
```
$ python app/app.py
```
Пример сurl запросов для проверки работоспособности сервиса:
```
$ curl http://localhost:7000/healthcheck
$ curl -X POST http://localhost:7000/predict -H "Content-Type: application/json" -d "@tests/request_example.json"
```
Работоспособность сервиса можно также проверить с помощью скрипта `tests/ping_app.sh`
```
$ chmod +x tests/ping_app.sh        # один раз, перед первым запуском
$ ./tests/ping_app.sh localhost:7000
```
*Опционально: интерфейс и порт можно не указывать, скрипт возьмет значения из переменных HOST_EXTERNAL, APP_PORT_EXTERNAL.*

### 2. FastAPI микросервис в Docker-контейнере

#### 2.1 Ручная сборка и запуск контейнера 

В файле `.env` в дополенение к переменным, указанным в п.1, должно быть задан значение для APP_PORT_DOCKER.    
Для ручной сборки образа и запуска контейнера с приложением в корне проекта выполняем команды:
```
$ docker image build -f Dockerfile_app -t fastapi_app .
$ docker container run -it -p 7000:7000 -v ./models:/fastapi_app/models --env-file .env --rm fastapi_app
```
 NB: Последня команда предполагает, что порт приложения в контейнере APP_PORT_DOCKER=7000. 

#### 2.2 Сборка и запуск контейнера с помошью `docker compose`
В дополенение к переменным, указанным выше, в файле `.env` должен быть заданы HOST_EXTERNAL, APP_PORT_EXTERNAL.    
В корне проекта выполняем команду:
```
$ docker compose -f docker-compose.single_app.yaml up --build
```
Пример json-запроса, корректно обрабатываемого сервисом, находится в файле `tests/request_example.json`, соответствующая curl команда приведена выше.

### 3. Микросервис с системами мониторинга в Docker-контенерах

Для запуска сервиса совместно с системами prometheus/grafana проверьте наличие в файле `.env` значений для переменных:
- PROMETHEUS_PORT_EXTERNAL
- GRAFANA_PORT_EXTERNAL
- GRAFANA_USER
- GRAFANA_USER_PASSWORD

**NB: Так как peomehteus не поддерживает переменные окружения в конфигурационных файлах, убедитесть, что значения порта микросервиса в конфигурационном файле `prometheus/prometheus.yml` соответсвтует значению APP_PORT_DOCKER, указанному в `.env`:**
```
    static_configs:
    - targets:
      - fastapi_app:7000 <--- должно совпадать с APP_PORT_DOCKER
```

В корне проекта выполняем команду:
```
$ docker compose up --build
```
После запуска docker контейнеров, микросервис и prometheus/grafana должны бть доступны по адресу HOST_EXTERNAL на портах указанных в env-переменных:
- APP_PORT_EXTERNAL  (внешний порт миросервиса)
- PROMETHEUS_PORT_EXTERNAL (внешний порт prometheus)
- GRAFANA_PORT_EXTERNAL (внешний порт grafana)

*Описание переменных с примером заполенния находится в шаблоне `.env_example`.* 

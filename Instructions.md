# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружении

**NB: Python-модель сохранена/протестирована в версии python 3.10 (3.10.12). При использовании другой версии python загрузка модели (в формате cloudpickle) моежет работать некорректно.**

Находясь в корневой директории проекта:   
Устанавливаем и активируем виртуальное окружение, устанавливаем зависимости
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Для работы сервиса в виртуальном окружении в файле `.env` должны быть заданы переменные:
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
Альтернативный способ (NB: в `.env` должны быть дополнительно заданы APP_HOST_DOCKER, APP_PORT_DOCKER)
```
$ python app/app.py
```
Пример сurl запросов для проверки работоспособности сервиса:
```
$ curl http://localhost:7000/healthcheck
$ curl -X POST http://localhost:7000/predict -H "Content-Type: application/json" -d "@tests/request_example.json"
```

### 2. FastAPI микросервис в Docker-контейнере

#### 2.1 Ручная сборка и запуск контейнера 

В файле `.env` в дополенение к переменным, указанным в п.1, должны быть заданы APP_HOST_DOCKER, APP_PORT_DOCKER.    
Для ручной сборки образа и запуска контейнера с приложением в корне проекта выполняем команды:
```
$ docker image build -f Dockerfile_app -t fastapi_app .
$ docker container run -it -p 7000:7000 -v ./models:/fastapi_app/models --env-file .env --rm fastapi_app
```
 NB: Последня команда предполагает, что порт приложения в контейнере APP_PORT_DOCKER=7000. 

#### 2.2 Сборка и запуск контейнера с помошью `docker compose`
В дополенение к переменным, указанным выше, в файле `.env` должен быть задан внешний порт прилоения APP_PORT_EXTERNAL
В корне проекта выполняем команду:
```
$ docker compose up  --build
```
Пример json-запроса, корректно обрабатываемого сервисом, находится в файле `tests/request_example.json`, соответствующая curl команда приведена выше.



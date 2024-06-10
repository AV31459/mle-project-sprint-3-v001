# Инструкции по запуску микросервиса

**NB** Python-модель сохранена/протестирована в версии python 3.10 (3.10.12). В другой версии python загрузка модели (в формате cloudpickle) моежет работать некорректно. 

### 1. FastAPI микросервис в виртуальном окружении

Находясь в корневой директории проекта:   
Устанавливаем и активируем виртуальное окружение, устанавливаем зависимости
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для работы сервиса в виртуальном окружении в файле `.env` должны быть заданы переменные:
- APP_LOG_LEVEL
- MODEL_PATH
- MODEL_X_EXAMPLE
- MODEL_Y_EXAMPLE

Описание переменных и значения по умолчанию находятся в шаблоне `.env_example`.    
На основе шаблона `.env_example` cоздаем и, при необходимости, редактируем файл конфигурации `.env`.     
```
cp .env_example .env
vi .env
```
Запуск uvicorn сервера:
```
uvicorn --app-dir=app app:app --host=127.0.0.1 --port=7000
```
Альтернативный способ (в `.env` должны быть дополнительно заданы APP_HOST_DOCKER, APP_PORT_DOCKER)
```
python app/app.py
```
Пример сurl запроса для проверки работоспособности сервиса:
```
curl -X POST http://localhost:7000/predict -H "Content-Type: application/json" -d "@tests/request_example.json"
```

### 2. FastAPI микросервис в Docker-контейнере
...

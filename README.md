# Проект - релиз ML-модели в production

### Постановка задачи
На входе имеем разаработанную/протестированную ML модель в формате сохраненного python объекта и примеры входных/выходных данных.   
Задача состоит в написании и развертывании web-микросервиса предоставляющего API для данной модели.

### Реализованные этапы
1. Разработан FastAPI web-микросервис, который:
    - принимает и валидируует входные запросы к модели в формате json
    - рассчитывает предсказание модели и возвращает результат в формате json
    - имеет автоматически сгенерированную документацию и примеры входных/выходных данных.
2. Написаны конфигруационные файлы для запуска микросервиса в docker контейнере.
3. Написаны конфигруационные файлы docker-compose для запуска микросервиса совместно с системами мониторинга Prometheus/Grafana. 
4. Написан скрипт, симулирующий нагрузку на микросервис. Выбраны метрики для мониторинга работы микросервиса и cоздан grafana-дашборд для их отображения.

Инструкции по запуску и работе с сервисом находятся в файле `Instructions.md`


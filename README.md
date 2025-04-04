### Структура
* ```auth```: сервис регистрации и аутентификации пользователей
    - ```entrypoints```: точки входа
      - ```flask_entrypoint```: точка входа для flask
        - ```__init__.py```: инициализация приложения flask
        - ```auth_user.py```: аутентификация (flask_jwt_extended) 
        - ```http_errors.py```: определение исключения для слоя web 
        - ```run_flask_app.py```: запуск приложения flask
        - ```views.py```: обработчики HTTP-запросов
    - ```service_layer.py```: служебный слой
      - ```manager.py```: прием входящих данных и зависимостей, вызовы, возрат результатов
      - ```unit_of_work.py```: абстракция атомарной операции 
      - ```validation_and_pass_hashing```
        - ```pass_hashing.py```: хеширование паролей
        - ```validation.py```: валидация входящих данных
* ```domain```: бизнес логика:
    - ```models```: модели (классы python, не таблицы БД)
    - ```services```: операции с моделями
    - ```custom_errors```: исключения (часть бизнес-логики)
* ```orm_tool```: абстракция над ORM
    - ```__init__.py```: инициализация БД, вызов мэппера моделей с таблицами БД
    - ```drop_create.py```: удаление и создание таблиц БД
    - ```table_mapper.py```: мэппер моделей с таблицами БД
* ```repository```: абстракция постоянного хранилища и методов доступа к нему
* ```tests```: тесты
* ```oas.yml```: OpenAPI-спецификация
### Запуск
* создать файл `.env` в корне проекта (образец: `.env.example`)
* запуск PostgreSQL, PGAdmin в docker-контейнерах:\
$ `docker-compose up -d`
* запуск приложения flask из корневой директории проекта:
```bash
python3 -m auth.entrypoints.flask_entrypoint.run_flask_app
```
    
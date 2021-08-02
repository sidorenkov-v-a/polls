# [Polls](http://84.201.162.201/)
## [Проект доступен на облачном сервере](http://84.201.162.201/)
Login: admin  
Pass: admin

**Система API для опросов пользователей.**  
*Функционал для администратора системы:*
- Авторизация в системе
- Добавление/изменение/удаление опросов.
- Добавление/изменение/удаление вопросов в опросе.

*Функционал для пользователей системы:*
- Получение списка активных опросов
- Прохождение опроса
- Получение пройденных пользователем опросов с детализацией по ответам

**Документация доступна на главной странице сервиса**

## Запуск приложения:
1) [Установите Docker](https://www.docker.com/products/docker-desktop)
2) [Установите docker-compose](https://docs.docker.com/compose/install/)
3) Клонируйте репозиторий с проектом:
```
git clone https://github.com/sidorenkov-v-a/polls.git
```
3) В корневой директории проекта создайте файл `.env`, в котором пропишите переменные окружения  
>Список необходимых переменных можно найти в файле `.env.example`
4) Перейдите в директорию проекта и запустите приложение
```
docker-compose up
```
5) Дополнительные возможности:
- Войдите в контейнер
```
docker exec -it polls_web_1 bash
```
- Создайте суперпользователя
```
python manage.py createsuperuser
```
- Используйте тестовые данные
```
python manage.py loaddata fixtures.json 
```

## Стек технологий:   
- Django framework 2.2.10
- Django rest framework 3.12.4
- PostgreSQL 12.4
- Gunicorn 20.1.0
- Nginx 1.19.0
- Docker, docker-compose
- Swagger

#### Об авторе:
[Профиль Github](https://github.com/sidorenkov-v-a/)  
[Telegram](https://t.me/sidorenkov_vl)

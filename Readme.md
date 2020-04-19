Прект на Heroku: https://e9-todo-home.herokuapp.com/

Для запуска локально:

Создаем контейнер с БД: docker run --rm  --name flask-db -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres:12-alpine 

Создаем БД в контейнере:  docker exec -it flask-db psql -U postgres -c "create database todo_home"

git clone https://github.com/Artromterra/e9-todo-home.git

Входим в директорию проекта.

Создаем вирт. окружение

pip3 install -r requirements.txt

python3 manage.py db migrate

python3 manage.py db upgrade

python3 manage.py runserver

Активируем виртуальное окружение
Создаем контейнер с БД: docker run --rm  --name flask-db -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres:12-alpine 
export FLASK_APP=todo.py
Создаем БД в контейнере:  docker exec -it flask-db psql -U postgres -c "create database todo_home"
export DATABASE_URL=postgresql://postgres:docker@localhost:5432/todo_home
Для дебаггера пишем export FLASK_ENV=development
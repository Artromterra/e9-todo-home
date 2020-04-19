release: python manage.py db migrate
release: python manage.py db upgrade
web: gunicorn -b $HOST:$PORT app:app
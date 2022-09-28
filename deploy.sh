python manage.py makemigrations
python manage.py migrate
daphne -b 0.0.0.0 -p $PORT forex_bot_api.asgi:application
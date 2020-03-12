web: gunicorn tinderforedu.wsgi --log-file -
web2: daphne tinderforedu.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
web3: python manage.py runserver
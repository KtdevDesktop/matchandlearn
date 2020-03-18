web: daphne tinderforedu.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT celery worker --app tinderforedu.celery.app --loglevel info
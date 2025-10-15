
release: python manage.py collectstatic --noinput

web: gunicorn BeyonceVotingSite.wsgi --bind 0.0.0.0:$PORT

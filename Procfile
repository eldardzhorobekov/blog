db: python src/manage.py makemigrations && python src/manage.py migrate && python src/manage.py loaddata fixtures/data.json
web: cd src && gunicorn src.wsgi

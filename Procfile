web: gunicorn deploy:app

web: cd project; python manager.py db migrate; gunicorn "app:create_app()"
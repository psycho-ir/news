cd ..
gunicorn -p core_pid  -b localhost:9000 -D  news.production_core_wsgi
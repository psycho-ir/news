cd ..
gunicorn -w 2 --threads 2 -p web_pid -b localhost:8000 -D  news.production_wsgi
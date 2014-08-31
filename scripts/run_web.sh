cd ..
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
gunicorn -w 3 -p web_pid --error-logfile=log/gunicorn_web.log -b localhost:8000 -D  news.production_wsgi
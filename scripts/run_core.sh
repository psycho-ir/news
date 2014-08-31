cd ..
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
gunicorn -p core_pid  -b localhost:9000 --error-logfile=log/gunicorn_core.log -D  news.production_core_wsgi
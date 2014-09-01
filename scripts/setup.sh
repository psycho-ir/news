export DJANGO_SETTINGS_MODULE=news.production_settings
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
python2.7 ../manage.py syncdb
python2.7 ../manage.py migrate
python2.7 ../manage.py collectstatic
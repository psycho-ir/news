export DJANGO_SETTINGS_MODULE=news.production_settings
python2.7 ../manage.py syncdb
python2.7 ../manage.py migrate
python2.7 ../manage.py collectstatic
cd /var/www/sparbee_web
git pull
/bin/bash /var/www/venv_sparbee/bin/activate
python manage.py collectstatic
python manage.py migrate
service apache2 restart
deactivate

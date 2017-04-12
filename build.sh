cd /var/www/sparbee_web
git pull
source /var/www/venv_sparbee/bin/activate
python manage.py collectstatic
service apache2 restart
deactivate

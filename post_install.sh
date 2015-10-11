

cd /var/www/unifispot

if [ ! -f config.yaml ]; then
    cp example.yaml config.yaml
fi 

if [ ! -f config/database.db ]; then
    env/bin/python manage.pyc db init
    env/bin/python manage.pyc db migrate
    env/bin/python manage.pyc db upgrade
fi

if [ ! -f /etc/apache2/sites-available/unifispot.conf ]; then
    cp unifispot.conf /etc/apache2/sites-available/
    a2ensite unifispot.conf 
fi
chown www-data:www-data -R /var/www/unifispot
service apache2 restart
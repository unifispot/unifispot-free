echo "---delete all files and folders----"
rm -rf migrations 


rm config/database.db

echo "-----Initialize all DBs------------"
python manage.py db init
python manage.py db migrate
python manage.py db upgrade



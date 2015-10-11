echo "---delete all files and folders----"
rmdir migrations /s /q


del config\database.db
echo "-----Initialize all DBs------------"
python manage.py db init
python manage.py db migrate
python manage.py db upgrade








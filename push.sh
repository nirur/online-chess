python3 manage.py collectstatic --no-input
python3 manage.py compilestatic
python3 manage.py collectstatic --no-input
git add .
git commit -m "Making changes for staticfiles and display"
git push -u origin master
heroku logs --tail -a onlinechess1
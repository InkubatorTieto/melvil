flask create_admin

if [ "$1" = "-p" ] ; then
    gunicorn --bind=0.0.0.0:8000 app:create_app\(\)
else
    flask run --host=0.0.0.0
fi
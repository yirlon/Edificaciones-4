
set -o errexit

#poetry install 

# pip install -r requirements.txt

#pip intall pypiwin32==304

python manage.py collectstatic --no-input
python manage.py migrate
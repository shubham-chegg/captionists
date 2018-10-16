# How to setup
```sh
$> brew install ffmpeg
$> git clone git@github.com:shubham-chegg/captionists.git
$> cd captionists
$> python -m virtualenv .venv
$> source .venv/bin/activate
$> pip install requirements.txt
$> python manage.py migrate
$> python manage.py runserver
```
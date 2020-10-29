# Car voting API

## Requirements for launching the app
* Docker
* Docker Compose

## Launching the app
### Docker
1. Copy .env.template to .env and edit it to your liking
2. docker-compose up

### Baremetal
1. Modify settings.py to change the database to SQLite3 or other db
2. Create a venv and add packages from requirements.txt or `pip install -r requirements.txt`
3. manage.py runserver
# collaboratory
It tried to make a clone of stackoverflow and also tried to use formsets
### Getting It 
Creating virtual environment 
> virtualenv -p python3 venv

Activating virtual environment
> source venv/bin/activate

Clone the git repository and move to that directory
> git clone https://github.com/madhu0309/collaboratory.git

### Installing requirements 

> pip install -r requirements.txt

### Set mailid and password

Set mailid in the place of os.getenv("USER") and password in the place of os.getenv("PASSWORD")

>EMAIL_HOST_USER = os.getenv("USER")

>EMAIL_HOST_PASSWORD = os.getenv("PASSWORD")

### Run migrations 

> python manage.py migrate

### Collectstatic

> python manage.py collectstatic

### Redis

Install redis server https://redis.io/download

Run redis server
>$ redis-server

Run celery
> celery -A collab_project worker -l info

### Run server

> python manage.py runserver

# WebChat with `django` and `channels`

### Requirements
 * Python 3.6+
 * Redis server (or docker)


### Setup your local environment


#### Clone this repo and cd into it
```bash
git clone git@github.com:maylonpedroso/webchat.git
cd webchat
```

#### Setup a virtual environment
```bash
python3 -m venv venv
source venv/bin/activete
```

#### Run the migrations to create the local DB

```bash
./manage.py migrate
```

#### Run the app
```bash
./manage.py runserver
```

Go to [http://127.0.0.1:8000]() and check the webchat

### Run chat bots

```bash
./manage.py runbots
```

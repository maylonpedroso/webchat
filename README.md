# WebChat with `django` and `channels`

This web chat application was created using django channels. 
Also includes a management command to link available chat bots to all 
already existent rooms.

### Requirements
 * Python 3.6+
 * Redis server

### Setup your local environment

#### Run redis server
This project is setup to use a channel layer with Redis backend. If you don't have
redis-server on port 6379 an easy way of get it running is with docker.
```bash
docker -d -p 6379:6379 redis:latest
```

#### Clone this repo and `cd` into it
```bash
git clone git@github.com:maylonpedroso/webchat.git
cd webchat
```

#### Setup a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
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
**Important:** If a new chat room is created the `runbots` command needs to be restarted 

### Running the tests
```
./manage.py test
```
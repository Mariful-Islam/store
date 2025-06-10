# Store Management System

## Clone respository
clone the gtihub repo from github 

```zsh
    git clone git@github.com:Mariful-Islam/store.git
```

## Create virtual environment 
```zsh
    python -m venv env
```
or

```zsh
    virtualenv env
```

## Activate virtual enviroment

For mac or linux
```zsh
    source env/bin/activate
```

For windows

```zsh
    source env/Scripts/activate
```

## Install requirements.txt 
```zsh
    pip install -r requirements.txt
```

## Database setup
```zsh
    python manage.py makemigrations
```
```zsh
    python manage.py migrate
```

## Run django server

```zsh
    python manage.py runserver
```



Then visit the link http://127.0.0.1:8000

To get swagger api documentation 
http://127.0.0.1:8000/swagger/

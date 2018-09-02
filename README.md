# Facio
Simple To-Do app with Django using TDD

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* **Make sure you have pip installed on your machine.**
* And make sure you are running python 3.6

### Installing

A step by step series of examples that tell you have to get a development env running

* Install virtualenv (not mandatory)

```
pip install virtualenv
```

* Create a virtualenviroment  

```
virtualenv env_name -p python3.6
```

* Open the folder created  

```
cd env_name/ && source bin/activate
```

* after clone this project run

```
pip install requirements.txt
```

## Create database

```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Create a super user

```
python manage.py create_superuser
```

## Run the local server

```
python manage.py runserver
```

## Running the tests

```
python manage.py test
```

## Built With

* [Django 1.11](https://www.djangoproject.com/) - The web framework used
* [pip](https://pypi.python.org/pypi/pip) - Package Management

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

- 

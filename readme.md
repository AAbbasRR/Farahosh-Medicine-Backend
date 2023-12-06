## Farahosh Medicines Backend :rocket:

env variables:

    :information: [Variables marked with * are mandatory and must be present in the .env file]

    # ___Project Setup___ #
    SECRET_KEY = string *
    DEBUG = bollean[default=True]
    ACCESS_TOKEN_LIFETIME = int[default=1 hour]

    # __Redis Setup__ #
    REDIS_HOST = url[default=localhost]
    REDIS_PORT = int[default=6379]
    REDIS_DB = int[default=0]

    # ___Database___ #
    USE_MYSQL = boolean[default=False]
    MYSQL_NAME = string(if USE_MYSQL is true, need to set this variable.)
    MYSQL_USER = string(if USE_MYSQL is true, need to set this variable.)
    MYSQL_PASS = string(if USE_MYSQL is true, need to set this variable.)
    MYSQL_HOST = url(if USE_MYSQL is true, need to set this variable.)
    MYSQL_PORT = int(if USE_MYSQL is true, need to set this variable.)
    DEPENDENT_EMAIL_ON_DEBUG = bool[default=True](in debug mode all email messages managing on console, if you want receiving email messages in debug mode setting this variable to False)

    USE_POSTGRES = boolean[default=False]
    POSTGRES_NAME = string(if USE_POSTGRES is true, need to set this variable.)
    POSTGRES_USER = string(if USE_POSTGRES is true, need to set this variable.)
    POSTGRES_PASS = string(if USE_POSTGRES is true, need to set this variable.)
    POSTGRES_HOST= url(if USE_POSTGRES is true, need to set this variable.)
    POSTGRES_PORT = int(if USE_POSTGRES is true, need to set this variable.)

    DEFAULT_DATABASE_NAME = str[set mysql or postgresql]

    # __sms portal[raygansms]__ #
    SMS_PORTAL_USERNAME = string *
    SMS_PORTAL_PASS = string *
    DEPENDENT_SMS_ON_DEBUG = bool[default=True](in debug mode all sms messages managing on console, if you want receiving sms messages in debug mode setting this variable to False)


docker env variables:

    # db - postgresql #
        POSTGRES_USER = string *
        POSTGRES_PASSWORD = string *
        POSTGRES_DB = string

:question:

    For install pre-commit configuration on your git:
        pre-commit install


How To Run Docker :question:

    docker-compose up -d

How To Run Locally :question:

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver or gunicorn src.config.wsgi:application --bind 0.0.0.0:8000


    for create default medecines from csv file:
        in src directory, run below command:
            python manage.py createmedicines

    for install redis:
        linux - ubuntu
            sudo apt-get install redis-server
            sudo service redis-server start
        windows:
            Step 1: Turn on Windows Subsystem for Linux
                Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
            Step 2: Launch Microsoft Windows Store
                start ms-windows-store:
            Step 3: Install Redis server
                sudo apt-add-repository ppa:redislabs/redis sudo apt-get update sudo apt-get upgrade sudo apt-get install redis-server




For Run Test Project Service :sparkles:

    python manage.py test --pattern="tests_*.py"

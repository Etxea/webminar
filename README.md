Webminar
=====================

Install:
    sudo apt-get install libmysqlclient-dev git-core python-pip virtualenv python-dev
    git clone https://github.com/Etxea/webminar
    pip install virtualenv
    virtualenv webminar
    cd webminar
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver

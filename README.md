# Codeforces Filter

This application helps you to filter codeforces problems in a better way.

# Getting Started

To get started open terminal and follow the commands.

    mkdir CF_Filter
    cd CF_Filter
    virtualenv venv --python=python3.5
    
If you don't have `virtualenv` installed locally you can install it by typing `sudo apt-get install virtualenv`.

Now, clone the project to you local directory.

    git clone https://github.com/rofi93/CF_Filter.git

Upon completion activate virtual environment and install requirements.

    source venv/bin/activate
    pip3 install -r requirements.txt
    
Now, create [Postgresql](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04) 
database necessary for the project and move to project directory and run.

    cd CF_Filter
    python3 manage.py migrate
    python3 manage.py crontab add
    python3 manage.py runserver
    

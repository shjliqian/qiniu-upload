 qiniu-upload
==============
A simple register page that can upload images to qiniu cloud
## Usage:
* $ git clone https://github.com/williezh/qiniu-upload
* $ cd qiniu-upload
* $ virtualenv --python=python2.7 venv
* $ source venv/bin/activate
* $ pip install -r requirements.txt
* $ cp yuntest/local_settings_sample.py yuntest/local_settings.py
* $ vi yuntest/local_settings.py #set the database,email and qiniu

After change the local_settings into yours
init the database and runserver

* $ python createdatabase.py
* $ python manage.py makemigrations
* $ python manage.py migrate
* $ python manage.py runserver

and then open the site: [127.0.0.1:8000](127.0.0.1:8000)

you will see the page where input a Username and 
click 'Choose File' to upload image and submit it,then you can
see the result and the image will be store at qiniu cloud.

 qiniu-upload
==============
A register page that can upload images to qiniu cloud
## Usage:
* $ git clone https://github.com/williezh/qiniu-upload
* $ cd qiniu-upload
* $ cp local_settings_sample.py local_settings.py

then change the configures into yours
after that performan like this(use python2.7)

* $ python manage.py makemigrations
* $ python manage.py migrate
* $ python manage.py runserver

and then open the site: 127.0.0.1:8000
you can see the page and upload your file to qiniu cloud

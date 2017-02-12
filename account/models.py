#coding=utf-8
from __future__ import unicode_literals

from django.db import models

# 这里的上传路径就是mysite/upload/xxx.jpg
class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    headImg = models.CharField(max_length=120)

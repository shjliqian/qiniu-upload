#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django import forms
from .models import User
from qiniuyun.backend import QiniuPush
import os

# 创建一个form表单类
class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()

# 第一次打开页面不是POST请求，所以走else那条路，创建一个form表单，然后在前台显示。
# 第二次点击“提交”按钮是POST请求，走if那条路：意思就是这个表单请求内容有files文件，
# 然后如果它们有数据，就存到数据库中，并且把用户名放在`session`中，最后跳转到一个新的url去。
def signup(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            uname = uf.cleaned_data['username']
            hImg = uf.cleaned_data['headImg']
#            L=[settings.BASE_DIR,'media','upload',hImg.name]
#            filePath=os.sep.join(L)
#            with open(filePath,'wb') as wf:
#                for chrunk in hImg.chunks():
#                    wf.write(chrunk)            
            hImg_qiniu= QiniuPush.put_data(hImg.name,hImg)            
            u = User()
            u.username = uname
            u.headImg = hImg_qiniu            
            u.save()
            request.session['user_name'] = uname
            return HttpResponseRedirect('/signup/done/')
    else:
        uf = UserForm()
    return render(request, 'account/signup.html', {'uf': uf})

# 从session中找到这个用户名，按照用户名找到数据库中的用户信息，把用户信息展示出来。
def signup_result(request):
    uuu = User.objects.get(username=request.session['user_name'])
    return render(request, 'account/signup_result.html', {'user': uuu})

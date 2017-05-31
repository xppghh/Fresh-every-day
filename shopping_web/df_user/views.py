#coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *

# Create your views here.

def register(request):
    return render(request,'store/register.html')
def register_handle(request):
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    if upwd != upwd2:
        return redirect('/store/register.html')
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    return render(request,'store/login.html')

def login(request):
    return render(request,'store/login.html')
def login_handle(request):
    post=request.POST
    name=post.get('username')
    pwd=post.get('pwd')
    s1=sha1()
    s1.update(pwd)
    spwd=s1.hexdigest()
    suser=UserInfo.objects.filter(uname=name,upwd=spwd)
    if len(suser) == 0: #不能是if suser==[]
        return redirect('/login.html')
    else:
        return render(request,'store/index.html')

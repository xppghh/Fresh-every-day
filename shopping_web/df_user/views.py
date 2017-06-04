#coding=utf-8
from django.shortcuts import render,redirect
from hashlib import sha1
from models import *
from django.http import JsonResponse,HttpResponseRedirect
import user_decorator

# Create your views here.

def register(request):
    context={'title':'注册'}
    return render(request,'store/register.html',context)
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
def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context={'title':'登陆','username':uname}
    return render(request,'store/login.html',context)
def login_handle(request):
    post=request.POST
    name=post.get('username')
    pwd=post.get('pwd')
    jizhu=post.get('jizhu',0)

    suser=UserInfo.objects.filter(uname=name)
    if len(suser) == 1: #不能是if suser==[]
        s1 = sha1()
        s1.update(pwd)
        if s1.hexdigest() == suser[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 成功后删除转向地址，防止以后直接登录造成的转向
            red.set_cookie('url', '', max_age=-1)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', name)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = suser[0].id
            request.session['user_name'] = name
            request.session.set_expiry(0)
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'username': name, 'pwd': pwd}
            return render(request, 'store/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 1, 'username': name, 'pwd': pwd}
        return render(request, 'store/login.html', context)
def logout(request):
    request.session.flush();
    return redirect('/')

@user_decorator.login
# zhuangshi=login(user_center_info)

#user_center_info=login(user_center_info)
#user_center_info()
def user_center_info(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    context={'user':user,'title':'用户中心'}
    return render(request,'store/user_center_info.html',context)

@user_decorator.login
def user_center_order(request):
    context={'title':'用户中心'}
    return render(request,'store/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        submitinfo=request.POST
        user.ushou=submitinfo.get('ushou')
        user.uaddress=submitinfo.get('uaddress')
        user.uyoubian=submitinfo.get('uyoubian')
        user.uphone=submitinfo.get('uphone')
        user.save()
    context={'user':user,'title':'用户中心'}
    return render(request,'store/user_center_site.html',context)

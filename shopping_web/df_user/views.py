from django.shortcuts import render,redirect
from hashlib import sha1

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

def login(request):
    return render(request,'store/login.html')

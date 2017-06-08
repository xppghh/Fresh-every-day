#coding=utf-8
from django.shortcuts import render
from df_cart.models import CartInfo

# Create your views here.

def index(request):

    if request.session['user_id'] != '':
        cart_count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        cart_count=0
    context={'title':'首页','cart_count':cart_count}
    return render(request,'store/index.html',context)


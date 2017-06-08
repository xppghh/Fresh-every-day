#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.http import JsonResponse
from df_user import user_decorator
from df_goods.models import GoodsInfo

# Create your views here.
# @user_decorator
@user_decorator.login
def cart(request):
    carts=CartInfo.objects.filter(user_id=request.session['user_id'])
    if request.session['user_id'] == '':
        cart_count=0
    else:
        cart_count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
    context={'title':'我的购物车','cart_count':cart_count,
             'carts':carts}
    return render(request,'store/cart.html',context)

@user_decorator.login
def add(request,gid,count):
    uid=request.session['user_id']
    gid=int(gid)
    count=int(count)
    goods=CartInfo.objects.filter(goods_id=gid)

    if len(goods)==0:
        cart=CartInfo()
        cart.goods_id=gid
        cart.user_id=uid
        cart.count=count
        cart.save()
    else:
        # cart=goods[0]
        print goods[0].count
        goods[0].count=goods[0].count+count
        print goods[0].count
        goods[0].save()
    if request.is_ajax():
        num=CartInfo.objects.filter(user_id=uid).count()
        data={'count':num}
        return  JsonResponse(data)
    else:
        return redirect('/cart/')

def numadd(request,gid,count):
    count=int(count)
    carts=CartInfo.objects.filter(goods_id=gid)
    print (type(carts))

    print carts[0].__dict__
    print (type(carts[0]))

    cart=carts[0]

    print cart.__dict__
    print (type(cart))

    cart.count=count
    cart.save()
    return JsonResponse({'count':count})

def delete(request,gid):
    carts=CartInfo.objects.filter(goods_id=gid)
    carts[0].delete()
    cart_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    return JsonResponse({'cart_count':cart_count})



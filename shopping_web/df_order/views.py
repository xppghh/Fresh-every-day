#coding=utf-8
from django.shortcuts import render,redirect
from df_cart.models import CartInfo
from df_user.models import UserInfo
from datetime import datetime

from models import OrderInfo,OrderDetailInfo

from django.http import HttpResponse
from django.db import transaction
# Create your views here.

def place_order(request):
    user_id=request.session['user_id']
    users=UserInfo.objects.get(id=user_id)
    cart_id=request.GET.getlist('cart_id')
    carts=CartInfo.objects.filter(id__in=cart_id)
    context={'title':'提交订单','page_name':1,
             'users':users,'carts':carts}
    return render(request,'store/place_order.html',context)

@transaction.atomic
def order(request):
    now = datetime.now()
    uid=request.session['user_id']
    user_name=UserInfo.objects.get(id=uid)
    address=request.POST.get('address')
    cart_id=request.POST.getlist('cart_id')
# 订单
    sid = transaction.savepoint()
    try:
        order=OrderInfo()
        order.oid='%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user=user_name
        order.oaddress=address
        order.oIsPay=False
        order.odate=now
        order.ototal=0
        order.save()

    #详细订单
        totalprice=0
        carts=CartInfo.objects.filter(id__in=cart_id)
        for cart in carts:

            if cart.goods.gkucun >= cart.count:
                # 库存足够，可以购买
                # 减少库存量
                cart.goods.gkucun -= cart.count
                cart.goods.save()

                orderdetail = OrderDetailInfo()
                orderdetail.goods=cart.goods
                orderdetail.order=order
                orderdetail.price=cart.goods.gprice
                orderdetail.count=cart.count
                orderdetail.save()

                totalprice += cart.goods.gprice * cart.count
                # 删除购物车数据
                cart.delete()
            else:
            # 库存中够，中止此次下单
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            # 保存总价
        order.ototal = totalprice
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/show_order/')
    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

    # return render(request,'store/user_center_order.html')

def show_order(request):
    orders=OrderInfo.objects.all()
    #orderdetails_list=[]
    # for order in orders:
    #     orderdetails=order.orderdetailinfo_set.all()
    #     orderdetails_list.append(orderdetails)
    #     print orderdetails[0].count
    context={'title':'全部订单','orders':orders}
    return render(request,'store/user_center_order.html',context)
def pay(request,oid):
    # oid=request.GET.get('oper_btn')
    orde=OrderInfo.objects.get(oid=oid)
    orde.oIsPay=True
    orde.save()


    orders = OrderInfo.objects.all()
    context = {'title': '全部订单', 'orders': orders}
    return render(request,'store/user_center_order.html',context)
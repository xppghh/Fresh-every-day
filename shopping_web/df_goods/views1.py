#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator

def index(request):
    typelist=TypeInfo.objects.all()
    type0=typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01=typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1=typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11=typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2=typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21=typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3=typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31=typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4=typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41=typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5=typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51=typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context={'title':'首页','type0':type0,'type01':type01,
             'type1':type1,'type11':type11,'type2':type2,'type21':type21,
             'type3':type3,'type31':type31,'type4':type4,'type41':type41,
             'type5':type5,'type51':type51}
    return render(request,'store/index2.html',context)

def list1(request,pid,pIndex,sort):
    typelist=TypeInfo.objects.get(id=int(pid))
    news=typelist.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods=typelist.goodsinfo_set.order_by('-id')
    elif sort == '2':
        goods =typelist.goodsinfo_set.order_by('gprice')
    else:
        goods=typelist.goodsinfo_set.order_by('-gclick')
    # 将地区信息按一页10条进行分页
    paginator = Paginator(goods, 10)

    # 通过url匹配的参数都是字符串类型，转换成int类型
    pIndex = int(pIndex)
    # 获取第pIndex页的数据
    page = paginator.page(pIndex)
    context={'title':typelist,'news':news,
             'page':page,'paginator':paginator,
             'typelist':typelist,'sort':sort}
    return render(request,'store/list1.html',context)

def detail1(request,pid):
    goods=GoodsInfo.objects.get(id=int(pid))
    news=GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]

    context={'title':goods.gtype,'goods':goods,'news':news,
             'id':goods.id}

    return render(request,'store/detail1.html',context)
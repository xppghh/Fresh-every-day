#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from df_cart.models import CartInfo


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

    #如果user_id不存在则设置为空
    request.session.setdefault('user_id','')
    if request.session['user_id'] != '':
        cart_count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        cart_count=0
    context={'title':'首页','cart_count':cart_count,'type0':type0,'type01':type01,
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
    if request.session['user_id'] =='':
        cart_count=0
    else:
        cart_count=CartInfo.objects.filter(user_id=request.session['user_id']).count()

    context={'title':typelist,'cart_count':cart_count,'news':news,
             'page':page,'paginator':paginator,
             'typelist':typelist,'sort':sort}
    return render(request,'store/list1.html',context)

def detail1(request,pid):
    goods=GoodsInfo.objects.get(id=int(pid))
    news=GoodsInfo.objects.filter(gtype=goods.gtype).order_by('-id')[0:2]
    if request.session['user_id'] != '':
        cart_count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        cart_count=0

    context={'title':goods.gtype,'cart_count':cart_count,'goods':goods,
             'news':news,'id':goods.id}

    response=render(request,'store/detail1.html',context)
    #最近浏览
    liulan=request.COOKIES.get("liulan","")
    if liulan == "":
        response.set_cookie("liulan",pid)

    else:
        liulan_list = liulan.split(',')
        if pid in liulan_list:
            liulan_list.remove(pid)
        liulan_list.insert(0,pid)
        if len(liulan_list)>5:
            liulan_list.pop()
        liulan2 = ','.join(liulan_list)
        response.set_cookie('liulan',liulan2)


    return response


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()

        extra['title']=self.request.GET.get('q')

        return extra


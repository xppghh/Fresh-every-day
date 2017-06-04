from django.conf.urls import url
import views1

urlpatterns=[
    url(r'^$', views1.index),
    url('^list(\d+)_(\d+)_(\d+)/$', views1.list1),
    url('^detail(\d+)/$',views1.detail1)
    
]

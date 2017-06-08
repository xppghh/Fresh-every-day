from django.conf.urls import url
import views

urlpatterns=[
    url(r'^cart/$',views.cart),
    url(r'^cart/add(\d+)_(-?\d+)',views.add),
    url(r'^cart/numadd(\d+)_(\d+)',views.numadd),
    url(r'^cart/delete(\d+)',views.delete),
]
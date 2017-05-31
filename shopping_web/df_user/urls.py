from django.conf.urls import url
import views

urlpatterns=[
    url(r'^register.html/$',views.register),
    url(r'^login.html/$',views.login),
    url(r'^login/$',views.register_handle),
    url(r'^login_handle/$',views.login_handle),
]
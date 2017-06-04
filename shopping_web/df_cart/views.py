from django.shortcuts import render
# from df_user import user_decorator
# Create your views here.
# @user_decorator
def cart(request):
    return render(request,'store/cart.html')

"""untitled3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from keshe import views

urlpatterns = [
    path('', views.index),
    path("all_books", views.all_books),
    path("book_type", views.book_type),
    path("borrow", views.borrow),
    path("page1",views.page1),
    path("page2",views.page2),
    path("page3",views.page3),
    path("page4",views.page4),
    path("page5",views.page5),
    path("sign_up",views.sign_up),
    path("login",views.login),
    path("classification",views.classification),
    path("get_class_value",views.get_class_value),
    path("search",views.search),
    path("get_user_inf",views.user_inf),
    path("book_return",views.return_book),
    path("get_borrow_value",views.borrowed_arr),
    path("page0",views.page0),
    path("logout",views.logout),


]

from django.contrib import admin
from django.urls import path, include
from order import views

urlpatterns = [
    path('', views.beforeLogin),
    path('order/', views.indexView, name='indexView'),
    path('detail/<orderId>', views.order_detail, name='detail'),
]

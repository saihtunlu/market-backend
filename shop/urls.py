"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('shops/', views.Shops.as_view()),
    path('shop/<str:slug>/', views.SingleShop.as_view()),
    path('shop/', views.SingleShop.as_view()),
    path('shop-users/', views.ShopUsers.as_view()),
    path('shop-user/<int:id>/', views.SingleShopUser.as_view()),
    path('shop-user/', views.SingleShopUser.as_view()),
]

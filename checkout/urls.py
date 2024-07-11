from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlPatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/<str:product_name>/', ProductView.as_view(), name='product-detail'),
    path('rules/', RuleView.as_view(), name='rules'),
    path('rules/<str:product_name>/', RuleView.as_view(), name='rule-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
from django.db import models
from kataCheckout import Product, Rules, Checkout

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30, null=True,blank=True)
    price = models.CharField(max_length=40,null=True, blank=True)
from django.db import models
from kataCheckout import Product as KataProduct, Rules as kataRules

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()

    def to_kataProduct(self):
        return KataProduct(self.name, self.price)

class Rule(models.Model):
    product = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    def to_kataRule(self):
        return kataRules(self.name, self.discount, self.quantity)
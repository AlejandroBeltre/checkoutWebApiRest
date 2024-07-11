from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

class Rule(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product_name} - {self.quantity} - {self.discount}"

class Checkout(models.Model):
    scanned_products = models.JSONField(default=list)  
    rules = models.JSONField(default=list)     

class ScannedProduct(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='scannedproduct_set', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
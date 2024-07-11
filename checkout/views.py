from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
from kataCheckout import *
# Create your views here.

class ProductView(APIView):
    def post(self, request):
        name = request.data.get("name")
        price = request.data.get("price")

        if not name or price is None:
            return Response({"error:" "Name and price are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = int(price)
            product, created = Product.objects.update_or_create(name=name, defaults={"price": price})
            message = "Product added" if created else "Product updated"
            return Response({"message": message, "name": product.name, "price": product.price}, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"error": "Price must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, product_name=None):
        if product_name:
            product = get_object_or_404(Product, name=product_name)
            return Response({"name": product.name, "price": product.price})

        products = Product.objects.all()
        return Response({p.name: {"name": p.name, "price": p.price} for p in products})
class RuleView(APIView):
    def post(self, request):
        product_name = request.data.get("product_name")
        quantity = request.data.get("quantity")
        discount = request.data.get("discount")
        if not product_name or quantity is None or discount is None:
            return Response({"error": "product_name, quantity and discount are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            quantity = int(quantity) if quantity else None
            discount = int(discount) if discount else None
            rule, created = Rule.objects.update_or_create(product=product, defaults={"quantity": quantity, "discount": discount})
            message = "Rule added" if created else "Rule updated"
            return Response({"message": message, "product_name": rule.product.name, "quantity": rule.quantity, "discount": rule.discount}, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"error": "Quantity and discount must be integers"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, product_name=None):
        if product_name:
            rule = get_object_or_404(Rule, product__name=product_name)
            return Response({"product_name": rule.product.name, "quantity": rule.quantity, "discount": rule.discount})

        rules = Rule.objects.all()
        return Response({r.product.name: {"product_name": r.product.name, "quantity": r.quantity, "discount": r.discount} for r in rules})

class CheckoutView(APIView):
    def post(self, request):
        product_names = request.data.get("product_name", [])
        if not product_names:
            return Response({"error": "Products are required"}, status=status.HTTP_400_BAD_REQUEST)
        rules = {r.product.name: r.to_kataRules() for r in Rule.objects.all()}
        checkout = Checkout(rules)

        for name in product_names:
            try:
                product = Product.objects.get(name=name)
                checkout.scan(product.to_kataProduct())
            except Product.DoesNotExist:
                return Response({"error": f"Product {name} not found"}, status=status.HTTP_404_NOT_FOUND)
        total = checkout.total()
        return Response({"total": total})
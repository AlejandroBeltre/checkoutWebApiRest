from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

    def validate(self, data):
        if data.get('quantity') and data.get('discount'):
            product_name = data['product_name']
            product = Product.objects.filter(product_name=product_name).first()
            if not product:
                raise serializers.ValidationError(f"Product with name '{product_name}' does not exist.")
            if int(data['quantity']) <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
            if int(data['discount']) <= 0:
                raise serializers.ValidationError("Discount must be greater than 0")
            if int(data['discount']) >= int(product.price) * int(data['quantity']):
                raise serializers.ValidationError("Discount cannot be greater than total price")
        return data

class ScannedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannedProduct
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    scanned_products = ScannedProductSerializer(many=True, read_only=True)
    rules = RuleSerializer(many=True, read_only=True)

    def create(self, validate_data):
        return Checkout.objects.create(**validate_data)

    class Meta:
        model = Checkout
        fields = '__all__'
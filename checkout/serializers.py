from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        fields = ['id','name','price']

class RuleSerializer(serializers.ModelSerializer):
    class Meta():
        model = Rule
        fields = ['id', 'product','quantity','discount']

    def validate(self, data):
        if data.get('quantity') and data.get('discount'):
            if data['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
            if data['discount'] <= 0:
                raise serializers.ValidationError("Discount must be greater than 0")
            if data['discount'] >= data['product'].price * data['quantity']:
                 raise serializers.ValidationError("Discount cannot be greater than total price")
        return data
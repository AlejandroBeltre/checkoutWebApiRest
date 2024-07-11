from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .models import Product, Rule, Checkout, ScannedProduct
from .serializers import ProductSerializer, RuleSerializer, CheckoutSerializer, ScannedProductSerializer
from kataCheckout import Checkout as kCheckout, Product as kProduct, Rules as kRules

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RuleView(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

class CheckoutView(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    @action(detail=True, methods=['post'])
    def manage_checkout(self, request, pk=None):
        checkout = self.get_object()
        action_type = request.data.get('action_type')

        if action_type == 'manage_checkout':
            # Handle scan_product
            scan_product_data = request.data.get('scan_product')
            if scan_product_data:
                product_name = scan_product_data.get('product_name')
                quantity = int(scan_product_data.get('quantity', 1))
                product = get_object_or_404(Product, product_name=product_name)

                scanned_product, created = ScannedProduct.objects.get_or_create(
                    checkout=checkout,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    scanned_product.quantity += quantity
                    scanned_product.save()

            # Handle add_rule
            add_rule_data = request.data.get('add_rule')
            if add_rule_data:
                rule_id = add_rule_data.get('rule_id')
                rule = get_object_or_404(Rule, id=rule_id)
                
                # Add rule to checkout
                checkout.rules.append({
                    'product_name': rule.product_name,
                    'quantity': rule.quantity,
                    'discount': rule.discount
                })
                checkout.save()

            # Handle total
            if request.data.get('total'):
                rules = {}
                for rule in Rule.objects.all():
                    product = get_object_or_404(Product, product_name=rule.product_name)
                    rules[product.product_name] = kRules(product, rule.quantity, rule.discount)
                
                k_checkout = kCheckout(rules)
                
                # Scan products
                for scanned_product in ScannedProduct.objects.filter(checkout=checkout):
                    product = kProduct(scanned_product.product.product_name, scanned_product.product.price)
                    for _ in range(scanned_product.quantity):
                        k_checkout.scan(product)
                
                total = k_checkout.total()
                return Response({"total": total}, status=status.HTTP_200_OK)

            return Response({"message": "Checkout managed successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action type"}, status=status.HTTP_400_BAD_REQUEST)
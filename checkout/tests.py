from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, Rule, Checkout, ScannedProduct
from .serializers import ProductSerializer, RuleSerializer, CheckoutSerializer, ScannedProductSerializer

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_name="manzana", price=100)

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, "manzana")
        self.assertEqual(self.product.price, 100)

class RuleModelTest(TestCase):
    def setUp(self):
        self.rule = Rule.objects.create(product_name="manzana", quantity=2, discount=50)

    def test_rule_creation(self):
        self.assertEqual(self.rule.product_name, "manzana")
        self.assertEqual(self.rule.quantity, 2)
        self.assertEqual(self.rule.discount, 50)

class CheckoutModelTest(TestCase):
    def setUp(self):
        self.checkout = Checkout.objects.create()

    def test_checkout_creation(self):
        self.assertEqual(self.checkout.scanned_products, [])
        self.assertEqual(self.checkout.rules, [])

class ScannedProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_name="manzana", price=100)
        self.checkout = Checkout.objects.create()
        self.scanned_product = ScannedProduct.objects.create(checkout=self.checkout, product=self.product, quantity=3)

    def test_scanned_product_creation(self):
        self.assertEqual(self.scanned_product.product, self.product)
        self.assertEqual(self.scanned_product.quantity, 3)

class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_name="manzana", price=100)
        self.serializer = ProductSerializer(instance=self.product)

    def test_product_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['product_name'], "manzana")
        self.assertEqual(data['price'], 100)

class RuleSerializerTest(TestCase):
    def setUp(self):
        self.rule = Rule.objects.create(product_name="manzana", quantity=2, discount=50)
        self.serializer = RuleSerializer(instance=self.rule)

    def test_rule_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['product_name'], "manzana")
        self.assertEqual(data['quantity'], 2)
        self.assertEqual(data['discount'], 50)

class CheckoutSerializerTest(TestCase):
    def setUp(self):
        self.checkout = Checkout.objects.create()
        self.serializer = CheckoutSerializer(instance=self.checkout)

    def test_checkout_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['scanned_products'], [])
        self.assertEqual(data['rules'], [])

class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {'product_name': 'manzana', 'price': 100}
        self.response = self.client.post(reverse('product-list'), self.product_data, format='json')

    def test_create_product(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RuleViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(product_name="manzana", price=100)
        self.rule_data = {'product_name': 'manzana', 'quantity': 2, 'discount': 50}
        self.response = self.client.post(reverse('rule-list'), self.rule_data, format='json')

    def test_create_rule(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_rules(self):
        response = self.client.get(reverse('rule-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CheckoutViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.checkout_data = {}
        self.response = self.client.post(reverse('checkout-list'), self.checkout_data, format='json')

    def test_create_checkout(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_checkouts(self):
        response = self.client.get(reverse('checkout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ManageCheckoutActionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(product_name="manzana", price=100)
        self.rule = Rule.objects.create(product_name="manzana", quantity=2, discount=50)
        self.checkout = Checkout.objects.create()
        self.url = reverse('manage_checkout', kwargs={'pk': self.checkout.pk})

    def test_manage_checkout(self):
        data = {
            'action_type': 'manage_checkout',
            'scan_product': {'product_name': 'manzana', 'quantity': 2},
            'add_rule': {'rule_id': self.rule.id},
            'total': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
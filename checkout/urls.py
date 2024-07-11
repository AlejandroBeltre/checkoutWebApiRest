from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView, RuleView, CheckoutView

router = DefaultRouter()
router.register(r'products', ProductView)
router.register(r'rules', RuleView)
router.register(r'checkouts', CheckoutView)

urlpatterns = [
    path('', include(router.urls)),
    path('checkouts/<int:pk>/manage_checkout/', CheckoutView.as_view({'post': 'manage_checkout'}), name='manage_checkout'),
]
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, LessonViewSet, BalanceViewSet, GroupViewSet

app_name = 'api'

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('lessons', LessonViewSet)
router.register('balances', BalanceViewSet)
router.register(
    r'products/(?P<product_id>\d+)/groups', GroupViewSet, basename='groups'
)

urlpatterns = [
    path('', include(router.urls)),
]

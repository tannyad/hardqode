from rest_framework import status, permissions
from api.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from course.models import Product, Lesson, Balance, Buy, Group
from .serializers import (ProductSerializer,
                          CreateProductSerializer,
                          LessonSerializer,
                          BalanceSerializer,
                          CreateLessonSerializer,
                          GroupSerializer,
                          CreateGroupSerializer)


class LessonViewSet(ModelViewSet):
    """Уроки"""

    permission_classes = (IsStudentOrIsAdmin,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        serializer.save(product=product)


class GroupViewSet(ModelViewSet):
    """Группы"""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs.get('product_id'))
        serializer.save(product=product)

    def get_queryset(self):
        return Group.objects.select_related('product').filter(
            product_id=self.kwargs.get('product_id'))


class BalanceViewSet(ReadOnlyModelViewSet):
    """Баланс пользователя"""

    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductViewSet(ModelViewSet):
    """Продукты"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        return CreateProductSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def buy(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        product = get_object_or_404(Product, id=pk)
        user = request.user
        user_subscription = Buy.objects.filter(
            product_id=pk, user_id=user.id).exists()
        user_balance = Balance.objects.get(user_id=user.id)
        product_cost = product.cost
        if not user_subscription:
            if user_balance.amount >= product_cost:
                new_user_balance = user_balance.amount - product_cost
                user_balance.amount = new_user_balance
                user_balance.save(update_fields=['amount'])
                Buy.objects.create(user=user, product=product)
                return Response(
                    data={201: 'Покупка совершена.'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data={400: 'Недостаточно средств.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
                data={400: 'Вы уже купили данный продукт.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available_courses(self, request):
        user_subs = Buy.objects.filter(user_id=request.user.id)
        products = Product.objects.exclude(id__in=[
            user_sub.product_id for user_sub in user_subs])
        serializer = self.get_serializer(products, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

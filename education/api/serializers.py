from rest_framework.fields import SerializerMethodField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from course.models import Product, Lesson, Balance, Buy, Group
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    """Список продуктов"""

    is_available = SerializerMethodField(read_only=True)
    creator = serializers.StringRelatedField(read_only=True)
    lessons = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('creator',
                  'name',
                  'date_start',
                  'cost',
                  'lessons',
                  'is_available',
                  )

    def get_is_available(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        is_available = Buy.objects.filter(user_id=user.id,
                                          product_id=obj.id).exists()
        if is_available:
            return False
        return True


class CreateProductSerializer(serializers.ModelSerializer):
    """Создание продукта"""

    class Meta:
        model = Product
        fields = ('creator',
                  'name',
                  'cost')


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков"""

    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = ('product',
                  'link',
                  'name')


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание урока"""
    class Meta:
        model = Lesson
        fields = ('product',
                  'link',
                  'name')


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор баланса пользователя"""

    class Meta:
        model = Balance
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Список групп"""

    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'product',
            'title',
            'count_student'
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание группы"""

    class Meta:
        model = Group
        fields = (
            'product',
            'title',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Balance.objects.create(user=user)

        return user


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )

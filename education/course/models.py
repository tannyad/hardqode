from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


min_amount_value = 0
default_amount = 1000


class Product(models.Model):
    """Модель продукта"""

    creator = models.ForeignKey(
        User,
        verbose_name='Создатель',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_products'
    )
    name = models.CharField(max_length=200,
                            verbose_name='Наименование продукта',)
    date_start = models.DateTimeField(
        verbose_name='Дата и время старта',
        auto_now_add=True,
        editable=False
    )
    cost = models.PositiveIntegerField(verbose_name='Стоимость продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""

    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        null=True,
        related_name='lessons'
    )
    name = models.CharField(max_length=200,
                            verbose_name='Наименование урока',)
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
        unique=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Balance(models.Model):
    """Баланс пользователя"""

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=True,
        related_name='user_balance'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=default_amount,
        validators=[MinValueValidator(
            min_amount_value,
            message='Баланс пользователя не может быть меньше нуля'
        )
        ])

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ['amount']

    def __str__(self):
        return f'Баланс {self.user.get_full_name()} = {self.amount}'


class Buy(models.Model):
    """Модель подписки/покупки пользователя на курс"""

    user = models.ForeignKey(
        User,
        related_name='buyer',
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='purchase',
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата покупки',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'Покупка {self.user} - {self.product}'


class Group(models.Model):
    """Модель группы"""

    title = models.CharField(
        max_length=250,
        verbose_name='Наименование группы'
    )
    count_student = models.IntegerField(
        verbose_name='Количество студентов',
        default=0
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='groups'
    )
    count_student = models.IntegerField(
        verbose_name='Количество студентов',
        default=0
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'Группа {self.title}'


class StudentGroup(models.Model):
    """Модель связи Студент-Группа"""

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )

    class Meta:
        verbose_name = 'Студент в группе'
        verbose_name_plural = 'Студенты в группе'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['group', 'user'],
                                    name='unique_student_group'),
        ]

    def __str__(self):
        return (f'Группа: {self.group.title} | Студент: {self.user.username} '
                f'| Курс: {self.group.product.title}')

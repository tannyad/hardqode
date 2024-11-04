from django.contrib import admin
from .models import (Product, Lesson, Balance, Buy)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Product._meta.fields]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Lesson._meta.fields]


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Balance._meta.fields]


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Buy._meta.fields]

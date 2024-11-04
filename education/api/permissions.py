from rest_framework.permissions import BasePermission, SAFE_METHODS
from course.models import Buy


def Buy(user, product_id: int) -> bool:
    if Buy.objects.filter(user=user, product__id=product_id).exists():
        return True
    return False


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.method in SAFE_METHODS and Buy(
            request.user, view.kwargs['product_id'])

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return request.method in SAFE_METHODS


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS

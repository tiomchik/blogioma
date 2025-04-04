from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from django.db.models import Model


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Model
    ) -> bool:
        if (request.method in permissions.SAFE_METHODS or
            request.user.is_staff):
            return True

        return obj.author == request.user

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View

from articles.models import Article


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, obj: Article
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.author == request.user) or request.user.is_staff

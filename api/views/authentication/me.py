from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import User
from api.serializers import UserSerializer


class Me(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    @method_decorator(cache_page(60))
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    def get_object(self) -> User:
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user

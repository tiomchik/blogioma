from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserSerializer, EditUserSerializer
from authentication.models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer: UserSerializer) -> User:
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        email = serializer.validated_data.get("email")
        pfp = serializer.validated_data.get("pfp")

        user = User.objects.create(
            username=username, password=password, email=email, pfp=pfp
        )

        return user

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserSerializer(new_user).data, status=status.HTTP_201_CREATED,
            headers=headers
        )


class Me(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    @method_decorator(cache_page(60))
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        user = self.get_object()
        return Response(
            UserSerializer(user).data, status=status.HTTP_200_OK
        )

    def get_object(self) -> User:
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user


class Edit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self) -> User:
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user

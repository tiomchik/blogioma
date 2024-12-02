from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from api.serializers import (
    UserSerializer, EditUserSerializer, ProfileSerializer
)
from authentication.models import Profile


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer: UserSerializer) -> User:
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        email = serializer.validated_data.get("email")
        pfp = serializer.validated_data.get("pfp")

        user = User.objects.create(username=username, password=password, email=email)
        Profile.objects.create(user=user, pfp=pfp)

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
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    @method_decorator(cache_page(60))
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        profile = self.get_object()

        return Response(
            ProfileSerializer(profile).data, status=status.HTTP_200_OK
        )

    def get_object(self) -> Profile:
        obj = Profile.objects.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)

        return obj


class Edit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self) -> User:
        obj = User.objects.get(username=self.request.user.username)
        self.check_object_permissions(self.request, obj)

        return obj

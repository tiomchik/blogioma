from rest_framework.generics import CreateAPIView

from authentication.models import User
from api.serializers.user import UserSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.generics import RetrieveAPIView

from api.serializers.user import UserSerializer
from authentication.models import User


class RetrieveUser(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

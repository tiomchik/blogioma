from rest_framework.generics import RetrieveAPIView

from api.serializers.user import UserSerializer
from authentication.models import User


class RetrieveUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from api.serializers.user import EditUserSerializer
from authentication.models import User


class Edit(RetrieveUpdateDestroyAPIView):
    serializer_class = EditUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self) -> User:
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user

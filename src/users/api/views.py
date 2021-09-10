from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from users.api.serializers import UserCreateSerializer, UserSerializer
from users.models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.for_viewset()

    def get_serializer_class(self):
        if hasattr(self, "action") and self.action == "create":
            return UserCreateSerializer
        return UserSerializer

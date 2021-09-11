from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from bookstore.api.serializers import AddUserPaymentSerializer, BookSerializer
from bookstore.definitions import PERIODS_MAP
from bookstore.models import Book, Subscription
from users.models import User


class SubscriptionOrListOnlyPermission(permissions.IsAuthenticated):
    """
    User can view book details only with active subscription.
    """

    def has_permission(self, request, view):
        if view.action == "retrieve":
            return Subscription.objects.filter(user=request.user).active().exists()

        return True


class BookViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, SubscriptionOrListOnlyPermission]
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AddUserPaymentView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = AddUserPaymentSerializer(data=request.data)
        if (
            serializer.is_valid(raise_exception=True)
            and serializer.validated_data["status"] == "ok"
        ):
            user = get_object_or_404(User, pk=serializer.validated_data["user_id"])
            update_period = PERIODS_MAP.get(serializer.validated_data["period"])
            user.subscription.update_due_date_after_payment(update_period)

        return Response("ok")

from rest_framework import serializers

from bookstore.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "name"]


class AddUserPaymentSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    status = serializers.ChoiceField(choices=("ok", "error"))
    period = serializers.ChoiceField(choices=("year", "month"), required=False)
    msg = serializers.CharField(required=False)

    def validate_user_id(self, value):
        if not value or not str(value).isdigit():
            raise serializers.ValidationError("user_id must be integer")
        return value

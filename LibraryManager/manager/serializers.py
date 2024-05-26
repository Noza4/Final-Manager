from rest_framework import serializers
from manager.models import Book, BookReservation, CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ReservationRemoval(serializers.Serializer):
    reservation_id = serializers.IntegerField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReservation
        fields = '__all__'

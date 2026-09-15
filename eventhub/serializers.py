from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Booking, UserProfile


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(
        source='organizer.username',
        read_only=True
    )

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer']


class BookingSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'customer_name', 'customer_email', 'total_amount']
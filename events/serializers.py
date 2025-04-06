from rest_framework import serializers
from .models import Event, EventRegistration
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        """
        Meta class for the UserSerializer.
        """
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.
    """
    organizer = UserSerializer(read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    is_registration_open = serializers.BooleanField(read_only=True)

    class Meta:
        """
        Meta class for the EventSerializer.
        """
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location',
            'organizer', 'capacity', 'price', 'created_at',
            'updated_at', 'is_active', 'available_seats',
            'is_registration_open'
        ]

class EventCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Event.
    """
    class Meta:
        """
        Meta class for the EventCreateSerializer.
        """
        model = Event
        fields = [
            'title', 'description', 'date', 'location',
            'capacity', 'price', 'is_active'
        ]

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value

class EventRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the EventRegistration model.
    """
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        """
        Meta class for the EventRegistrationSerializer.
        """
        model = EventRegistration
        fields = [
            'id', 'event', 'user', 'registration_date',
            'status', 'payment_status'
        ]
        read_only_fields = ['user', 'registration_date']

class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an EventRegistration.
    """
    class Meta:
        """
        Meta class for the EventRegistrationCreateSerializer.
        """
        model = EventRegistration
        fields = ['event']

    def validate(self, data: dict) -> dict:
        """
        Validate the data for the EventRegistrationCreateSerializer.
        """
        event = data['event']
        user = self.context['request'].user

        if not event.is_registration_open():
            raise serializers.ValidationError("Event registration is closed")

        if event.available_seats <= 0:
            raise serializers.ValidationError("No available seats")

        if EventRegistration.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("You are already registered for this event")

        return data 
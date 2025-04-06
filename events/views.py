from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Event, EventRegistration
from .serializers import (
    EventSerializer, EventCreateSerializer,
    EventRegistrationSerializer, EventRegistrationCreateSerializer
)
from .permissions import IsEventOrganizer
from .filters import EventFilter
from notifications.tasks import send_event_registration_email
from typing import QuerySet

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing events.
    """
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_serializer_class(self) -> EventCreateSerializer | EventSerializer:
        """
        Get the serializer class for the event view set.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return EventCreateSerializer
        return EventSerializer

    def get_permissions(self) -> list[permissions.BasePermission]   :
        """
        Get the permissions for the event view set.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEventOrganizer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: EventCreateSerializer) -> None:
        """
        Perform the create action for the event view set.
        """
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def register(self, request: Request, pk: int = None) -> Response:
        """
        Register for an event.
        """
        event = self.get_object()
        serializer = EventRegistrationCreateSerializer(
            data={'event': event.id},
            context={'request': request}
        )
        
        if serializer.is_valid():
            registration = serializer.save(user=request.user)
            
            send_event_registration_email.delay(
                user_id=request.user.id,
                event_id=event.id,
                registration_id=registration.id
            )
            
            return Response(
                EventRegistrationSerializer(registration).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def registrations(self, request: Request, pk: int = None) -> Response:
        """
        Get the registrations for an event.
        """
        event = self.get_object()
        registrations = event.registrations.all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class EventRegistrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing event registrations.
    """
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[EventRegistration]:
        """
        Get the queryset for the event registration view set.
        """
        return EventRegistration.objects.filter(user=self.request.user)

    def get_permissions(self) -> list[permissions.BasePermission]:
        """
        Get the permissions for the event registration view set.
        """
        if self.action in ['destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def cancel(self, request: Request, pk: int = None) -> Response:
        """
        Cancel a registration.
        """
        registration = self.get_object()
        
        if registration.status == 'cancelled':
            return Response(
                {'error': 'Registration is already cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if registration.event.date < timezone.now():
            return Response(
                {'error': 'Cannot cancel registration for past events'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration.status = 'cancelled'
        registration.save()
        
        return Response(
            EventRegistrationSerializer(registration).data,
            status=status.HTTP_200_OK
        ) 
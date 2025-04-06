from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from typing import Any
from events.models import Event

class IsEventOrganizer(permissions.BasePermission):
    """
    Custom permission to only allow event organizers to edit their events.
    """
    def has_object_permission(self, request: Request, view: APIView, obj: Event) -> bool:
        """
        Check if the user is the organizer of the event.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.organizer == request.user 
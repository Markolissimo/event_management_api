from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from typing import Any


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user 
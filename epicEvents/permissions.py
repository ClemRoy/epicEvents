from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from authentication.models import User
from epicEvents.models import Client, Contract, Event


class EventPermission(permissions.BasePermission):
    """
    Permission class that determines whether a user has the necessary permissions to perform a given action on an Event object.
    """

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        """
        Returns a boolean indicating whether the user has permission to perform the given action on the Event object.
        
        Parameters:
        - request: The HTTP request object.
        - view: The view that is being accessed.
        
        Returns:
        - A boolean indicating whether the user has permission to perform the given action.
        """
        user = request.user
        
        if user.is_superuser:
            return True
        if user.is_commercial() or user.is_support():
            if view.action in ['list', 'retrieve']:
                return True
            if view.action == 'destroy':
                if user.is_superuser:
                    return True
                else:
                    return False
            if view.action == 'create':
                if user.is_commercial():
                    return True
                else:
                    return False
            if view.action in ['update','partial_update']:
                if user.is_support():
                    return True
                else:
                    return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Returns a boolean indicating whether the user has permission to perform the given action on the given Event object.
        
        Parameters:
        - request: The HTTP request object.
        - view: The view that is being accessed.
        - obj: The Event object being accessed.
        
        Returns:
        - A boolean indicating whether the user has permission to perform the given action on the given Event object.
        """
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Event):
            if obj.support_contact == user and user.is_support():
                return True
            else:
                return False


class ClientAndContractPermission(permissions.BasePermission):
    """
    Permission class for Client and Contract models.
    Users can only perform actions based on their role:
    - Superuser: all actions
    - Commercial: view and create clients and contracts, view and edit their own clients and contracts
    - Support: view events and contracts, edit events and contracts they support
    """

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        """
        Check if user has permission to perform the given action.
        """
        user = request.user

        if user.is_superuser:
            return True
        if user.is_commercial() or user.is_support():
            if view.action in ['list', 'retrieve']:
                return True

            if view.action == 'destroy':
                if user.is_superuser:
                    return True
                else:
                    return False

            if user.is_commercial():
                return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to perform the given action on the object.
        """
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Client):
            if obj.sales_contact == user and user.is_commercial():
                return True
            else:
                return False
        elif isinstance(obj,Contract):
            if obj.sales_contact == user:
                return True
            else:
                return False

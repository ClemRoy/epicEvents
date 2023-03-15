from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from authentication.models import User
from epicEvents.models import Client, Contract, Event


class EventPermission(permissions.BasePermission):

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        if view.action in ['list', 'retrieve']:
            return True

        if view.action is 'destroy':
            if user.is_superuser:
                return True
            else:
                return False

        if view.action is 'create':
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
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Event):
            if obj.support_contact == user and user.is_support():
                return True
            else:
                return False


class ClientAndContractPermission(permissions.BasePermission):

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        if view.action in ['list', 'retrieve']:
            return True

        if view.action is 'destroy':
            if user.is_superuser:
                return True
            else:
                return False

        if user.is_commercial():
            return True

        else:
            return False

    def has_object_permission(self, request, view, obj):
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

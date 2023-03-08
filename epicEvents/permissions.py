from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from authentication.models import User
from epicEvents.models import Client, Contract, Event


class EventPermission(permissions.BasePermission):

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        user = request.user

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


class ClientAndContractPermission(permissions.BasePermission):

    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        user = request.user

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

""" has object perm pour verifier propr. """

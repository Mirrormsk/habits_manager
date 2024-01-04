from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Checks if the user is an owner of the habit or superuser"""
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user == obj.owner or request.user.is_superuser)

from rest_framework.permissions import BasePermission

from .models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.ADMIN


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Role.MEMBER

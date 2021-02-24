from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allows patient to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Validates that patient is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class UpdateOwnReading(permissions.BasePermission):
    """Allows patient to edit their own readings"""

    def has_object_permission(self, request, view, obj):
        """Validates that patient is trying to edit their own reading"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id
from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
    """
    Global permission to allow read-only access to all requests.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow admin users to edit objects but allow read-only
    access to all users.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

    
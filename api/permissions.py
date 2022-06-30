from rest_framework import permissions


class UserHasAgencePermission(permissions.BasePermission):

    # edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, "agence"):
            return True

        return False

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True

    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     if obj.author == request.user:
    #         return True

    #     if request.user.is_staff and request.method not in self.edit_methods:
    #         return True

    #     return False

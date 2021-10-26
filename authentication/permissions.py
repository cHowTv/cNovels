from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Author can only have access to modify his novel
    """
    message = "Only author has access to this resource"

    def has_permission(self, request, view):
        if request.user.is_authenticated :
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False



class GroupOwners(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    
    def has_object_permission(self, request, view, obj):
        if request.user in obj.admins:
            return True
        return False
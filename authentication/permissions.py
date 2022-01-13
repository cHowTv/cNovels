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

    def has_permission(self, request, view):
        #if creator is author
        if request.user.is_author:
            return True
        return False
    # Check if user has access to the particular resource
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False



class GroupOwners(permissions.BasePermission):
    """
    Managing the group
    """
    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return True 
        return False

    
    def has_object_permission(self, request, view, obj):
        if request.user in obj.admins.all():
            return True
        return False

class GroupMember(permissions.BasePermission):
    """
    Managing the group
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        #list group member if user in group
        if request.user.groupchat_set.filter(room=obj):
            return True
        return False

class GroupCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            return True 
        return False

    
    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        return False

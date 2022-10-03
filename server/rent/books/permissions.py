from rest_framework import permissions


class IsAuthorOrCantDeleteAndUpdate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('delete', 'put', 'patch'):
            return request.user.is_staff() or request.user == obj.author
        return True

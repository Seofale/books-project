from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class IsHaveSubscriptionOrCantReadBook(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return obj.subscription_type <= request.user.subscription.type

        except ObjectDoesNotExist:
            return False

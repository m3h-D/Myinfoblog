from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """baraye updateAPIView ke request.user hamoon author bashe"""
    message = "شما باید صاحب این پست باشید"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return obj.author == request.user
        except:
            return obj.user == request.user

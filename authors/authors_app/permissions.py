from rest_framework.permissions import BasePermission
from oauth2_provider.models import AccessToken


class BearerPermission(BasePermission):
    def has_permission(self, request, view):
        token_str = request.META.get('HTTP_AUTHORIZATION', '')
        try:
            token = token_str[6:].strip()
        except TypeError:
            return False
        return AccessToken.objects.filter(token=token).exists()
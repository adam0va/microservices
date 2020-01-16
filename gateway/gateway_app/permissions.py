from rest_framework.permissions import BasePermission
from .requesters.auth_requester import AuthRequester


class IsAuthenticatedThroughAuthService(BasePermission):
    def has_permission(self, request, view):
        _, code = AuthRequester().get_user_info(request=request)
        print(f'code: {code}')
        return code == 200
from typing import Tuple
from .requester import Requester


class AuthRequester(Requester):
    AUTH_HOST = Requester.HOST + ':8004/api/'

    def _create_auth_header(self, token: str):
        token_type = 'Bearer' if len(token) < 40 else 'Token'
        return {'Authorization': f'{token_type} {token}'}


    def get_user_info(self, request):
        token = self.get_token_from_request(request)
        if token is None:
            return {}, 403
        response = self.get_request(self.AUTH_HOST + 'user_info/', headers=self._create_auth_header(token))
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

    def authenticate(self, data: dict):
        response = self.post_request(url=self.AUTH_HOST + 'token-auth/', data=data)
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code
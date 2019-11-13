from gateway_app.requesters.requester import Requester

class AuthorRequester(Requester):
    AUTHOR_HOST = Requester.HOST + ':8002/authors/'

    def get_all_authors(self, request):
        response = self.get_request(self.AUTHOR_HOST)
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

    def get_author(self, request, uuid):
        response = self.get_request(self.AUTHOR_HOST + f'{uuid}/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

    def post_author(self, request, data):
        response = self.post_request(self.AUTHOR_HOST, data=data)
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

    def patch_author(self, request, uuid, data):
        response = self.patch_request(self.AUTHOR_HOST + f'{uuid}/', data=data)
        #if response is None:
            #return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

    def delete_author(self, request, uuid):
        response = self.delete_request(self.AUTHOR_HOST + f'{uuid}/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code

class AuthorQueue:
    def __init__(self):
        self.queue = []
        self.is_on = True

    def add_patch(self, uuid, data):
        self.queue.append({'type' : 'patch', 'uuid' : uuid, 'data' : data})
        self.is_on = False
        print('add patch')

    def add_post(self, data):
        self.queue.append({'type': 'post', 'data': data})
        self.is_on = False
        print('add post')

    def add_delete(self, uuid):
        self.queue.append({'type': 'delete', 'uuid' : uuid})
        self.is_on = False
        print('add delete')

    def send_requests(self):
        from .author_requester import AuthorRequester
        if self.is_on:
            return
        self.is_on = True
        print('Sending')
        requester = AuthorRequester()
        for request in self.queue:
            if request['type'] == 'patch':
                requester.patch_author(uuid=request['uuid'], data=request['data'], request=None)
            if request['type'] == 'post':
                requester.post_author(data=request['data'], request=None)
            if request['type'] == 'delete':
                requester.delete_author(uuid=request['uuid'], request=None)
        self.queue = []

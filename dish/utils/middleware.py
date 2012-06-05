from django.http import HttpResponse

class LazyAccount(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_account'):
            from dish.utils.auth import get_youease_account
            request._cached_account = get_youease_account(request)
        return request._cached_account

class YoueaseAccountMiddleware(object):

    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.__class__.account = LazyAccount()
        return None

    #def process_response(self, request):

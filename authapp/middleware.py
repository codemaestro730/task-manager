from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

def get_user(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return AnonymousUser()
    try:
        user = TokenAuthentication().authenticate(request)
        if user is not None:
            return user[0]
    except AuthenticationFailed:
        pass
    return AnonymousUser()

class GraphQLAuthMiddleware:
    def resolve(self, next, root, info, **args):
        request = info.context
        request.user = SimpleLazyObject(lambda: get_user(request))

        if not request.user.is_authenticated:
            if "IntrospectionQuery" not in info.operation.name.value:  # Allow introspection queries
                raise Exception("Authentication credentials were invalid.")
        return next(root, info, **args)
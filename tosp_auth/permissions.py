from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import BasePermission
from .authentication import SecretTokenAuthentication as Secret


class IsAuthenticatedWithSecret(BasePermission):
    """
    Allows acces only to users that Authenticated
    with their Secret Token; based on the IsAuthenticated
    permission from the Django Rest Framework.
    """

    def auth_method_is_secret_token(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != Secret.keyword.lower().encode():
            return False
        return True

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            self.auth_method_is_secret_token(request)

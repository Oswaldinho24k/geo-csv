from rest_framework import parsers, renderers, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from user_profiles.utils import is_client
from .models import SecretToken


class ResetAuthToken(ObtainAuthToken, GenericAPIView):
    """ View to Obtain an authentication Token
        View for a user to provide credentials and obtain an authentication Token.
        This view is a refactor of:
        https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/views.py#L21
        This view incorporates validation that only certain group users can obtain
        authentication through the API.
        The view creates or retrieves a Token for a user and returns it in JSON format.
    """
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if is_client(user):
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token, created = Token.objects.get_or_create(user=user)

            secret_token, created = SecretToken.objects.get_or_create(user=user)
            if not created:
                secret_token.delete()
                secret_token, created = SecretToken.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'secret_token': secret_token.key})

        return Response(status=status.HTTP_400_BAD_REQUEST)

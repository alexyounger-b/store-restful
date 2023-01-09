from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response

from apps.authentication.models import User
from apps.authentication.serializers import (
    LoginSerializer,
    SignUpSerializer,
    UserSerializer,
)


class AuthenticationViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["POST"], detail=False, url_path="signup", serializer_class=SignUpSerializer)
    def signup(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data=UserSerializer(instance=user).data)

    @action(methods=["POST"], detail=False, url_path="login", serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key})

    @action(
        methods=["POST"],
        detail=False,
        url_path="logout",
        serializer_class=LoginSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ("patch", "put", "get")
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

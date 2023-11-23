from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from CDR.filters import CRDFilter
from CDR.models import CDR, User
from CDR.serializer import CDRSerializer, VerifySerializer, RegisterSerializer, LoginSerializer
from CDR.service import UserAuthService
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class CDRView(viewsets.ModelViewSet):
    queryset = CDR.objects.all()
    serializer_class = CDRSerializer
    filterset_class = CRDFilter
    permission_classes = (IsAuthenticated,)


class RegisterView(GenericAPIView):
    queryset = User
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()
        UserAuthService.get_response(user, user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyView(GenericAPIView):
    queryset = User
    serializer_class = VerifySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    queryset = User
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
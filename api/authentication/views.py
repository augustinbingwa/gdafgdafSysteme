# from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


from .serializers import UsernameLoginSerializer, UserSerializer


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UsernameLoginSerializer
    # renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        # user = request.data.get("user", {})
        print(request)


        # # Notice here that we do not call 'serializer.save()' like we did for
        # # the registration endpoint. This is because we don't  have
        # # anything to save. Instead, the 'validate' method on our serializer
        # # handles everything we need.
        # serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)
        #
        # return Response({"user": serializer.data}, status=status.HTTP_200_OK)

        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},status=HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our 'User' object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     user_data = request.data.get("user", {})
    #     serializer_data = {
    #         "username": user_data.get("username", request.user.username),
    #         "email": user_data.get("email", request.user.email),
    #         "profile": {
    #             "bio": user_data.get("bio", request.user.profile.bio),
    #             "image": user_data.get("image", request.user.profile.image),
    #             "regis": "Kigabo",
    #         },
    #     }
    #     # Here is that serialize, validate, save pattern we talked about
    #     # before.
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_200_OK)

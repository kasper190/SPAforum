from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer,
    UserPasswordResetSerializer,
)
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from forum.models import ForumSettings


User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserPasswordChangeAPIView(UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            self.object.set_password(data['password1'])
            self.object.save()
            return Response({'username': self.object.username}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserPasswordResetAPIView(APIView):
    serializer_class = UserPasswordResetSerializer
    permission_classes = (AllowAny,)
    
    def reset_password(self, email):
        user_obj = User.objects.get(email=email)
        password = User.objects.make_random_password()
        user_obj.set_password(password)
        user_obj.save()
        return password

    def send_password_reset_email(self, email, password):
        user = User.objects.get(email=email)
        forum_name = ForumSettings.objects.last()
        subject = "Your %s account new password" % forum_name
        message = "<p>Hi <b>%s</b>!</p>\
                   <p>You have reset your password.\
                   Here is your new password: <b>%s</b>\
                   <br>Now you can log in and change it.</p>\
                   <p>Thanks,\
                   <br>%s administration</p>" % (
                    user.username, password, forum_name
                   )
        from_email = settings.DEFAULT_FROM_EMAIL
        new_email = send_mail(
            subject,
            message,
            from_email,
            [user.email],
            html_message=message,
            fail_silently=False
        )
        return new_email

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserPasswordResetSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email = data['email']
            password = self.reset_password(email)
            send_email = self.send_password_reset_email(email, password)
            if send_email:
                new_data = serializer.data
                return Response(new_data, status=HTTP_200_OK)
            return Response("Reset password operation has failed. Please try again.", status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AllowAny,)
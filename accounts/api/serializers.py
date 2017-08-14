from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    password = CharField(label='Password', write_only=True)
    password2 = CharField(label='Confirm Passeord', write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'password2',
            'token',
        )

    def validate(self, data):
        # username = data['username']
        # user_qs_email = User.objects.filter(username=username)
        # if user_qs_email.exists():
        #   raise ValidationError("User with this username has already registered.")
        # email = data['email']
        # user_qs_email = User.objects.filter(email=email)
        # if user_qs_email.exists():
        #   raise ValidationError("User with this e-mail has already registered.")
        return data
    
    def validate_password(self, value):
        data = self.get_initial()
        password1 = data.get('password2')
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get('password')
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        validated_data['id'] = user_obj.id
        validated_data['token'] = token
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    #email = EmailField(label='Email Address')
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            #'email',
            'password',
            'token',        
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        username = data['username']
        password = data['password']
        user_obj = User.objects.get(username=username)
        if user_obj.is_banned:
            raise ValidationError('You are banned.')
        if not user_obj.check_password(password):
            raise ValidationError('Incorrect credentials please try again.') 
        if user_obj.check_password(password):
            data['id'] = user_obj.id
            data['username'] = user_obj.username
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            data['token'] = token
            return data
        raise ValidationError('Invalid credentials.')


class UserPasswordChangeSerializer(ModelSerializer):
    password1 = CharField(label='New Password', write_only=True)
    password2 = CharField(label='Confirm New Password', write_only=True)

    class Meta:
        model = User
        fields = (
            'password',
            'password1',
            'password2',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_password(self, value):
        data = self.get_initial()
        user = self.context['request'].user
        password = data.get('password')
        user_obj = User.objects.get(username=user)
        if not user_obj.check_password(password):
            raise ValidationError("You passed invalid password.")
        return value

    def validate_password1(self, value):
        data = self.get_initial()
        password1 = data.get('password2')
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value
    
    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get('password1')
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value


class UserPasswordResetSerializer(Serializer):
    email = EmailField()

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        return value


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            #'email',
            'date_joined',
            'last_login',
            'is_banned',
        )
        read_only_fields = fields
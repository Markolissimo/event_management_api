from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        """
        Meta class for the UserSerializer.
        """
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'phone_number', 'bio', 'profile_picture', 'is_verified',
                 'created_at', 'updated_at']
        read_only_fields = ['is_verified', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Meta class for the UserRegistrationSerializer.
        """
        model = User
        fields = ['email', 'username', 'password', 'password2', 
                 'first_name', 'last_name', 'phone_number']

    def validate(self, attrs: dict) -> dict:
        """
        Validate the data for the UserRegistrationSerializer.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data: dict):
        """
        Create a new user.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> dict:
        """
        Get a token for the user.
        """
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token 
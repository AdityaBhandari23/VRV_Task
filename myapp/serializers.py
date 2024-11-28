from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, UserRole, Article

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','username','email','date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['director', 'hod', 'student'], write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Assign role
        role, _ = Role.objects.get_or_create(name=role_name)
        UserRole.objects.create(user=user, role=role)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ('id','title','content','author','created_at','updated_at')
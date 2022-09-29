from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class UserRetrieveSerializer(serializers.ModelSerializer):
    is_me_following = serializers.SerializerMethodField(method_name='get_is_me_following')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_me_following')

    def get_is_me_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.followers.filter(user=user).exists()

        return False

from datetime import date

from rest_framework import serializers

from .models import Book, Tag, Genre, Subscription


class BookCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Book
        fields = ('title', 'description', 'tags', 'genres')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['upload'] = self.context['request'].FILES.get('file')

        return super().create(validated_data)


class BookRetrieveSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    is_me_liked = serializers.SerializerMethodField(method_name='get_is_me_liked')

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'tags', 'genres', 'is_me_liked')

    def get_is_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()

        return False


class BookRetrieveForSubUserSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    is_me_liked = serializers.SerializerMethodField(method_name='get_is_me_liked')

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'tags', 'genres', 'upload', 'is_me_liked')

    def get_is_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()

        return False


class BookListSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    is_me_liked = serializers.SerializerMethodField(method_name='get_is_me_liked')

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'tags', 'genres', 'is_me_liked')

    def get_is_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()

        return False


class TagRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'title')


class GenreRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'title')


class SubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('type', 'duration')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['start_date'] = date.today()

        return super().create(validated_data)


class SubscriptionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('type', 'duration', 'start_date')

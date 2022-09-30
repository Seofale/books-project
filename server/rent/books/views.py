from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from .serializers import (BookCreateSerializer, BookRetrieveSerializer,
                          TagRetrieveSerializer, GenreRetrieveSerializer,
                          SubscriptionCreateSerializer, SubscriptionRetrieveSerializer,
                          BookRetrieveForSubUserSerializer)
from .models import Book, Tag, Genre, Like
from . import constants


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'retrieve':
            try:
                if self.get_object().subscription_type <= self.request.user.subscription.type:
                    return BookRetrieveForSubUserSerializer
                return BookRetrieveSerializer

            except ObjectDoesNotExist:  # user don't have any subscription
                return BookRetrieveSerializer
        elif self.action in ('list', 'likes'):
            return BookRetrieveSerializer
        elif self.action == 'subscribe':
            return SubscriptionCreateSerializer
        elif self.action == 'subscription':
            return SubscriptionRetrieveSerializer

    def get_queryset(self):
        if self.action == 'likes':
            return Book.objects.filter(likes__user=self.request.user)

        return Book.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

    def get_object(self):
        if self.action == 'subscription':
            try:
                return self.request.user.subscription

            except ObjectDoesNotExist:
                return {'type': None, 'duration': None, 'start_date': None, 'days_to_end': None}

        return super().get_object()

    @action(
        methods=('post',),
        detail=False,
        url_path='subscribe',
    )
    def subscribe(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(
        methods=('get',),
        detail=False,
        url_path='subscription',
    )
    def subscription(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='like',
    )
    def like(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)

        like_exists = Like.objects.filter(user=request.user, book=book).exists()

        if request.method == 'POST':
            if not like_exists:
                Like.objects.create(user=request.user, book=book)
                return Response(status=status.HTTP_201_CREATED)

            return Response({'message': constants.ALREADY_LIKED})

        if like_exists:
            Like.objects.filter(user=request.user, book=book).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'message': constants.NOT_LIKED})

    @action(
        methods=('get',),
        detail=False,
        url_path='likes',
    )
    def likes(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TagListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagRetrieveSerializer
    queryset = Tag.objects.all()


class GenreListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreRetrieveSerializer
    queryset = Genre.objects.all()

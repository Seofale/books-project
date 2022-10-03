from typing import Type, Union

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, serializers, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models.query import QuerySet

from .serializers import (BookCreateSerializer, BookRetrieveSerializer,
                          TagRetrieveSerializer, GenreRetrieveSerializer,
                          SubscriptionCreateSerializer, SubscriptionRetrieveSerializer,
                          BookRetrieveForSubUserSerializer)
from .models import Book, Tag, Genre, Like, Subscription
from . import constants
from .permissions import IsAuthorOrCantDeleteAndUpdate


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAuthorOrCantDeleteAndUpdate)

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'retrieve':
            try:
                if self.get_object().subscription_type <= self.request.user.subscription.type:
                    return BookRetrieveForSubUserSerializer
                return BookRetrieveSerializer

            except ObjectDoesNotExist:  # user don't have any subscription
                return BookRetrieveSerializer
        elif self.action in ('list', 'likes', 'top_by_likes'):
            return BookRetrieveSerializer
        elif self.action == 'subscribe':
            return SubscriptionCreateSerializer
        elif self.action == 'subscription':
            return SubscriptionRetrieveSerializer

    def get_queryset(self) -> QuerySet:
        if self.action == 'likes':
            return Book.objects.filter(likes__user=self.request.user)
        elif self.action == 'top_by_likes':
            return Book.objects.annotate(
                likes_count=Sum('likes')
            ).order_by('-likes_count')[:10]
        elif self.action == 'top_by_author_subscriptions':
            return Book.objects.annotate(
                likes_count=Sum('likes')
            ).order_by('-likes_count')[:10]

        return Book.objects.all()

    def get_permissions(self) -> permissions.BasePermission:
        if self.action == 'list':
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

    def get_object(self) -> Union[Book, Subscription]:
        if self.action == 'subscription':
            try:
                return self.request.user.subscription

            except ObjectDoesNotExist:
                return constants.NO_SUBSCRIPTION

        return super().get_object()

    @action(
        methods=('post',),
        detail=False,
        url_path='subscribe',
    )
    def subscribe(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @action(
        methods=('get',),
        detail=False,
        url_path='subscription',
    )
    def subscription(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='like',
    )
    def like(self, request: Request, pk: int = None) -> Response:
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
    def likes(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=('get',),
        detail=False,
        url_path='top-10-by-likes',
    )
    def top_by_likes(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class TagListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagRetrieveSerializer
    queryset = Tag.objects.all()


class GenreListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreRetrieveSerializer
    queryset = Genre.objects.all()

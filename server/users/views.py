from typing import Type, Optional

from django.db.models import QuerySet
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserRetrieveSerializer
from .models import User, Follow
from . import constants


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'head', 'delete')

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == 'create':
            return UserCreateSerializer

        return UserRetrieveSerializer

    def get_queryset(self, user=None) -> QuerySet:
        if self.action == 'follows':
            return User.objects.filter(followers__user=user)

        elif self.action == 'followers':
            return User.objects.filter(follows__author=user)

        return User.objects.all()

    def get_permissions(self):
        if self.action in ('retrieve', 'list', 'create'):
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

    def get_object(self) -> User:
        if self.action == 'me':
            return self.request.user

        return super().get_object()

    @action(
        detail=False,
        methods=('get',),
        url_path='me',
    )
    def me(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=('get',),
        url_path='follows',
    )
    def follows(self, request: Request, pk: Optional[int] = None) -> Response:
        return self.get_follows_and_followers(pk)

    @action(
        detail=True,
        methods=('get',),
        url_path='followers',
    )
    def followers(self, request: Request, pk: Optional[int] = None) -> Response:
        return self.get_follows_and_followers(pk)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='follow',
    )
    def follow(self, request: Request, pk: Optional[int] = None) -> Response:
        user = request.user
        author = get_object_or_404(User, pk=pk)

        follow_exists = Follow.objects.filter(user=user, author=author).exists()

        if request.method == 'POST':
            if not follow_exists:
                Follow.objects.create(user=user, author=author)
                return Response(status=status.HTTP_201_CREATED)

            return Response({'message': constants.ALREADY_SUBSCRIBE})

        if follow_exists:
            Follow.objects.filter(user=request.user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'message': constants.NOT_SUBSCRIBE})

    def get_follows_and_followers(self, pk: int):
        user = get_object_or_404(User, pk=pk)

        if not user.is_private or user == self.request.user:
            queryset = self.get_queryset(user)
            page = self.paginate_queryset(queryset)
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response(
            {'message': constants.PRIVATE_ACCOUNT},
            status=status.HTTP_403_FORBIDDEN,
        )

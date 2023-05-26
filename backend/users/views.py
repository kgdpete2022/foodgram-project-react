from djoser.views import UserViewSet
from .serializers import (
    CustomUserSerializer,
    FollowSerializer,
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework import status
from .models import Follow
from rest_framework.decorators import action

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if user == author:
            return Response(
                {"errors": "Нельзя подписаться на самого себя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "POST":
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                Follow.objects.create(user=user, author=author)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == "DELETE":
            subscription = get_object_or_404(Follow, user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"errors": "Пользователь не подписан на данного автора"}
            )
        return None

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

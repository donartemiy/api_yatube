from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, User
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        if not User.objects.get(username=self.request.user).is_superuser:
            raise MethodNotAllowed('Недостаточно прав для создания группы')
        serializer.save()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Что бы ссылки в urls заработали"""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user, post=get_object_or_404(Post, pk=post_id))

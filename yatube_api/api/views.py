from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from posts.models import Comment, Group, Post, User
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from django.core.exceptions import PermissionDenied


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        # super(PostViewSet, self).perform_update(serializer) хренабора непонятная
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        if not User.objects.get(username=self.request.user).is_superuser:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Что бы ссылки в urls заработали"""
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post=Post.objects.get(pk=post_id))

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        # super(PostViewSet, self).perform_update(serializer) # хренабора непонятная
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        print('\n\n instance:', instance)
        if self.request.user != instance.author:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()

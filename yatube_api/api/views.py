from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post, User
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    # если убрать, то тесты не проходят: 
    # TestCommentAPI::test_comment_change_by_not_author_with_valid_data[put]
    # TestCommentAPI::test_comment_change_by_not_author_with_valid_data[patch]
    # TestCommentAPI::test_comment_delete_by_author

    def get_queryset(self):
        """Что бы ссылки в urls заработали"""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user, post=get_object_or_404(Post, pk=post_id))

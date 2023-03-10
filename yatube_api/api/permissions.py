from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):    # Метод нужен, без него не
        # не пройти pytest. Будет 4ре fails'a:
        # TestCommentAPI::test_comments_get_unauth
        # TestCommentAPI::test_comments_id_unauth_get
        # TestPostAPI::test_post_not_auth
        # TestPostAPI::test_post_unauth_create
        # ¯\_(ツ)_/¯
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

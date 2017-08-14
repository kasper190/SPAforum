from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)
from .permissions import (
    IsAdminOrModeratorOrReadOnly,
    IsOwnerOrAdminOrModeratorOrReadOnly,
    IsOwnerOrReadOnly,
)
from .serializers import (
    NoteSerializer,
    NoteCreateUpdateSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostListSerializer,
)
from posts.models import (
    Note,
    Post,
)


class NoteCreateAPIView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteCreateUpdateSerializer

    def perform_create(self, serializer):
        post_id = self.request.data['post']
        user_id = self.request.user.id
        is_admin = self.request.user.is_staff
        if serializer.is_valid(raise_exception=True):
            is_moderator = Post.objects.filter(
                id = post_id, 
                thread__subforum__moderators = user_id
            ).exists()
            if not (is_admin or is_moderator):
                raise PermissionDenied(detail='You do not have permission to perform this action.')
        serializer.save(user=self.request.user)


class NoteUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteCreateUpdateSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly, IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class NoteDeleteAPIView(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly, IsOwnerOrReadOnly)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = (IsOwnerOrAdminOrModeratorOrReadOnly,)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (IsAdminOrModeratorOrReadOnly,)
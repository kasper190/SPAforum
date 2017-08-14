from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from posts.models import (
    Post,
    Note,
)
from forum.models import Thread

User = get_user_model()


class UserInNoteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )
        read_only_fields = fields


class UserInPostSerializer(ModelSerializer):
    posts_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'date_joined',
            'posts_count',
        )
        read_only_fields = fields

    def get_posts_count(self, obj):
        return Post.objects.filter(user=obj.id).count()

        
class NoteSerializer(ModelSerializer):
    user = UserInNoteSerializer(many=False, read_only=True)

    class Meta:
        model = Note
        fields = (
            'id',
            'user',
            'note',
            'publish',
            'updated',
        )


class NoteCreateUpdateSerializer(ModelSerializer):
    user = UserInNoteSerializer(many=False, read_only=True)

    class Meta:
        model = Note
        fields = (
            'id',
            'user',
            'post',
            'note',
            'publish',
            'updated',
        )
        read_only_fields = ('user', 'publish', 'updated')


class PostListSerializer(ModelSerializer):
    user = UserInPostSerializer(many=False, read_only=True)
    notes = NoteSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'content',
            'publish',
            'updated',
            'notes',
        )
        read_only_fields = ('user',)


class PostCreateSerializer(ModelSerializer):
    user = UserInPostSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'thread',
            'content',
            'publish',
            'updated',
        )
        read_only_fields = ('user', 'publish', 'updated')


class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'content',
            'updated',
        )
        read_only_fields = ('updated',)

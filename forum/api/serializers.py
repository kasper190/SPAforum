from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    SerializerMethodField,
    SlugField,
)
from forum.models import(
    Category,
    ForumSettings, 
    SubForum, 
    Thread,
)
from posts.api.serializers import PostListSerializer
from posts.models import Post


class ThreadCreateSerializer(ModelSerializer):
    post = CharField()
    thread_slug = SlugField(read_only=True)

    class Meta:
        model = Thread
        fields = (
            'subforum',
            'user',
            'title',
            'post',
            'thread_slug',
        )

    def create(self, validated_data):
        subforum = validated_data['subforum']
        user = validated_data['user']
        title = validated_data['title']
        post = validated_data['post']

        thread_obj = Thread(
            subforum = subforum,
            user = user,
            title = title,
        )
        thread_obj.save()
        post_obj = Post(
            user = thread_obj.user,
            thread = thread_obj,
            content = post,
        )
        post_obj.save()
        
        thread_slug = Thread.objects.get(id=thread_obj.id).thread_slug
        validated_data['thread_slug'] = thread_slug
        return validated_data


class ThreadUpdateSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            'title',
            'is_open',
        )


class ThreadDetailSerializer(ModelSerializer):
    category = SerializerMethodField()
    moderators = SerializerMethodField()
    posts = SerializerMethodField()
    subforum = SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'is_open',
            'moderators',
            'subforum',
            'category',
            'posts',
        )
    
    def get_category(self, obj):
        return obj.subforum.category.category

    def get_moderators(self, obj):
        return obj.subforum.moderators.values_list('username', flat=True).distinct()

    def get_posts(self, obj):
        qs = Post.objects.filter(thread=obj.id).all()
        posts = PostListSerializer(qs, many=True).data
        return posts

    def get_subforum(self, obj):
        return obj.subforum.subforum


class ThreadListSerializer(ModelSerializer):
    user = SerializerMethodField()
    replies_count = SerializerMethodField()
    last_post_author = SerializerMethodField()
    last_post_publish = SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'user',
            'title',
            'thread_slug',
            'publish',
            'is_open',
            'replies_count',
            'last_post_author',
            'last_post_publish',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_replies_count(self, obj):
        posts_count = obj.posts.count()
        if posts_count > 0:
            return posts_count - 1
        else:
            return 0

    def get_last_post_author(self, obj):
        try:
            return obj.posts.order_by('publish').last().user.username
        except:
            return None

    def get_last_post_publish(self, obj):
        try:
            return obj.posts.order_by('publish').last().publish
        except:
            return None
        

class SubForumDetailSerializer(ModelSerializer):
    threads = SerializerMethodField()

    class Meta:
        model = SubForum
        fields = (
            'id',
            'subforum',
            'description',
            'subforum_slug',
            'threads',
        )

    def get_threads(self, obj):
        qs = Thread.objects.filter(subforum=obj.id).all()
        threads = ThreadListSerializer(qs, many=True).data
        return threads


class SubForumListSerializer(ModelSerializer):
    threads_count = SerializerMethodField()
    posts_count = SerializerMethodField()
    last_post_author = SerializerMethodField()
    last_post_publish = SerializerMethodField()

    class Meta:
        model = SubForum
        fields = (
            'subforum',
            'subforum_slug',
            'description',
            'order',
            'threads_count',
            'posts_count',
            'last_post_author',
            'last_post_publish',
        )
        read_only_fields = fields
    
    def get_last_post_author(self, obj):
        try:
            return Post.objects.filter(thread__subforum=obj.id).order_by('publish').last().user.username
        except:
            return None

    def get_last_post_publish(self, obj):
        try:
            return Post.objects.filter(thread__subforum=obj.id).order_by('publish').last().publish
        except:
            return None

    def get_threads_count(self, obj):
        return obj.threads.count()

    def get_posts_count(self, obj):
        return Post.objects.filter(thread__subforum=obj.id).count()


class CategoryListSerializer(ModelSerializer):
    subforums = SubForumListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'category',
            'description',
            'order',
            'subforums',
        )
        read_only_fields = fields


class ForumDetailSerializer(ModelSerializer):
    class Meta:
        model = ForumSettings
        fields = (
            'forum_name',
            'description',
        )
        read_only_fields = fields
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrModeratorOrReadOnly
from .serializers import (
    CategoryListSerializer,
    ForumDetailSerializer,
    SubForumDetailSerializer,
    ThreadCreateSerializer,
    ThreadDetailSerializer,
    ThreadUpdateSerializer,

)
from forum.models import (
    Category,
    ForumSettings,
    SubForum,
    Thread,
)


class SubforumThreadLookupMixin(object):
    def get_object(self):
        subforum_slug_url = self.kwargs['subforum_slug']
        thread_slug_url = self.kwargs['thread_slug']
        return get_object_or_404(
            Thread,
            subforum__subforum_slug = subforum_slug_url,
            thread_slug = thread_slug_url
        ) 


class ForumDetailAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        forum_settings = ForumSettings.objects.last()
        forum_serializer = ForumDetailSerializer(forum_settings, many=False)
        return Response(forum_serializer.data)



class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = (AllowAny,)


class SubforumDetailAPIView(RetrieveAPIView):
    queryset = SubForum.objects.all()
    serializer_class = SubForumDetailSerializer
    lookup_field = 'subforum_slug'
    permission_classes = (AllowAny,)


class ThreadDetailAPIView(SubforumThreadLookupMixin, RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadDetailSerializer
    lookup_fields = ('subforum_slug', 'thread_slug')
    permission_classes = (AllowAny,)


class ThreadCreateAPIView(CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadCreateSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        

class ThreadUpdateAPIView(SubforumThreadLookupMixin, RetrieveUpdateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadUpdateSerializer
    lookup_fields = ('subforum_slug', 'thread_slug')
    permission_classes = (IsAdminOrModeratorOrReadOnly,)

    
class ThreadDeleteAPIView(SubforumThreadLookupMixin, DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadDetailSerializer
    lookup_fields = ('subforum_slug', 'thread_slug')
    permission_classes = (IsAdminOrModeratorOrReadOnly,)
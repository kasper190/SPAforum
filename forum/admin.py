from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import(
    Category,
    ForumSettings,
    SubForum,
    Thread
)
from posts.models import Post


def open_threads(modeladmin, news, queryset):
    queryset.update(is_open=True)
open_threads.short_description = "Open selected Threads"

def close_threads(modeladmin, news, queryset):
    queryset.update(is_open=False)
close_threads.short_description = "Close selected Threads"


class ForumSettingsAdmin(admin.ModelAdmin):
    list_display = ['forum_name', 'description']
    list_editable = list_display
    list_display_links = None

    class Meta:
        model = ForumSettings

    def get_actions(self, request):
        actions = super(ForumSettingsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['category', 'description']
    list_editable = ['description']


class ThreadInline(admin.TabularInline):
    model = Thread
    extra = 0
    ordering = ['publish']


class SubForumAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['subforum', 'description', 'category']
    list_editable = ['description']
    readonly_fields = ['subforum_slug']
    inlines = [ThreadInline]


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    ordering = ['publish']


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'subforum', 'publish', 'user', 'is_open']
    readonly_fields = ['thread_slug']
    list_filter = ['publish', 'is_open']
    search_fields = ['title', 'user__username']
    actions = [open_threads, close_threads]
    ordering = ['-publish']
    inlines = [PostInline]


try:
    forum_name = ForumSettings.objects.last()
except:
    forum_name = _('Forum')
admin.site.site_header = forum_name
admin.site.index_title = _('Forum administration')
admin.site.site_title = forum_name


admin.site.register(ForumSettings, ForumSettingsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubForum, SubForumAdmin)
admin.site.register(Thread, ThreadAdmin)
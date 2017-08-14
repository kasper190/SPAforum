from django.contrib import admin
from .models import (
    Post,
    Note
)


def part_of_content(obj):
    return ("%s" % (obj.content)[:70])
part_of_content.short_description = "Part of content"

def part_of_note(obj):
    return ("%s" % (obj.note)[:70])
part_of_note.short_description = "Part of note"


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    ordering = ['publish']


class PostAdmin(admin.ModelAdmin):
    list_display = [part_of_content, 'thread', 'user', 'publish']
    list_filter = ['publish']
    search_fields = ['content', 'thread__title', 'user__username']
    ordering = ['-publish']
    inlines = [NoteInline]


class NoteAdmin(admin.ModelAdmin):
    list_display = [part_of_note, 'post', 'user', 'publish']
    list_filter = ['publish']
    search_fields = ['note', 'post__content', 'user__username']
    ordering = ['-publish']


admin.site.register(Post, PostAdmin)
admin.site.register(Note, NoteAdmin)
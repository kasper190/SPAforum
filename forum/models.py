from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class SingletonForumSettings(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonForumSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class ForumSettings(SingletonForumSettings):
    forum_name = models.CharField(max_length=120, default='My Forum')
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('settings')

    def __str__(self):
        return self.forum_name


class Category(models.Model):
    category = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.category


class SubForum(models.Model):
    category = models.ForeignKey(Category, related_name='subforums', on_delete=models.CASCADE)
    subforum = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=200, blank=True)
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    subforum_slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.subforum

    def save(self, *args, **kwargs):
        self.subforum_slug = slugify(self.subforum) 
        super(SubForum, self).save(*args, **kwargs)

    def get_moderators(self):
        return self.moderators.all()

    def get_threads(self):
        return SubForum.objects.get(id=self.id).threads.all()

    def get_posts_in_subforum(self):
        return Thread.objects.get(subforum=self.id).posts.all()


class Thread(models.Model):
    subforum = models.ForeignKey(SubForum, related_name='threads', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads')
    title = models.CharField(max_length=120)
    publish = models.DateField(auto_now=False, auto_now_add=True)
    is_open = models.BooleanField(default=True)
    thread_slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            thread_obj = Thread.objects.get(id=self.id)
            super(Thread, self).save(*args, **kwargs)
        except Thread.DoesNotExist:
            super(Thread, self).save(*args, **kwargs)
            thread_obj = Thread.objects.filter(id=self.id).update(thread_slug = slugify(str(self.id) + '-' + self.title))
        return thread_obj
    
    def get_posts_in_thread(self):
        return Thread.objects.get(id=self.id).posts.all()
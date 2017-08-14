from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView
from ang.views import AngularTemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/forum/', include("forum.api.urls", namespace='forum')),
    url(r'^api/post/', include("posts.api.urls", namespace='post')),
    url(r'^api/user/', include("accounts.api.urls", namespace='accounts')),
    url(r'^api/templates/(?P<item>[A-Za-z0-9\_\-\.\/]+)\.html$',  AngularTemplateView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns +=  [
    url(r'^.*', TemplateView.as_view(template_name='ang/home.html'))
]
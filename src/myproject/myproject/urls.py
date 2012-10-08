from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateView
from useful.django.views import serve_with_Expires

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

 url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^%s/' % getattr(settings, 'ADMIN_URL', 'admin'), include(admin.site.urls)),

) + static.static(settings.STATIC_URL, serve_with_Expires) \
  + static.static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)

if not settings.SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY must be set to an "
                               "installation-specific value in local settings.")

if not getattr(settings, 'HTTP_PORT', None):
    raise ImproperlyConfigured("No HTTP_PORT setting, was this installation "
                               "configured from the INSTALLATIONS dict?")

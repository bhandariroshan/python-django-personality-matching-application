# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from .views import AboutView, ContactView, HomeView
from .views import MailView, GalleryView, QuizView
from .views import ResultView, ProfileView
from sciencerunaway.users.views import SignupView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^accounts/signup/$', SignupView.as_view(), name='signup'),
    url(r'^contacts/$', ContactView.as_view(), name='contact'),
    url(r'^mailing/$', MailView.as_view(), name='mail'),
    url(r'^gallery/$', GalleryView.as_view(), name='gallery'),
    url(r'^quiz/$', QuizView.as_view(), name='quiz'),
    url(r'^result/$', ResultView.as_view(), name='result'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('sciencerunaway.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

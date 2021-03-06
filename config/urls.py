# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from chamados.autentica import views

urlpatterns = [
	# Django Admin, use {% url 'admin:index' %}
	url(settings.ADMIN_URL, admin.site.urls),

	# Your stuff: custom urls includes go here
	url(r'^telefonia/', include('chamados.telefonia.urls', namespace='telefonia')),
	url(r'^autentica/', include('chamados.autentica.urls', namespace='autentica')),
	#url(r'^login/$', auth_views.login, name='login'),
	#url(r'^logout/$', auth_views.logout, name='logout'),
	#url(r'^logout/$', include('django.contrib.auth.views.logout', {'next_page': '/telefonia/'}, namespace='logout')),
	url(r'^loga/$', views.loga, name='loga'),
	url(r'^sair/$', views.sair, name='sair'),
	url(r'^valida-usuario/$', views.valida_usuario, name='valida-usuario'),

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

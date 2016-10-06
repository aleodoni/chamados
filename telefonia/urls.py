# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from telefonia.views import TrocaEquipamentoIndexView

urlpatterns = [
	url(r'^$', views.index, name='index'),
	#url(r'^chamado/$', views.chamado, name='chamado'),
	#url(r'^exclui/$', views.exclui, name='exclui'),
	url(r'^exclui/(?P<pk>[0-9]+)/$', views.ChamadoDeleteView.as_view(), name='exclui'),
	#url(r'^troca/$', views.troca_index, name='index'),
	url(r'^troca/(?P<pk>[0-9]+)/$', views.TrocaEquipamentoIndexView.as_view(), name='index'),
	url(r'^troca/(?P<pk>[0-9]+)/nova/$', views.TrocaEquipamentoView.as_view(), name='nova'),
	url(r'^troca/(?P<id_chamado>[0-9]+)/edita/(?P<pk>[0-9]+)/$', views.TrocaEquipamentoUpdateView.as_view(), name='edita'),
	url(r'^troca/(?P<id_chamado>[0-9]+)/deleta/(?P<pk>[0-9]+)/$', views.TrocaEquipamentoDeleteView.as_view(), name='deleta'),
	url(r'^relatorio/chamados.pdf$', views.HelloPDFView.as_view(), name='relatorio_chamados'),
	url(r'^chamado/$', views.ChamadoCreateView.as_view(), name='chamado'),
	url(r'^chamado/edita/(?P<pk>[0-9]+)/$', views.ChamadoUpdateView.as_view(), name='edita'),
	url(r'^chamado_terceiro/$', views.ChamadoTerceiroCreateView.as_view(), name='chamado_terceiro'),
	url(r'^ramais/$', views.ListaRamaisView.as_view(), name='ramais'),

	url(r'^api/depto/$', views.departamento_json, name='api-depto'),
]
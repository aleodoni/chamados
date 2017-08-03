# -*- coding: utf-8 -*-

import os
import json
import codecs
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_date
from django.views import generic
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from datetime import datetime    

from .models import Status, Executor, Chamado, Urgencia, TrocaEquipamento, Ramal, Departamento

from .forms import PesquisaForm, PesquisaRamaisForm
from .forms import ChamadoForm
from .forms import TrocaForm
from .forms import ChamadoTerceiroForm

from .util import status_default, executor_default

from easy_pdf.views import PDFTemplateView

#from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):

	# busca status, executor default para fazer pesquisa inicial
	status_default = Status.objects.filter(default=True)
	executor_default = Executor.objects.filter(default=True)
	lista_chamado = Chamado.objects.order_by('abertura')
	atendente = ''
	status = ''
	abertura = ''
	fechamento = ''

	form = PesquisaForm()

	if status_default.exists():
		if request.method == 'POST':
			form = PesquisaForm(request.POST)
			filtro_status = request.POST['status']
			flag_pesquisa = True
			status = filtro_status
			status_default_id = '0'
		else:
			filtro_status = status_default[0].id
			flag_pesquisa = False
		if filtro_status != '':
			lista_chamado = lista_chamado.filter(status=filtro_status)

	if executor_default.exists():
		if request.method == 'POST':
			filtro_executor = request.POST['atendente']
			atendente = filtro_executor
		else:
			filtro_executor = executor_default[0].id
		if filtro_executor != '':
			lista_chamado = lista_chamado.filter(executor=filtro_executor)

	if 'dtinicio' in request.POST:
		if not request.POST['dtinicio'] == '':
			abertura = request.POST['dtinicio']
			lista_chamado = lista_chamado.filter(abertura__gte=datetime.strptime(request.POST['dtinicio'], "%d/%m/%Y").date())

	if 'dtfim' in request.POST:
		if not request.POST['dtfim'] == '':
			fechamento = request.POST['dtfim']
			lista_chamado = lista_chamado.filter(abertura__lte=datetime.strptime(request.POST['dtfim'], "%d/%m/%Y").date())
	
	context = {'lista_chamado': lista_chamado, 'flag_pesquisa': flag_pesquisa, 'atendente': atendente, 'form': form, 'filtro_status': filtro_status, 'filtro_executor': filtro_executor, 'abertura': abertura, 'fechamento': fechamento}
	return render(request, 'telefonia/index.html', context)


class TrocaEquipamentoIndexView(generic.ListView):
	model = TrocaEquipamento
	template_name = 'telefonia/troca_index.html'
	context_object_name = 'troca_list'

	def get_queryset(self):
		pk = 0
		if 'pk' in self.kwargs:
			pk = int(self.kwargs['pk'])
		if pk > 0:
			lista = TrocaEquipamento.objects.order_by('chamado')
			lista = lista.filter(chamado=pk)
		else:
			lista = None
		return lista

	def get_context_data(self, **kwargs):
		context = super(generic.ListView, self).get_context_data(**kwargs)
		if 'pk' in self.kwargs:
			context['id_chamado'] = self.kwargs['pk']
			chamado = Chamado.objects.get(pk=context['id_chamado'])
		context['chamado'] = chamado
		return context

class TrocaEquipamentoView(SuccessMessageMixin, CreateView):
	template_name = 'telefonia/troca_add.html'
	model = TrocaEquipamento
	form_class = TrocaForm
	success_url = ''
	success_message = "Troca incluída com sucesso"

	def get_context_data(self, **kwargs):
		context = super(generic.CreateView, self).get_context_data(**kwargs)
		if 'pk' in self.kwargs:
			context['id_chamado'] = self.kwargs['pk']
		return context

	def get_initial(self):
		return { 'serial_velho': '', 'serial_novo': '', 'motivo': '' }

	def get_success_url(self):
		if 'pk' in self.kwargs:
			pk = self.kwargs['pk']
		else:
			pk = 0
		return ('/telefonia/troca/' + pk)


class TrocaEquipamentoUpdateView(SuccessMessageMixin, UpdateView):
	template_name = 'telefonia/troca_add.html'
	model = TrocaEquipamento
	form_class = TrocaForm
	success_url = ''
	success_message = "Troca alterada com sucesso"

	def get_context_data(self, **kwargs):
		context = super(generic.UpdateView, self).get_context_data(**kwargs)
		if 'id_chamado' in self.kwargs:
			context['id_chamado'] = self.kwargs['id_chamado']
		return context

	def get_success_url(self):
		if 'id_chamado' in self.kwargs:
			id_chamado = self.kwargs['id_chamado']
		else:
			id_chamado = 0
		return ('/telefonia/troca/' + id_chamado)		

class TrocaEquipamentoDeleteView(DeleteView):
	template_name = ''
	model = TrocaEquipamento
	success_url = ''
	success_message = "Troca excluída com sucesso"

	def get_success_url(self):
		if 'id_chamado' in self.kwargs:
			id_chamado = self.kwargs['id_chamado']
		else:
			id_chamado = 0
		return ('/telefonia/troca/' + id_chamado)

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(TrocaEquipamentoDeleteView, self).delete(request, *args, **kwargs)


class HelloPDFView(PDFTemplateView):
	template_name = 'telefonia/relatorio.html'
	status = 0
	atendente = 0
	abertura = ''
	fechamento = ''
	chamados = None

	def get_context_data(self, **kwargs):
		context = super(PDFTemplateView, self).get_context_data(**kwargs)
		context['title'] = 'Relatório de Chamados'
		context['pagesize'] = 'A4 landscape'

		chamados = Chamado.objects.order_by('abertura')
		if self.status != '':
			chamados = chamados.filter(status=self.status)
		if self.atendente != '':
			chamados = chamados.filter(executor=self.atendente)
		if self.abertura != '':
			chamados = chamados.filter(abertura__gte=datetime.strptime(self.abertura, "%d/%m/%Y").date())
			context['data_inicio'] = datetime.strptime(self.abertura, "%d/%m/%Y").date()
		if self.fechamento != '':
			chamados = chamados.filter(abertura__lte=datetime.strptime(self.fechamento, "%d/%m/%Y").date())
			context['data_fim'] = datetime.strptime(self.fechamento, "%d/%m/%Y").date()
		context['chamados'] = chamados
		return context

	def get(self, request, *args, **kwargs):
		context = super(PDFTemplateView, self).get_context_data(**kwargs)
		self.status =  request.GET['pstatus']
		self.atendente =  request.GET['patendente']
		self.abertura =  request.GET['pabertura']
		self.fechamento =  request.GET['pfechamento']
		return super(HelloPDFView, self).get(request, *args, **kwargs)

class ChamadoCreateView(SuccessMessageMixin, CreateView):
	template_name = 'telefonia/chamado.html'
	model = Chamado
	form_class = ChamadoForm
	success_url = '/telefonia/'
	success_message = "Chamado adicionado com sucesso"

	def get_initial(self):
		return { 'solicitante': '', 'problema': '', 'execucao': '', 'status': 2, 'urgencia': 2, 'executor': 1, 'email_solicitante': '' }

class ChamadoUpdateView(SuccessMessageMixin, UpdateView):
	template_name = 'telefonia/chamado.html'
	model = Chamado
	form_class = ChamadoForm
	success_url = '/telefonia'
	success_message = "Chamado atualizado com sucesso"

	def form_valid(self, form):
		form.envia_email_atualizacao()
		return super(ChamadoUpdateView, self).form_valid(form)

class ChamadoDeleteView(DeleteView):
	template_name = ''
	model = Chamado
	success_url = '/telefonia'
	success_message = "Chamado excluído com sucesso"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(ChamadoDeleteView, self).delete(request, *args, **kwargs)

#-----------------------------------------------------------------------------------------------------------------------------
# classes para abertura de chamados por terceiros
#-----------------------------------------------------------------------------------------------------------------------------
class ChamadoTerceiroCreateView(SuccessMessageMixin, CreateView):
	template_name = 'telefonia/chamado_terceiro.html'
	model = Chamado
	form_class = ChamadoTerceiroForm
	success_url = '/telefonia/chamado_terceiro'
	success_message = "Chamado adicionado com sucesso. O setor de Telefonia entrará em contato brevemente."

	def get_initial(self):
		return { 'solicitante': '', 'problema': '', 'email_solicitante': ''}

	def form_valid(self, form):
		form.send_email()
		return super(ChamadoTerceiroCreateView, self).form_valid(form)


#-----------------------------------------------------------------------------------------------------------------------------
# classes de segurança/acesso
#-----------------------------------------------------------------------------------------------------------------------------		
#class ChamadosLoginRequired(LoginRequiredMixin):
#	login_url = "/login/"	


#-----------------------------------------------------------------------------------------------------------------------------
# classes para pesquisa/listagem de ramais
#-----------------------------------------------------------------------------------------------------------------------------		
class ListaRamaisView(SuccessMessageMixin, FormView):
	template_name = "telefonia/ramais.html"
	form_class = PesquisaRamaisForm

	def get(self, request, *args, **kwargs):

		context = self.get_context_data(**kwargs)

		departamento = self.request.GET.get('departamento','')
		pessoa = self.request.GET.get('pessoa','')

		lista_ramais = Ramal.objects.order_by('departamento__nome')
		if (departamento != ''):
			lista_ramais = lista_ramais.filter(departamento__nome__icontains=departamento)
		if (pessoa != ''):
			lista_ramais = lista_ramais.filter(nome__icontains=pessoa)

		data = {'departamento': departamento, 'pessoa': pessoa}
		form = PesquisaRamaisForm(initial=data)

		context['form'] = form
		context['lista_ramais'] = lista_ramais

		return self.render_to_response(context)



#-----------------------------------------------------------------------------------------------------------------------------
# gera json com lista de departamentos
#-----------------------------------------------------------------------------------------------------------------------------		
def departamento_json(request):
	resposta = []

	for e in Departamento.objects.all():
		depto_json = {}
		depto_json['nome'] = e.nome
		resposta.append(depto_json)

	data = json.dumps(resposta)
	
	return HttpResponse(
		#json.dumps(resposta, cls=DjangoJSONEncoder),
		data,
		content_type="application/json"
	)			


#-----------------------------------------------------------------------------------------------------------------------------
# Relatório lista de ramais
#-----------------------------------------------------------------------------------------------------------------------------		
class RamaisPDFView(PDFTemplateView):
	template_name = 'telefonia/relatorio_ramais.html'
	departamento = ''
	pessoa = ''
	lista_ramais = None

	def get_context_data(self, **kwargs):
		context = super(PDFTemplateView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de Ramais'
		context['pagesize'] = 'A4 portrait'

		lista_ramais = Ramal.objects.order_by('departamento__nome')

		if (self.departamento != ''):
			lista_ramais = lista_ramais.filter(departamento__nome__icontains=self.departamento)
		if (self.pessoa != ''):
			lista_ramais = lista_ramais.filter(nome__icontains=self.pessoa)

		context['lista_ramais'] = lista_ramais
		return context

	def get(self, request, *args, **kwargs):
		context = super(PDFTemplateView, self).get_context_data(**kwargs)
		self.departamento =  self.request.GET.get('pdepartamento', '')
		self.pessoa =  self.request.GET.get('ppessoa', '')
		return super(RamaisPDFView, self).get(request, *args, **kwargs)	
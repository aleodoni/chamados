# -*- coding: utf-8 -*-

from django import forms
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime    
from .models import Status, Executor, Departamento, Ramal, Urgencia, Chamado, TrocaEquipamento, TipoEquipamento, ProblemasComuns

class PesquisaForm(forms.Form):
	status_default = Status.objects.filter(default=True)
	executor_default = Executor.objects.filter(default=True)
	status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label='TODOS')
	atendente = forms.ModelChoiceField(queryset=Executor.objects.all(), empty_label='TODOS')
	dtinicio = forms.DateField()
	dtfim = forms.DateField()

class ChamadoForm(forms.ModelForm):
	class Meta:
		model = Chamado
		fields = ('id', 'abertura', 'fechamento', 'solicitante', 'departamento', 'ramal_atendimento', 'ramal_contato', 'problema', 'execucao', 'status', 'urgencia', 'executor', 'email_solicitante', 'problema_comum')

	id = forms.CharField(widget=forms.HiddenInput)
	
	#id = forms.IntegerField()
	#abertura = forms.DateField()
	#fechamento = forms.DateField(required=False)
	#solicitante = forms.CharField()
	departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label=None)
	ramal_atendimento = forms.ModelChoiceField(queryset=Ramal.objects.all(), empty_label=None)
	ramal_contato = forms.ModelChoiceField(queryset=Ramal.objects.all(), empty_label=None)
	#problema = forms.CharField(required=False)
	#execucao = forms.CharField(required=False)
	status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label=None)
	urgencia = forms.ModelChoiceField(queryset=Urgencia.objects.all(), empty_label=None)
	executor = forms.ModelChoiceField(queryset=Executor.objects.all(), empty_label=None)
	problema_comum = forms.ModelChoiceField(queryset=ProblemasComuns.objects.all(), empty_label=None)

	def envia_email_atualizacao(self):
		assunto = 'Setor de Telefonia - Atualização de Chamado'
		para = [self.cleaned_data['email_solicitante']]
		de = 'telefonia@gmail.com'
		ctx = {
			'abertura': self.cleaned_data['abertura'],
			'departamento': self.cleaned_data['departamento'],
			'solicitante': self.cleaned_data['solicitante'],
			'ramal_defeito': self.cleaned_data['ramal_atendimento'],
			'ramal_contato': self.cleaned_data['ramal_contato'],
			'problema': self.cleaned_data['problema'],
			'problema_comum': self.cleaned_data['problema_comum'],
			'fechamento': self.cleaned_data['fechamento'],
			'status': self.cleaned_data['status'],
			'urgencia': self.cleaned_data['urgencia'],
			'executor': self.cleaned_data['executor'],
			'execucao': self.cleaned_data['execucao']
		}
		mensagem = get_template('telefonia/email_atualizacao.txt').render(Context(ctx))
				
		EmailMessage(assunto, mensagem, to=para, from_email=de).send()


class TrocaForm(forms.ModelForm):
	class Meta:
		model = TrocaEquipamento
		fields = ('chamado', 'tipo_equipamento', 'serial_velho', 'serial_novo', 'motivo')

	tipo_equipamento = forms.ModelChoiceField(queryset=TipoEquipamento.objects.all(), empty_label=None)

class ChamadoTerceiroForm(forms.ModelForm):
	class Meta:
		model = Chamado
		fields = ('id', 'abertura', 'departamento', 'ramal_atendimento', 'ramal_contato', 'problema', 'solicitante', 'email_solicitante', 'problema_comum')

	id = forms.CharField(widget=forms.HiddenInput)
	departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label=None)
	ramal_atendimento = forms.ModelChoiceField(queryset=Ramal.objects.all(), empty_label=None)
	ramal_contato = forms.ModelChoiceField(queryset=Ramal.objects.all(), empty_label=None)
	problema_comum = forms.ModelChoiceField(queryset=ProblemasComuns.objects.all(), empty_label=None)
	abertura = forms.DateField(initial=datetime.now)

	def send_email(self):
		assunto = 'Setor de Telefonia - Abertura de Chamado'
		para = [self.cleaned_data['email_solicitante']]
		de = 'telefonia@gmail.com'
		ctx = {
			'abertura': self.cleaned_data['abertura'],
			'departamento': self.cleaned_data['departamento'],
			'solicitante': self.cleaned_data['solicitante'],
			'ramal_defeito': self.cleaned_data['ramal_atendimento'],
			'ramal_contato': self.cleaned_data['ramal_contato'],
			'problema': self.cleaned_data['problema'],
			'problema_comum': self.cleaned_data['problema_comum'],
		}
		mensagem = get_template('telefonia/email_abertura.txt').render(Context(ctx))
				
		EmailMessage(assunto, mensagem, to=para, from_email=de).send()
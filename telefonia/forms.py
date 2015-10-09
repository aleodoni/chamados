from django import forms
from .models import Status, Executor, Departamento, Ramal, Urgencia, Chamado, TrocaEquipamento, TipoEquipamento

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
		fields = ('id', 'abertura', 'fechamento', 'solicitante', 'departamento', 'ramal_atendimento', 'ramal_contato', 'problema', 'execucao', 'status', 'urgencia', 'executor')

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

class TrocaForm(forms.ModelForm):
	class Meta:
		model = TrocaEquipamento
		fields = ('chamado', 'tipo_equipamento', 'serial_velho', 'serial_novo', 'motivo')

	tipo_equipamento = forms.ModelChoiceField(queryset=TipoEquipamento.objects.all(), empty_label=None)

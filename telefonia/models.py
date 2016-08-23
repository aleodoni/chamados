# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

#--------------------------------------------------------------------------------------
class Departamento(models.Model):
	nome = models.CharField(max_length=300)

	def __unicode__(self):
		return self.nome

#--------------------------------------------------------------------------------------
class Ramal(models.Model):
	nome = models.CharField(max_length=200)
	numero = models.CharField(max_length=20)

	def __unicode__(self):
		return self.nome + ' - ' + self.numero

	class Meta:
		verbose_name_plural = "ramais"

#--------------------------------------------------------------------------------------
class Problemas(models.Model):
	nome = models.CharField(max_length=500)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name_plural = "problemas"

#--------------------------------------------------------------------------------------
class Status(models.Model):
	nome = models.CharField(max_length=100)
	default = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name_plural = "status"

#--------------------------------------------------------------------------------------
class Urgencia(models.Model):
	nome = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nome

#--------------------------------------------------------------------------------------
class Executor(models.Model):
	nome = models.CharField(max_length=100)
	default = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name_plural = "executores"

#--------------------------------------------------------------------------------------
class Chamado(models.Model):
	abertura = models.DateField()
	fechamento = models.DateField(blank=True, null=True)
	solicitante = models.CharField(max_length=300)
	departamento = models.ForeignKey('Departamento')
	ramal_atendimento = models.ForeignKey('Ramal', related_name="ramal_atendimento")
	ramal_contato = models.ForeignKey('Ramal', related_name="ramal_contato")
	problema = models.CharField(max_length=500, blank=True, null=True)
	execucao = models.CharField(max_length=300, blank=True, null=True)
	status = models.ForeignKey('Status')
	urgencia = models.ForeignKey('Urgencia')
	executor = models.ForeignKey('Executor')
	email_solicitante = models.EmailField(blank=True, null=True)

	def __unicode__(self):
		return "Chamado : " + unicode(self.id)

	# foi sobrescrito o metodo save para contemplar a nova tela de chamados de terceiros onde os campos 
	# status, urgencia e executor nao sao informados pelo usuario e o sistema devera buscar os valores
	# padrao no banco de dados
	# ATENCAO - deve-se alterar os valores abaixo (pk=?) para buscar os valores padrao do BD de cada um
	#           estes valores foram definidos como variáveis globais no arquivo settings.py

	def save(self, *args, **kwargs):                                       
		if getattr(self, 'status', None) == None:
			status = Status.objects.get(pk=settings.STATUS_DEFAULT)
			self.status = status
		if getattr(self, 'urgencia', None) == None:
			urgencia = Urgencia.objects.get(pk=settings.URGENCIA_DEFAULT)
			self.urgencia = urgencia
		if getattr(self, 'executor', None) == None:
			executor = Executor.objects.get(pk=settings.EXECUTOR_DEFAULT)
			self.executor = executor
		super(Chamado, self).save(*args, **kwargs)   

#--------------------------------------------------------------------------------------
class TipoEquipamento(models.Model):
	nome = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nome

#--------------------------------------------------------------------------------------
class TrocaEquipamento(models.Model):
	chamado = models.ForeignKey('Chamado')
	tipo_equipamento = models.ForeignKey('TipoEquipamento')
	serial_velho = models.CharField(max_length=50, null=True)
	serial_novo = models.CharField(max_length=50, null=True)
	motivo = models.CharField(max_length=500, blank=True, null=True)

#--------------------------------------------------------------------------------------
class ProblemasComuns(models.Model):
	problema = models.CharField(max_length=500)

	def __unicode__(self):
		return self.nome

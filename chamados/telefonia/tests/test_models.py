from django.test import TestCase
from chamados.telefonia.models import Departamento, Ramal, Problemas, Status, Urgencia, Executor, TipoEquipamento, ProblemasComuns, Chamado, TrocaEquipamento
from django.db import IntegrityError, DataError

#-------------------------------------------------------------------------------------------------
class DepartamentoTestCase(TestCase):
	def setUp(self):
		Departamento.objects.create(nome="Telefonia")

	def test_departamento_foi_criado(self):
		telefonia = Departamento.objects.get(nome="Telefonia")
		self.assertEqual(telefonia.nome, 'Telefonia')

#-------------------------------------------------------------------------------------------------	
class RamalTestCase(TestCase):

	def setUp(self):
		self.depto = Departamento.objects.create(nome="Gabinete Zezinho")
		Ramal.objects.create(nome="Zezinho", numero="1234", departamento=self.depto)

	def test_ramal_inserido(self):
		ramal = Ramal.objects.get(nome="Zezinho")
		self.assertEqual(ramal.nome, 'Zezinho')

	def test_ramal_numero_nulo(self):
		with self.assertRaises(IntegrityError):
			ramal = Ramal.objects.create(nome='Nome', numero=None, departamento=self.depto)

	def test_ramal_departamento_nulo(self):
		with self.assertRaises(IntegrityError):
			Ramal.objects.create(nome='Nome', numero='1234567890123456789')

	def test_ramal_numero_maior_20(self):
		with self.assertRaises(DataError):
			Ramal.objects.create(nome='Nome', numero='12345678901234567890000000')

	def test_ramal_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			ramal = Ramal.objects.create(nome=None, numero='123456', departamento=self.depto)

#-------------------------------------------------------------------------------------------------
class ProblemasTestCase(TestCase):
	def setUp(self):
		Problemas.objects.create(nome="Telefone quebrado")

	def test_problema_foi_criado(self):
		problema = Problemas.objects.get(nome="Telefone quebrado")
		self.assertEqual(problema.nome, 'Telefone quebrado')

	def test_problema_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			problema = Problemas.objects.create(nome=None)

#-------------------------------------------------------------------------------------------------
class StatusTestCase(TestCase):
	def setUp(self):
		Status.objects.create(nome="Status criado")

	def test_status_foi_criado(self):
		status = Status.objects.get(nome="Status criado")
		self.assertEqual(status.nome, 'Status criado')

	def test_status_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			status = Status.objects.create(nome=None)			

#-------------------------------------------------------------------------------------------------
class UrgenciaTestCase(TestCase):
	def setUp(self):
		Urgencia.objects.create(nome="Urgencia criado")

	def test_urgencia_foi_criado(self):
		urgencia = Urgencia.objects.get(nome="Urgencia criado")
		self.assertEqual(urgencia.nome, 'Urgencia criado')

	def test_urgencia_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			urgencia = Urgencia.objects.create(nome=None)						

#-------------------------------------------------------------------------------------------------
class ExecutorTestCase(TestCase):
	def setUp(self):
		Executor.objects.create(nome="Executor criado")

	def test_executor_foi_criado(self):
		executor = Executor.objects.get(nome="Executor criado")
		self.assertEqual(executor.nome, 'Executor criado')

	def test_executor_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			executor = Executor.objects.create(nome=None)									

#-------------------------------------------------------------------------------------------------
class TipoEquipamentoTestCase(TestCase):
	def setUp(self):
		TipoEquipamento.objects.create(nome="Tipo de equipamento criado")

	def test_tipo_equipamento_foi_criado(self):
		tipo_equipamento = TipoEquipamento.objects.get(nome="Tipo de equipamento criado")
		self.assertEqual(tipo_equipamento.nome, 'Tipo de equipamento criado')

	def test_tipo_equipamento_nome_nulo(self):
		with self.assertRaises(IntegrityError):
			executor = TipoEquipamento.objects.create(nome=None)												

#-------------------------------------------------------------------------------------------------
class ProblemasComunsTestCase(TestCase):
	def setUp(self):
		ProblemasComuns.objects.create(problema="Problema comum criado", estimado=1)

	def test_problema_comum_foi_criado(self):
		problema_comum = ProblemasComuns.objects.get(problema="Problema comum criado", estimado=1)
		self.assertEqual(problema_comum.problema, 'Problema comum criado')

	def test_problema_comum_problema_nulo(self):
		with self.assertRaises(IntegrityError):
			executor = ProblemasComuns.objects.create(problema=None, estimado=1)															

	def test_problema_comum_estimado_nulo(self):
		with self.assertRaises(IntegrityError):
			executor = ProblemasComuns.objects.create(problema='Problema comum criado', estimado=None)															

#-------------------------------------------------------------------------------------------------
class ChamadoTestCase(TestCase):
	def setUp(self):
		self.depto = Departamento.objects.create(nome="Telefonia")
		self.ramal_at = Ramal.objects.create(nome="Zezinho", numero="1234", departamento=self.depto)
		self.ramal_co = Ramal.objects.create(nome="Zezinho", numero="1234", departamento=self.depto)
		self.status = Status.objects.create(nome="Status criado")
		self.urgencia = Urgencia.objects.create(nome="Urgencia criado")
		self.executor = Executor.objects.create(nome="Executor criado")
		self.problema_comum = ProblemasComuns.objects.create(problema="Problema comum criado", estimado=1)
		Chamado.objects.create(abertura="2017-01-01", fechamento=None, solicitante='Solicitante', departamento=self.depto, ramal_atendimento=self.ramal_at, ramal_contato=self.ramal_co, problema='Problema', execucao='Execucao', status=self.status, urgencia=self.urgencia, executor=self.executor, problema_comum=self.problema_comum, email_solicitante='solicitante@a.com', executado=None)

	def test_chamado_foi_criado(self):
		chamado = Chamado.objects.get(solicitante='Solicitante')
		self.assertEqual(chamado.solicitante, 'Solicitante')

	def test_chamado_abertura_nula(self):
		with self.assertRaises(IntegrityError):
			Chamado.objects.create(abertura=None, fechamento=None, solicitante='Solicitante', departamento=self.depto, ramal_atendimento=self.ramal_at, ramal_contato=self.ramal_co, problema='Problema', execucao='Execucao', status=self.status, urgencia=self.urgencia, executor=self.executor, problema_comum=self.problema_comum, email_solicitante='solicitante@a.com', executado=None)

#-------------------------------------------------------------------------------------------------
class TrocaEquipamentoTestCase(TestCase):
	def setUp(self):
		self.depto = Departamento.objects.create(nome="Telefonia")
		self.ramal_at = Ramal.objects.create(nome="Zezinho", numero="1234", departamento=self.depto)
		self.ramal_co = Ramal.objects.create(nome="Zezinho", numero="1234", departamento=self.depto)
		self.status = Status.objects.create(nome="Status criado")
		self.urgencia = Urgencia.objects.create(nome="Urgencia criado")
		self.executor = Executor.objects.create(nome="Executor criado")
		self.problema_comum = ProblemasComuns.objects.create(problema="Problema comum criado", estimado=1)
		self.chamado = Chamado.objects.create(abertura="2017-01-01", fechamento=None, solicitante='Solicitante', departamento=self.depto, ramal_atendimento=self.ramal_at, ramal_contato=self.ramal_co, problema='Problema', execucao='Execucao', status=self.status, urgencia=self.urgencia, executor=self.executor, problema_comum=self.problema_comum, email_solicitante='solicitante@a.com', executado=None)
		self.tipo_equipamento = TipoEquipamento.objects.create(nome="Tipo de equipamento criado")
		TrocaEquipamento.objects.create(chamado=self.chamado, tipo_equipamento=self.tipo_equipamento, serial_velho=None, serial_novo=None, motivo=None)

	def test_troca_equipamento_foi_criado(self):
		troca_equipamento = TrocaEquipamento.objects.get(id=1)
		self.assertEqual(troca_equipamento.id, 1)

	

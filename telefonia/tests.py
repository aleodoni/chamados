from django.test import TestCase
from telefonia.models import Departamento

# Create your tests here.

class DepartamentoTestCase(TestCase):
    def setUp(self):
        Departamento.objects.create(nome="Telefonia")

    def test_departamento_foi_criado(self):
        telefonia = Departamento.objects.get(nome="Telefonia")
        self.assertEqual(telefonia.nome, 'Telefonia')

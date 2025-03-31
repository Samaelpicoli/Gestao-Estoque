from django.test import TestCase

from suppliers.models import Supplier


class TestsModelsSupplier(TestCase):
    """Testes unitários para o modelo Supplier."""

    def setUp(self):
        """Configuração inicial para os testes.

        Cria uma instância de Supplier para ser usada nos testes.
        """
        self.supplier = Supplier.objects.create(name='Ivan')

    def test_str_de_supplier_deve_retornar_seu_nome(self):
        """
        Testa se o método __str__ retorna corretamente o nome do fornecedor.
        """
        esperado = 'Ivan'
        resultado = str(self.supplier)
        self.assertEqual(esperado, resultado)

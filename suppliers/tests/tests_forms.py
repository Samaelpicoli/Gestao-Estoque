from django.test import TestCase

from suppliers.forms import SupplierForm
from suppliers.models import Supplier


class TestsFormsSupplier(TestCase):
    """Testes para validação do formulário de Supplier (SupplierForm)"""

    def setUp(self):
        """Configuração inicial para criação de um fornecedor."""
        self.supplier = Supplier.objects.create(name='Ivan')

    def test_supplier_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = SupplierForm(
            data={'name': 'Logitech', 'description': 'Para notebooks'}
        )
        self.assertTrue(form.is_valid())

    def test_supplier_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando o
        campo 'name' não é preenchido.
        """
        form = SupplierForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

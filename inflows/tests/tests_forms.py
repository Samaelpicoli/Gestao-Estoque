from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from inflows.forms import InflowForm
from products.models import Product
from suppliers.models import Supplier


class TestsFormsInflow(TestCase):
    """Testes para validação do formulário de Inlow (InflowForm)"""

    def setUp(self):
        """Configuração inicial para criação de uma entrada."""
        self.brand = Brand.objects.create(name='Microsoft')
        self.category = Category.objects.create(name='Mouse')
        self.product = Product.objects.create(
            title='Mouse Sem Fio',
            brand=self.brand,
            category=self.category,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        self.supplier = Supplier.objects.create(name='Ivan')

    def test_inflow_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = InflowForm(
            data={
                'supplier': self.supplier,
                'product': self.product,
                'quantity': 10,
            }
        )
        self.assertTrue(form.is_valid())

    def test_inflow_form_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando o
        campo 'product' não é preenchido.
        """
        form = InflowForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('product', form.errors)

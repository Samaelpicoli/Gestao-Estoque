from django.db.models.signals import post_save
from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from outflows.forms import OutflowForm
from products.models import Product
from suppliers.models import Supplier


class TestsFormsOutflow(TestCase):
    """Testes para validação do formulário de Outflow (OutflowForm)"""

    def setUp(self):
        """Configuração inicial para criação de uma saída."""
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
        Inflow.objects.create(
            supplier=self.supplier,
            product=self.product,
            quantity=10,
        )

    def test_outflow_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = OutflowForm(
            data={
                'product': self.product,
                'quantity': 3,
            }
        )
        self.assertTrue(form.is_valid())

    def test_outflow_form_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando o
        campo 'product' não é preenchido.
        """
        form = OutflowForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('product', form.errors)

    def test_outflow_form_qtd_maior_que_estoque_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando a quantidade é maior
        do que a que está no estoque.
        """
        form = OutflowForm(
            data={
                'product': self.product.id,
                'quantity': 12,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def tearDown(self):
        """Limpa os signals após os testes"""
        post_save.receivers = []

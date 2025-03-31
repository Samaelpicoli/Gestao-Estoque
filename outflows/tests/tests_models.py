from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from products.models import Product
from suppliers.models import Supplier


class TestsModelsOutflow(TestCase):
    """
    Testes para o modelo Outflow.
    """

    def setUp(self):
        """
        Configuração inicial dos objetos necessários para os testes.
        """
        brand = Brand.objects.create(name='Microsoft')
        category = Category.objects.create(name='Mouse')
        product = Product.objects.create(
            title='Mouse Sem Fio',
            brand=brand,
            category=category,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        supplier = Supplier.objects.create(name='Ivan')
        Inflow.objects.create(
            supplier=supplier,
            product=product,
            quantity=10,
        )
        self.outflow = Outflow.objects.create(
            product=product,
            quantity=5,
        )

    def test_str_de_outflow_deve_retornar_nome_do_produto(self):
        """
        Testa se o método __str__ do modelo Outflow retorna
        corretamente o nome do produto associado à saída.
        """
        esperado = 'Mouse Sem Fio'
        resultado = str(self.outflow)
        self.assertEqual(esperado, resultado)

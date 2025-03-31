from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from products.models import Product
from suppliers.models import Supplier


class TestsModelsInflow(TestCase):
    """
    Testes para o modelo Inflow.
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
        self.inflow = Inflow.objects.create(
            supplier=supplier,
            product=product,
            quantity=10,
        )

    def test_str_de_inflow_deve_retornar_seu_titulo(self):
        """
        Testa se o método __str__ do modelo Inflow
        retorna corretamente o nome do produto associado à entrada.
        """
        esperado = 'Mouse Sem Fio'
        resultado = str(self.inflow)
        self.assertEqual(esperado, resultado)

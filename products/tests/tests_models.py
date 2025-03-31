from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from products.models import Product


class TestsModelsProduct(TestCase):
    """
    Testes para o modelo Product.
    """

    def setUp(self):
        """
        Configuração inicial dos objetos necessários para os testes.
        """
        self.product = Product.objects.create(
            title='Mouse Sem Fio',
            brand=Brand.objects.create(name='Microsoft'),
            category=Category.objects.create(name='Mouse'),
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )

    def test_str_de_product_deve_retornar_seu_titulo(self):
        """
        Testa se o método __str__ retorna corretamente o título do produto.
        """
        esperado = 'Mouse Sem Fio'
        resultado = str(self.product)
        self.assertEqual(esperado, resultado)

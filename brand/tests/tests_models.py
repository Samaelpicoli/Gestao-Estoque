from django.test import TestCase

from brand.models import Brand


class TestsModelsBrand(TestCase):
    """Testes unitários para o modelo Brand."""

    def setUp(self):
        """
        Configuração inicial para os testes.

        Cria uma instância de Brand para ser usada nos testes.
        """
        self.brand = Brand.objects.create(name='Lenovo')

    def test_str_de_brand_deve_retornar_seu_nome(self):
        """Testa se o método __str__ retorna corretamente o nome da marca."""
        esperado = 'Lenovo'
        resultado = str(self.brand)
        self.assertEqual(esperado, resultado)

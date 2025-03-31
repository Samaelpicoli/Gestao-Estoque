from django.test import TestCase

from categories.models import Category


class TestsModelsCategory(TestCase):
    """Testes unitários para o modelo Category."""

    def setUp(self):
        """Configuração inicial para os testes.

        Cria uma instância de Category para ser usada nos testes.
        """
        self.category = Category.objects.create(name='Mouse')

    def test_str_de_category_deve_retornar_seu_nome(self):
        """
        Testa se o método __str__ retorna corretamente o nome da categoria.
        """
        esperado = 'Mouse'
        resultado = str(self.category)
        self.assertEqual(esperado, resultado)

from django.test import TestCase

from categories.forms import CategoryForm
from categories.models import Category


class TestsFormsCategory(TestCase):
    """Testes para validação do formulário de Category (CategoryForm)"""

    def setUp(self):
        """Configuração inicial para criação de uma categoria."""
        self.category = Category.objects.create(name='Mouse')

    def test_category_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = CategoryForm(
            data={'name': 'Teclados', 'description': 'Para notebooks'}
        )
        self.assertTrue(form.is_valid())

    def test_category_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando o
        campo 'name' não é preenchido.
        """
        form = CategoryForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

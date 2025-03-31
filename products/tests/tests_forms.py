from django.test import TestCase

from brand.models import Brand
from categories.models import Category
from products.forms import ProductForm


class TestsFormsProduct(TestCase):
    """Testes para validação do formulário de Product (ProductForm)"""

    def setUp(self):
        """Configuração inicial para criação de um produto."""
        self.brand = Brand.objects.create(name='Microsoft')
        self.category = Category.objects.create(name='Mouse')

    def test_product_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = ProductForm(
            data={
                'title': 'Mouse sem Fio',
                'category': self.category,
                'brand': self.brand,
                'serie_number': 3818012,
                'cost_price': 70.90,
                'selling_price': 111.99,
            }
        )
        self.assertTrue(form.is_valid())

    def test_product_form_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando os
        campos não são preenchido.
        """
        form = ProductForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

from django.test import TestCase

from brand.forms import BrandForm
from brand.models import Brand


class TestsFormsBrand(TestCase):
    """Testes para validação do formulário de Brand (BrandForm)"""

    def setUp(self):
        """Configuração inicial para criação de uma marca."""
        self.brand = Brand.objects.create(name='Dell')

    def test_brand_form_retorna_valido(self):
        """
        Testa se o formulário é válido quando todos os campos
        obrigatórios são preenchidos corretamente.
        """
        form = BrandForm(
            data={'name': 'LG', 'description': 'Marca de Monitores'}
        )
        self.assertTrue(form.is_valid())

    def test_brand_form_retorna_invalido(self):
        """
        Testa se o formulário retorna inválido quando o
        campo 'name' não é preenchido.
        """
        form = BrandForm(data={'description': 'TESTE'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

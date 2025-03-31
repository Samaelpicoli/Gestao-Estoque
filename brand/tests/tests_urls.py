from django.test import TestCase
from django.urls import resolve, reverse

from brand import views


class TestsUrlsBrand(TestCase):
    """Teste das URLS de Brand."""

    def test_url_brand_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de marcas está correta.

        Este teste verifica se a URL associada à view de listagem de marcas
        corresponde ao caminho esperado. O resultado deve ser a URL
        '/brands/list/'.
        """
        esperado = '/brands/list/'
        resultado = reverse('brand_list')
        self.assertEqual(esperado, resultado)

    def test_url_brand_list_retorna_a_view_brand_list(self):
        """
        Testa se a URL de Listagem de marcas retorna a view correta
        (BrandListView).

        Este teste verifica se, ao resolver a URL da lista de marcas, a
        view retornada é a `BrandListView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.BrandListView
        resultado = resolve(reverse('brand_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_brand_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de marca está correta.

        Este teste verifica se a URL associada à view de cadastro de marcas
        corresponde ao caminho esperado. O resultado deve ser a URL
        '/brands/create/'.
        """
        esperado = '/brands/create/'
        resultado = reverse('brand_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_brand_list_retorna_a_view_create_brand(self):
        """
        Testa se a URL de cadastro de marca retorna a view correta
        (BrandCreateView).

        Este teste verifica se, ao resolver a URL de cadastro de marcas, a
        view retornada é a `BrandCreateView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.BrandCreateView
        resultado = resolve(reverse('brand_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_brand_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de marca está correta.

        Este teste verifica se a URL associada à view de detalhes de marcas
        corresponde ao caminho esperado para um ID específico (neste caso, 1).
        O resultado deve ser a URL '/brands/1/detail/'.
        """
        esperado = '/brands/1/detail/'
        resultado = reverse('brand_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_brand_detail_retorna_a_view_detail_brand(self):
        """
        Testa se a URL de detalhes retorna a view correta (BrandDetailView).

        Este teste verifica se, ao resolver a URL de detalhes de uma marca,
        a view retornada é a `BrandDetailView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.BrandDetailView
        resultado = resolve(reverse('brand_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_brand_update_possui_a_url_correta(self):
        """
        Testa se a URL para a página de atualização de marca está correta.

        Este teste verifica se a URL associada à view de atualização de marcas
        corresponde ao caminho esperado para um ID específico (neste caso, 1).
        O resultado deve ser a URL '/brands/1/update/'.
        """
        esperado = '/brands/1/update/'
        resultado = reverse('brand_update', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_brand_update_retorna_a_view_update_brand(self):
        """
        Testa se a URL de atualização de marca retorna a view correta
        (BrandUpdateView).

        Este teste verifica se, ao resolver a URL de atualização de uma marca,
        a view retornada é a `BrandUpdateView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.BrandUpdateView
        resultado = resolve(reverse('brand_update', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_brand_delete_possui_a_url_correta(self):
        """
        Testa se a URL para a página de exclusão de marca está correta.

        Este teste verifica se a URL associada à view de exclusão de marcas
        corresponde ao caminho esperado para um ID específico (neste caso, 1).
        O resultado deve ser a URL '/brands/1/delete/'.
        """
        esperado = '/brands/1/delete/'
        resultado = reverse('brand_delete', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_brand_delete_retorna_a_view_delete_brand(self):
        """
        Testa se a URL de exclusão de marca retorna a view correta
        (BrandDeleteView).

        Este teste verifica se, ao resolver a URL de exclusão de uma marca,
        a view retornada é a `BrandDeleteView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.BrandDeleteView
        resultado = resolve(reverse('brand_delete', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

from django.test import TestCase
from django.urls import resolve, reverse

from products import views


class TestsUrlsProduct(TestCase):
    def test_url_product_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de produtos está correta.
        """
        esperado = '/products/list/'
        resultado = reverse('product_list')
        self.assertEqual(esperado, resultado)

    def test_url_product_list_retorna_a_view_product_list(self):
        """
        Testa se a URL de Listagem de produtos retorna
        a view correta (ProductListView).
        """
        esperado = views.ProductListView
        resultado = resolve(reverse('product_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_product_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de produto está correta.
        """
        esperado = '/products/create/'
        resultado = reverse('product_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_product_list_retorna_a_view_create_product(self):
        """
        Testa se a URL de cadastro de produto retorna
        a view correta (ProductCreateView).
        """
        esperado = views.ProductCreateView
        resultado = resolve(reverse('product_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_product_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de product está correta.
        """
        esperado = '/products/1/detail/'
        resultado = reverse('product_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_product_detail_retorna_a_view_detail_product(self):
        """
        Testa se a URL de detalhes retorna a view correta (ProductDetailView).
        """
        esperado = views.ProductDetailView
        resultado = resolve(reverse('product_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_product_update_possui_a_url_correta(self):
        """
        Testa se a URL para a página de atualização de produto está correta.
        """
        esperado = '/products/1/update/'
        resultado = reverse('product_update', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_product_update_retorna_a_view_update_product(self):
        """
        Testa se a URL de atualização de produto retorna
        a view correta (ProductUpdateView).
        """
        esperado = views.ProductUpdateView
        resultado = resolve(reverse('product_update', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_product_delete_possui_a_url_correta(self):
        """Testa se a URL para a página de exclusão de produto está correta."""
        esperado = '/products/1/delete/'
        resultado = reverse('product_delete', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_product_delete_retorna_a_view_delete_product(self):
        """
        Testa se a URL de exclusão de produto retorna a view
        correta (ProductDeleteView).
        """
        esperado = views.ProductDeleteView
        resultado = resolve(reverse('product_delete', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

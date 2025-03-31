from django.test import TestCase
from django.urls import resolve, reverse

from categories import views


class TestsUrlsCategory(TestCase):
    """Teste das URLS de Categoria."""

    def test_url_category_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de categorias está correta.
        """
        esperado = '/categories/list/'
        resultado = reverse('category_list')
        self.assertEqual(esperado, resultado)

    def test_url_category_list_retorna_a_view_category_list(self):
        """
        Testa se a URL de Listagem de categorias retorna
        a view correta (CategoryListView).
        """
        esperado = views.CategoryListView
        resultado = resolve(reverse('category_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_category_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de categoria está correta.
        """
        esperado = '/categories/create/'
        resultado = reverse('category_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_category_list_retorna_a_view_create_category(self):
        """
        Testa se a URL de cadastro de categoria retorna
        a view correta (CategoryCreateView).
        """
        esperado = views.CategoryCreateView
        resultado = resolve(reverse('category_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_category_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de categorias está correta.
        """
        esperado = '/categories/1/detail/'
        resultado = reverse('category_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_category_detail_retorna_a_view_detail_category(self):
        """
        Testa se a URL de detalhes retorna a view correta (CategoryDetailView).
        """
        esperado = views.CategoryDetailView
        resultado = resolve(reverse('category_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_category_update_possui_a_url_correta(self):
        """
        Testa se a URL para a página de atualização de categoria está correta.
        """
        esperado = '/categories/1/update/'
        resultado = reverse('category_update', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_category_update_retorna_a_view_update_category(self):
        """
        Testa se a URL de atualização de categoria retorna
        a view correta (CategoryUpdateView).
        """
        esperado = views.CategoryUpdateView
        resultado = resolve(reverse('category_update', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_category_delete_possui_a_url_correta(self):
        """
        Testa se a URL para a página de exclusão de categoria está correta.
        """
        esperado = '/categories/1/delete/'
        resultado = reverse('category_delete', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_category_delete_retorna_a_view_delete_category(self):
        """
        Testa se a URL de exclusão de categoria retorna a view
        correta (CategoryDeleteView).
        """
        esperado = views.CategoryDeleteView
        resultado = resolve(reverse('category_delete', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

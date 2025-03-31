from django.test import TestCase
from django.urls import resolve, reverse

from outflows import views


class TestsUrlsOutflow(TestCase):
    def test_url_outflow_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de saídas está correta.
        """
        esperado = '/outflows/list/'
        resultado = reverse('outflow_list')
        self.assertEqual(esperado, resultado)

    def test_url_outflow_list_retorna_a_view_outflow_list(self):
        """
        Testa se a URL de Listagem de saídas retorna
        a view correta (OutflowListView).
        """
        esperado = views.OutflowListView
        resultado = resolve(reverse('outflow_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_outflow_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de saída está correta.
        """
        esperado = '/outflows/create/'
        resultado = reverse('outflow_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_outflow_list_retorna_a_view_create_outflow(self):
        """
        Testa se a URL de cadastro de saída retorna
        a view correta (OutflowCreateView).
        """
        esperado = views.OutflowCreateView
        resultado = resolve(reverse('outflow_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_outflow_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de outflow está correta.
        """
        esperado = '/outflows/1/detail/'
        resultado = reverse('outflow_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_outflow_detail_retorna_a_view_detail_outflow(self):
        """
        Testa se a URL de detalhes retorna a view correta (OutflowDetailView).
        """
        esperado = views.OutflowDetailView
        resultado = resolve(reverse('outflow_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

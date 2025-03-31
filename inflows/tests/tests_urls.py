from django.test import TestCase
from django.urls import resolve, reverse

from inflows import views


class TestsUrlsInflow(TestCase):
    """Testes das URLS de Entradas (Inflows)."""

    def test_url_inflow_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de entradas está correta.
        """
        esperado = '/inflows/list/'
        resultado = reverse('inflow_list')
        self.assertEqual(esperado, resultado)

    def test_url_inflow_list_retorna_a_view_inflow_list(self):
        """
        Testa se a URL de Listagem de entradas retorna
        a view correta (InflowListView).
        """
        esperado = views.InflowListView
        resultado = resolve(reverse('inflow_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_inflow_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de entrada está correta.
        """
        esperado = '/inflows/create/'
        resultado = reverse('inflow_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_inflow_list_retorna_a_view_create_inflow(self):
        """
        Testa se a URL de cadastro de entrada retorna
        a view correta (InflowCreateView).
        """
        esperado = views.InflowCreateView
        resultado = resolve(reverse('inflow_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_inflow_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de inflow está correta.
        """
        esperado = '/inflows/1/detail/'
        resultado = reverse('inflow_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_inflow_detail_retorna_a_view_detail_inflow(self):
        """
        Testa se a URL de detalhes retorna a view correta (InflowDetailView).
        """
        esperado = views.InflowDetailView
        resultado = resolve(reverse('inflow_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

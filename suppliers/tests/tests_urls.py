from django.test import TestCase
from django.urls import resolve, reverse

from suppliers import views


class TestsUrlsSupplier(TestCase):
    def test_url_supplier_list_possui_a_url_correta(self):
        """
        Testa se a URL para a página de listagem de fornecedores está correta.
        """
        esperado = '/suppliers/list/'
        resultado = reverse('supplier_list')
        self.assertEqual(esperado, resultado)

    def test_url_supplier_list_retorna_a_view_supplier_list(self):
        """
        Testa se a URL de Listagem de fornecedores retorna
        a view correta (SupplierListView).
        """
        esperado = views.SupplierListView
        resultado = resolve(reverse('supplier_list'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_new_supplier_possui_a_url_correta(self):
        """
        Testa se a URL para a página de cadastro de fornecedor está correta.
        """
        esperado = '/suppliers/create/'
        resultado = reverse('supplier_create')
        self.assertEqual(esperado, resultado)

    def test_url_new_supplier_list_retorna_a_view_create_supplier(self):
        """
        Testa se a URL de cadastro de fornecedores retorna
        a view correta (SupplierCreateView).
        """
        esperado = views.SupplierCreateView
        resultado = resolve(reverse('supplier_create'))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_supplier_detail_possui_a_url_correta(self):
        """
        Testa se a URL para a página de detalhes de fornecedores está correta.
        """
        esperado = '/suppliers/1/detail/'
        resultado = reverse('supplier_detail', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_supplier_detail_retorna_a_view_detail_supplier(self):
        """
        Testa se a URL de detalhes retorna a view correta (SupplierDetailView).
        """
        esperado = views.SupplierDetailView
        resultado = resolve(reverse('supplier_detail', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_supplier_update_possui_a_url_correta(self):
        """
        Testa se a URL para a página de atualização
        de fornecedores está correta.
        """
        esperado = '/suppliers/1/update/'
        resultado = reverse('supplier_update', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_supplier_update_retorna_a_view_update_supplier(self):
        """
        Testa se a URL de atualização de fornecedor retorna
        a view correta (SupplierUpdateView).
        """
        esperado = views.SupplierUpdateView
        resultado = resolve(reverse('supplier_update', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

    def test_url_supplier_delete_possui_a_url_correta(self):
        """
        Testa se a URL para a página de exclusão de fornecedor está correta.
        """
        esperado = '/suppliers/1/delete/'
        resultado = reverse('supplier_delete', kwargs={'pk': 1})
        self.assertEqual(esperado, resultado)

    def test_url_supplier_delete_retorna_a_view_delete_supplier(self):
        """
        Testa se a URL de exclusão de fornecedor retorna a view
        correta (SupplierDeleteView).
        """
        esperado = views.SupplierDeleteView
        resultado = resolve(reverse('supplier_delete', kwargs={'pk': 1}))
        self.assertIs(esperado, resultado.func.view_class)

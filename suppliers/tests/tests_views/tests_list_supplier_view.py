from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from suppliers.models import Supplier


class TestsListSupplierView(TestCase):
    """Testes para a View de Listagem de Fornecedores."""

    def setUp(self):
        """
        Configura o ambiente de teste com a criação de 2 fornecedores.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_supplier')
        )
        self.client.login(username='testuser', password='12345')
        self.microsoft = Supplier.objects.create(name='Microsoft')
        self.apple = Supplier.objects.create(name='Apple')

    def test_list_view_retorna_status_code_200(self):
        """
        Testa se a visualização da lista de fornecedores retorna
        um código de status 200 (OK).
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('supplier_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def test_list_view_template_utilizado_retorna_supplier_list_html(self):
        """
        Testa se a visualização da lista de fornecedores utiliza o
        template correto ('supplier_list.html').
        """
        esperado = 'supplier_list.html'
        response = self.client.get(reverse('supplier_list'))
        self.assertTemplateUsed(response, esperado)

    def test_list_view_retorna_nenhum_fornecedor_encontrado(self):
        """
        Testa se, quando não há fornecedores no banco de dados, a quantidade
        de fornecedores é 0.
        """
        Supplier.objects.all().delete()
        esperado = 0
        response = self.client.get(reverse('supplier_list'))
        self.assertEqual(len(response.context['suppliers']), esperado)

    def test_list_view_retorna_context_com_filtro_no_search(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas as fornecedores
        que correspondem ao termo de pesquisa devem ser retornados.
        """
        response = self.client.get(
            reverse('supplier_list'), {'name': 'Teclado'}
        )
        self.assertContains(response, 'Teclado')
        self.assertNotContains(response, 'Mouse')

    def test_list_view_retorna_context_e_quantidade_de_itens(self):
        """
        Testa se o contexto da view contém a lista de fornecedores
        e verifica a quantidade de fornecedores retornados.
        """
        response = self.client.get(reverse('supplier_list'))
        chave_esperada_no_context = 'suppliers'
        self.assertIn(chave_esperada_no_context, response.context)

        esperado_quantidade_itens = 2

        self.assertEqual(
            len(response.context['suppliers']), esperado_quantidade_itens
        )

    def test_list_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de listagem de fornecedor.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('supplier_list'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de listagem de fornecedores.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('supplier_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def tearDown(self):
        """Limpa os dados criados no banco de dados após cada teste."""
        Supplier.objects.all().delete()

from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from categories.models import Category


class TestsListCategoryView(TestCase):
    """Testes para a View de Listagem de Caregorias."""

    def setUp(self):
        """
        Configura o ambiente de teste para a View de Listagem de Categorias.

        Este método é chamado antes da execução de cada método de teste.
        Ele cria um usuário de teste com permissões adequadas para visualizar
        categorias e faz o login desse usuário. Também cria duas instâncias
        do modelo Category para serem utilizadas nos testes.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_category')
        )
        self.client.login(username='testuser', password='12345')
        self.teclado = Category.objects.create(name='Teclado')
        self.mouse = Category.objects.create(name='Mouse')

    def test_list_view_retorna_status_code_200(self):
        """
        Testa se a visualização da lista de categorias retorna
        um código de status 200 (OK).
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('category_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def test_list_view_template_utilizado_retorna_category_list_html(self):
        """
        Testa se a visualização da lista de categorias utiliza o
        template correto ('category_list.html').
        """
        esperado = 'category_list.html'
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, esperado)

    def test_list_view_retorna_nenhuma_categoria_encontrado(self):
        """
        Testa se, quando não há categorias no banco de dados, a quantidade
        de categorias é 0.
        """
        Category.objects.all().delete()
        esperado = 0
        response = self.client.get(reverse('category_list'))
        self.assertEqual(len(response.context['categories']), esperado)

    def test_list_view_retorna_context_com_filtro_no_search(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas as categorias
        que correspondem ao termo de pesquisa devem ser retornados.
        """
        response = self.client.get(
            reverse('category_list'), {'name': 'Teclado'}
        )
        self.assertContains(response, 'Teclado')
        self.assertNotContains(response, 'Mouse')

    def test_list_view_retorna_context_e_quantidade_de_itens(self):
        """
        Testa se o contexto da view contém a lista de categorias
        e verifica a quantidade de categorias retornados.
        """
        response = self.client.get(reverse('category_list'))
        chave_esperada_no_context = 'categories'
        self.assertIn(chave_esperada_no_context, response.context)

        esperado_quantidade_itens = 2

        self.assertEqual(
            len(response.context['categories']), esperado_quantidade_itens
        )

    def test_list_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de criação de uma categoria.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('category_list'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de listagem de categorias.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('category_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def tearDown(self):
        """Limpa os dados criados no banco de dados após cada teste."""
        Category.objects.all().delete()

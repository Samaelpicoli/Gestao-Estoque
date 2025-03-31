from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from categories.models import Category


class TestsDeleteCategoryView(TestCase):
    """Testes para a View de Exclusão de Categorias."""

    def setUp(self):
        """
        Configura o ambiente de teste para a View de Exclusão de Categorias.

        Este método é chamado antes da execução de cada método de teste.
        Ele cria um usuário de teste com permissões adequadas para excluir
        categorias e faz o login desse usuário. Também cria uma instância
        do modelo Category para ser utilizado nos testes.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_category')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_category')
        )
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='Toyota')

    def test_delete_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Testa se a página de exclusão de uma categoria retorna o código de
        status 200 (OK) quando acessada por GET.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('category_delete', args=[self.category.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_template_utilizado_retorna_category_delete_html(self):
        """
        Testa se a página de exclusão utiliza o template
        correto ('category_delete.html').
        """
        esperado_nome_template = 'category_delete.html'
        response = self.client.get(
            reverse('category_delete', args=[self.category.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_delete_view_deleta_e_retorna_zero_objetos_e_redireciona(self):
        """
        Testa se a categoria é deletado corretamente após o envio do POST para
        a view de exclusão. Verifica também se o número de categorias no
        banco de dados é 0 após a exclusão e se ocorre um redirecionamento
        para a página de lista de categorias.
        """
        esperado_quantidade_categorias = 0
        response = self.client.post(
            reverse('category_delete', args=[self.category.id])
        )
        self.assertEqual(
            Category.objects.count(), esperado_quantidade_categorias
        )
        self.assertRedirects(response, reverse('category_list'))

    def test_delete_view_categoria_inexistente_retorna_not_found(self):
        """
        Testa se a tentativa de exclusão de uma categoria que não existe
        retorna o código de status 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('category_delete', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de exclusão de uma categoria.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('category_delete', args=[self.category.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de exclusão de categorias.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('category_delete', args=[self.category.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from categories.models import Category


class TestsUpdateCategoryView(TestCase):
    """Testa a view de atualização de uma categoria."""

    def setUp(self):
        """
        Configura o ambiente de teste para a View de Atualização de Categorias.

        Este método é chamado antes da execução de cada método de teste.
        Ele cria um usuário de teste com permissões adequadas para atualizar
        categorias e faz o login desse usuário. Também cria uma instância
        do modelo Category para ser utilizada nos testes.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_category')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_category')
        )
        self.client.login(username='testuser', password='12345')
        self.category = Category.objects.create(name='Mouse')

    def test_update_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Verifica se a página de atualização de categoria pode ser
        acessada e retorna status HTTP 200.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('category_update', args=[self.category.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_template_utilizado_retorna_category_update_html(self):
        """
        Verifica se a view de atualização de categoria
        utiliza o template correto.
        """
        esperado_nome_template = 'category_update.html'

        response = self.client.get(
            reverse('category_update', args=[self.category.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_update_view_atualiza_categoria_valido(self):
        """
        Testa se a atualização de uma categoria válida ocorre corretamente
        e redireciona para a página de detalhes.
        """
        self.client.post(
            reverse('category_update', args=[self.category.id]),
            data={'name': 'Mouse Sem Fio'},
        )
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Mouse Sem Fio')

    def test_update_view_categoria_inexistente_retorna_not_found(self):
        """
        Verifica se a tentativa de atualizar um categoria
        inexistente retorna um status HTTP 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('category_update', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de atualização de uma categoria.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('category_update', args=[self.category.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de atualização de categorias.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('category_update', args=[self.category.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

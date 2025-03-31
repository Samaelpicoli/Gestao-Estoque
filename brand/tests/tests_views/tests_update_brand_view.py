from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand


class TestsUpdateBrandView(TestCase):
    """Testa a view de atualização de uma marca."""

    def setUp(self):
        """
        Configura o ambiente de teste para a View de Atualização de Marcas.

        Este método é chamado antes da execução de cada método de teste.
        Ele cria um usuário de teste com permissões adequadas para atualizar
        marcas e faz o login desse usuário. Também cria uma instância
        do modelo Brand para ser utilizada nos testes.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_brand')
        )
        self.client.login(username='testuser', password='12345')
        self.brand = Brand.objects.create(name='Samsumg')

    def test_update_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Verifica se a página de atualização de marca pode ser
        acessada e retorna status HTTP 200.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('brand_update', args=[self.brand.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_template_utilizado_retorna_brand_update_html(self):
        """
        Verifica se a view de atualização de marca utiliza o template correto.
        """
        esperado_nome_template = 'brand_update.html'

        response = self.client.get(
            reverse('brand_update', args=[self.brand.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_update_view_atualiza_marca_valido(self):
        """
        Testa se a atualização de uma marca válida ocorre corretamente
        e redireciona para a página de detalhes.
        """
        self.client.post(
            reverse('brand_update', args=[self.brand.id]),
            data={'name': 'Samsung'},
        )
        self.brand.refresh_from_db()
        self.assertEqual(self.brand.name, 'Samsung')

    def test_update_view_marca_inexistente_retorna_not_found(self):
        """
        Verifica se a tentativa de atualizar um marca
        inexistente retorna um status HTTP 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('brand_update', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de atualização de uma marca.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('brand_update', args=[self.brand.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de atualização de marcas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('brand_update', args=[self.brand.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

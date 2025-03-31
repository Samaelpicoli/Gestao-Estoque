from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand


class TestsDeleteBrandView(TestCase):
    """Testes para a View de Exclusão de Marcas."""

    def setUp(self):
        """
        Configura o ambiente de teste para a View de Exclusão de Marcas.

        Este método é chamado antes da execução de cada método de teste.
        Ele cria um usuário de teste com permissões adequadas para excluir
        marcas e faz o login desse usuário. Também cria uma instância
        do modelo Brand para ser utilizado nos testes.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_brand')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_brand')
        )
        self.client.login(username='testuser', password='12345')
        self.brand = Brand.objects.create(name='Toyota')

    def test_delete_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Testa se a página de exclusão de uma marca retorna o código de
        status 200 (OK) quando acessada por GET.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('brand_delete', args=[self.brand.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_template_utilizado_retorna_brand_delete_html(self):
        """
        Testa se a página de exclusão utiliza o template
        correto ('brand_delete.html').
        """
        esperado_nome_template = 'brand_delete.html'
        response = self.client.get(
            reverse('brand_delete', args=[self.brand.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_delete_view_deleta_marca_e_retorna_qtd_zero_e_redireciona(self):
        """
        Testa se a marca é deletado corretamente após o envio do POST para
        a view de exclusão. Verifica também se o número de marcas no
        banco de dados é 0 após a exclusão e se ocorre um redirecionamento
        para a página de lista de marcas.
        """
        esperado_quantidade_marcas = 0
        response = self.client.post(
            reverse('brand_delete', args=[self.brand.id])
        )
        self.assertEqual(Brand.objects.count(), esperado_quantidade_marcas)
        self.assertRedirects(response, reverse('brand_list'))

    def test_delete_view_marca_inexistente_retorna_not_found(self):
        """
        Testa se a tentativa de exclusão de uma marca que não existe
        retorna o código de status 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('brand_delete', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de exclusão de uma marca.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('brand_delete', args=[self.brand.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de exclusão de marcas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('brand_delete', args=[self.brand.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

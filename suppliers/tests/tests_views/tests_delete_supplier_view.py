from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from suppliers.models import Supplier


class TestsDeleteSupplierView(TestCase):
    """Testes para a View de Exclusão de Fornecedores."""

    def setUp(self):
        """
        Configura o ambiente de teste com um usuário, um fornecedor
        (Lenovo). Além disso,
        realiza o login do usuário para testes de exclusão.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_supplier')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_supplier')
        )
        self.client.login(username='testuser', password='12345')
        self.supplier = Supplier.objects.create(name='Toyota')

    def test_delete_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Testa se a página de exclusão de um fornecedor retorna o código de
        status 200 (OK) quando acessada por GET.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('supplier_delete', args=[self.supplier.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_template_utilizado_retorna_supplier_delete_html(self):
        """
        Testa se a página de exclusão utiliza o template
        correto ('supplier_delete.html').
        """
        esperado_nome_template = 'supplier_delete.html'
        response = self.client.get(
            reverse('supplier_delete', args=[self.supplier.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_delete_view_deleta_fornecedor_retorna_zero_objects_e_direciona(
        self,
    ):  # noqa: E501
        """
        Testa se o fornecedor é deletado corretamente após o envio do POST para
        a view de exclusão. Verifica também se o número de fornecedores no
        banco de dados é 0 após a exclusão e se ocorre um redirecionamento
        para a página de lista de fornecedores.
        """
        esperado_quantidade_fornecedores = 0
        response = self.client.post(
            reverse('supplier_delete', args=[self.supplier.id])
        )
        self.assertEqual(
            Supplier.objects.count(), esperado_quantidade_fornecedores
        )
        self.assertRedirects(response, reverse('supplier_list'))

    def test_delete_view_fornecedor_inexistente_retorna_not_found(self):
        """
        Testa se a tentativa de exclusão de uma fornecedor que não existe
        retorna o código de status 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('supplier_delete', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_delete_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de exclusão de um fornecedor.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('supplier_delete', args=[self.supplier.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de exclusão de fornecedores.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('supplier_delete', args=[self.supplier.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

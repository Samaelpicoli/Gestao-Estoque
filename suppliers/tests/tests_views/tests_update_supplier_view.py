from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from suppliers.models import Supplier


class TestsUpdateSupplierView(TestCase):
    """Testa a view de atualização de um fornecedor."""

    def setUp(self):
        """Configura os dados iniciais para os testes."""
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_supplier')
        )
        self.client.login(username='testuser', password='12345')
        self.supplier = Supplier.objects.create(name='Evolução')

    def test_update_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Verifica se a página de atualização de fornecedor pode ser
        acessada e retorna status HTTP 200.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('supplier_update', args=[self.supplier.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_template_utilizado_retorna_supplier_update_html(self):
        """
        Verifica se a view de atualização de fornecedor
        utiliza o template correto.
        """
        esperado_nome_template = 'supplier_update.html'

        response = self.client.get(
            reverse('supplier_update', args=[self.supplier.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_update_view_atualiza_fornecedor_valido(self):
        """
        Testa se a atualização de um fornecedor válida ocorre corretamente
        e redireciona para a página de detalhes.
        """
        self.client.post(
            reverse('supplier_update', args=[self.supplier.id]),
            data={'name': 'Evolução Agrícola'},
        )
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Evolução Agrícola')

    def test_update_view_fornecedor_inexistente_retorna_not_found(self):
        """
        Verifica se a tentativa de atualizar um fornecedor
        inexistente retorna um status HTTP 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('supplier_update', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de atualização de um fornecedor.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('supplier_update', args=[self.supplier.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de atualização de fornecedores.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('supplier_update', args=[self.supplier.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

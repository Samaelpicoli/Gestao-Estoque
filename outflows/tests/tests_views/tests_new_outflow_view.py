from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from products.models import Product
from suppliers.models import Supplier


class TestsNewOutflowView(TestCase):
    """
    Testes para a view de criação de uma saída na aplicação.
    Verifica se a página de criação está acessível, se o template
    correto é renderizado, se os dados são validados corretamente
    e se o redirecionamento ocorre conforme esperado.
    """

    def setUp(self):
        """
        Configura o ambiente de teste.
        Cria uma saída e um usuário para fazer login.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_outflow')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_outflow')
        )
        self.client.login(username='testuser', password='12345')
        self.brand = Brand.objects.create(name='Microsoft')
        self.category = Category.objects.create(name='Mouse')
        self.product = Product.objects.create(
            title='Mouse Sem Fio',
            brand=self.brand,
            category=self.category,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        self.supplier = Supplier.objects.create(name='Ivan')
        Inflow.objects.create(
            supplier=self.supplier,
            product=self.product,
            quantity=10,
        )

    def test_new_view_a_ser_acessado_retorna_status_code_200(self):
        """
        Testa se a página de criação de uma saída está acessível
        e retorna o status code 200.
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('outflow_create'))
        self.assertEqual(response.status_code, esperado)

    def test_new_view_template_utilizado_retorna_outflow_create_html(self):
        """
        Testa se o template correto ('outflow_create.html')
        é utilizado na página de criação de saída.
        """
        esperado = 'outflow_create.html'
        response = self.client.get(reverse('outflow_create'))
        self.assertTemplateUsed(response, esperado)

    def test_new_view_valido_cadastra_saida_e_retorna_qtd_saidas_e_redirecionamento(  # noqa: E501
        self,
    ):  # noqa: E501
        """
        Testa se, ao enviar um formulário válido, uma saída é cadastrada,
        a quantidade de saídas aumenta para 1 e ocorre o redirecionamento
        para a lista de saídas.
        """
        esperado_status_code = HTTPStatus.FOUND
        esperado_quantidade_saidas = 1
        esperado_redirect = 'outflow_list'

        response = self.client.post(
            reverse('outflow_create'),
            data={
                'product': self.product.id,
                'quantity': 10,
                'description': '',
            },
        )

        self.assertEqual(response.status_code, esperado_status_code)
        self.assertEqual(Outflow.objects.count(), esperado_quantidade_saidas)
        self.assertRedirects(response, reverse(esperado_redirect))

    def test_new_view_invalido_retorna_invalido_e_zero_saidas(self):
        """
        Testa se, ao enviar um formulário com dados inválidos (sem produto),
        o formulário é invalidado, nenhuma saída é criada e o template
        correto é renderizado.
        """
        esperado_status_code = HTTPStatus.OK
        esperado_template_utilizado = 'outflow_create.html'
        esperado_quantidade_saidas = 0

        response = self.client.post(
            reverse('outflow_create'),
            data={
                'product': '',
                'quantity': '',
            },
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTemplateUsed(response, esperado_template_utilizado)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Outflow.objects.count(), esperado_quantidade_saidas)

    def test_create_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de criação de uma saída.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('outflow_create'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de criação de saídas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('outflow_create'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

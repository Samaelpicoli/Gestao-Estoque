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


class TestsListOutflowView(TestCase):
    """Testes para a View de Listagem de Saídas."""

    def setUp(self):
        """Configuração inicial para criação de uma saída."""
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_outflow')
        )
        self.client.login(username='testuser', password='12345')
        brand = Brand.objects.create(name='Microsoft')
        category = Category.objects.create(name='Mouse')
        product_mouse = Product.objects.create(
            title='Mouse Sem Fio',
            brand=brand,
            category=category,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        product_keyboard = Product.objects.create(
            title='Teclado Sem Fio',
            brand=brand,
            category=category,
            serie_number='2198011',
            cost_price=99.00,
            selling_price=150.00,
            quantity=3,
        )
        supplier = Supplier.objects.create(name='Ivan')
        Inflow.objects.create(
            supplier=supplier,
            product=product_mouse,
            quantity=10,
        )
        Inflow.objects.create(
            supplier=supplier,
            product=product_keyboard,
            quantity=2,
        )
        self.outflow_mouse = Outflow.objects.create(
            product=product_mouse, quantity=4
        )
        self.outflow_keyboard = Outflow.objects.create(
            product=product_keyboard, quantity=1
        )

    def test_list_view_retorna_status_code_200(self):
        """
        Testa se a visualização da lista de saídas retorna
        um código de status 200 (OK).
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('outflow_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def test_list_view_template_utilizado_retorna_outflow_list_html(self):
        """
        Testa se a visualização da lista de saídas utiliza o
        template correto ('outflow_list.html').
        """
        esperado = 'outflow_list.html'
        response = self.client.get(reverse('outflow_list'))
        self.assertTemplateUsed(response, esperado)

    def test_list_view_retorna_nenhuma_saida_encontrada(self):
        """
        Testa se, quando não há saídas no banco de dados, a quantidade
        de saídas é 0.
        """
        Outflow.objects.all().delete()
        esperado = 0
        response = self.client.get(reverse('outflow_list'))
        self.assertEqual(len(response.context['outflows']), esperado)

    def test_list_view_retorna_context_com_filtro_no_search(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas as saídas
        que correspondem ao termo de pesquisa devem ser retornados.
        """
        response = self.client.get(
            reverse('outflow_list'), {'product': 'Mouse'}
        )
        self.assertContains(response, 'Mouse')
        self.assertNotContains(response, 'Teclado')

    def test_list_view_retorna_context_e_quantidade_de_itens(self):
        """
        Testa se o contexto da view contém a lista de saídas
        e verifica a quantidade de saídas retornadas.
        """
        response = self.client.get(reverse('outflow_list'))
        chave_esperada_no_context = 'outflows'
        self.assertIn(chave_esperada_no_context, response.context)

        esperado_quantidade_itens = 2

        self.assertEqual(
            len(response.context['outflows']), esperado_quantidade_itens
        )

    def test_list_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de listagem de saídas.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('outflow_list'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de listagem de saídas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('outflow_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

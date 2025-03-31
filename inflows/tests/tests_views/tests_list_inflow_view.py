from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from products.models import Product
from suppliers.models import Supplier


class TestsListInflowView(TestCase):
    """Testes para a View de Listagem de Entradas."""

    def setUp(self):
        """
        Configura o ambiente de teste antes da execução de cada
        método de teste.

        Este método é chamado antes de cada teste e realiza as seguintes ações:
        - Cria um usuário de teste com permissões para visualizar categorias.
        - Faz o login do usuário para que as requisições feitas
        durante os testes sejam autenticadas.
        - Cria uma marca chamada 'Microsoft'.
        - Cria uma categoria chamada 'Mouse'.
        - Cria dois produtos: 'Mouse Sem Fio' e 'Teclado Sem Fio',
        ambos associados a marca e categoria criadas.
        - Cria um fornecedor chamado 'Ivan'.
        - Cria duas entradas (inflows) associadas aos produtos e ao fornecedor.

        Attributes:
            user (User): O usuário de teste criado.
            inflow_mouse (Inflow): A entrada relacionada ao Mouse Sem Fio.
            inflow_key (Inflow): A entrada relacionada ao Teclado Sem Fio.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_inflow')
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
        product_key = Product.objects.create(
            title='Teclado Sem Fio',
            brand=brand,
            category=category,
            serie_number='2198011',
            cost_price=99.00,
            selling_price=150.00,
            quantity=3,
        )
        supplier = Supplier.objects.create(name='Ivan')
        self.inflow_mouse = Inflow.objects.create(
            supplier=supplier,
            product=product_mouse,
            quantity=10,
        )
        self.inflow_key = Inflow.objects.create(
            supplier=supplier,
            product=product_key,
            quantity=2,
        )

    def test_list_view_retorna_status_code_200(self):
        """
        Testa se a visualização da lista de entradas retorna
        um código de status 200 (OK).
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('inflow_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def test_list_view_template_utilizado_retorna_inflow_list_html(self):
        """
        Testa se a visualização da lista de entradas utiliza o
        template correto ('inflow_list.html').
        """
        esperado = 'inflow_list.html'
        response = self.client.get(reverse('inflow_list'))
        self.assertTemplateUsed(response, esperado)

    def test_list_view_retorna_nenhuma_entrada_encontrado(self):
        """
        Testa se, quando não há entradas no banco de dados, a quantidade
        de entradas é 0.
        """
        Inflow.objects.all().delete()
        esperado = 0
        response = self.client.get(reverse('inflow_list'))
        self.assertEqual(len(response.context['inflows']), esperado)

    def test_list_view_retorna_context_com_filtro_no_search(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas as entradas
        que correspondem ao termo de pesquisa devem ser retornados.
        """
        response = self.client.get(
            reverse('inflow_list'), {'product': 'Mouse'}
        )
        self.assertContains(response, 'Mouse')
        self.assertNotContains(response, 'Teclado')

    def test_list_view_retorna_context_e_quantidade_de_itens(self):
        """
        Testa se o contexto da view contém a lista de entradas
        e verifica a quantidade de entradas retornados.
        """
        response = self.client.get(reverse('inflow_list'))
        chave_esperada_no_context = 'inflows'
        self.assertIn(chave_esperada_no_context, response.context)

        esperado_quantidade_itens = 2

        self.assertEqual(
            len(response.context['inflows']), esperado_quantidade_itens
        )

    def test_list_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de listagem de entradas.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('inflow_list'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de listagem de entradas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('inflow_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

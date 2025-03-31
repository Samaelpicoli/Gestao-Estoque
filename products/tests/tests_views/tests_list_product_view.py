from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from products.models import Product


class TestsListProductView(TestCase):
    """Testes para a View de Listagem de Produtos."""

    def setUp(self):
        """
        Configura o ambiente de teste com a criação de 2 produtos.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_product')
        )
        self.client.login(username='testuser', password='12345')
        self.category_mouse = Category.objects.create(name='Mouse')
        self.category_keyboard = Category.objects.create(name='Teclado')

        self.brand_microsoft = Brand.objects.create(name='Microsoft')

        self.product_mouse = Product.objects.create(
            title='Mouse Sem Fio',
            brand=self.brand_microsoft,
            category=self.category_mouse,
            serie_number='83901321',
            cost_price=80.00,
            selling_price=120.00,
            quantity=10,
        )
        self.product_keyboard = Product.objects.create(
            title='Teclado Mecânico',
            brand=Brand.objects.create(name='Red Dragon'),
            category=self.category_keyboard,
            serie_number='199101901',
            cost_price=110.00,
            selling_price=185.00,
            quantity=7,
        )

    def test_list_view_retorna_status_code_200(self):
        """
        Testa se a visualização da lista de produtos retorna
        um código de status 200 (OK).
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('product_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def test_list_view_template_utilizado_retorna_product_list_html(self):
        """
        Testa se a visualização da lista de produtos utiliza o
        template correto ('product_list.html').
        """
        esperado = 'product_list.html'
        response = self.client.get(reverse('product_list'))
        self.assertTemplateUsed(response, esperado)

    def test_list_view_retorna_nenhum_produto_encontrado(self):
        """
        Testa se, quando não há produtos no banco de dados, a quantidade
        de produtos é 0.
        """
        Product.objects.all().delete()
        esperado = 0
        response = self.client.get(reverse('product_list'))
        self.assertEqual(len(response.context['products']), esperado)

    def test_list_view_retorna_context_com_filtro_no_title(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas os produtos
        que correspondem ao termo de pesquisa no título devem ser retornados.
        """
        response = self.client.get(reverse('product_list'), {'title': 'Mouse'})
        self.assertContains(response, 'Mouse')

    def test_list_view_retorna_context_com_filtro_no_serie_number(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas os produtos
        que correspondem ao termo de pesquisa no número de série
        devem ser retornados.
        """
        response = self.client.get(
            reverse('product_list'), {'serie_number': '199101901'}
        )
        self.assertContains(response, 'Teclado')

    def test_list_view_retorna_context_com_filtro_no_category(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas os produtos
        que pertencem à categoria especificada devem ser retornados.
        """
        response = self.client.get(
            reverse('product_list'), {'category': self.category_mouse.id}
        )
        self.assertContains(response, 'Mouse Sem Fio')
        self.assertNotContains(response, 'Teclado Mecânico')

    def test_list_view_retorna_context_com_filtro_no_brand(self):
        """
        Testa se o filtro de busca funciona corretamente.
        Quando o filtro de busca é aplicado, apenas os produtos
        que pertencem à marca especificada devem ser retornados.
        """
        response = self.client.get(
            reverse('product_list'), {'brand': self.brand_microsoft.id}
        )
        self.assertContains(response, 'Mouse Sem Fio')
        self.assertNotContains(response, 'Teclado Mecânico')

    def test_list_view_retorna_context_e_quantidade_de_itens(self):
        """
        Testa se o contexto da view contém a lista de produtos
        e verifica a quantidade de produtos retornados.
        """
        response = self.client.get(reverse('product_list'))
        chave_esperada_no_context = 'products'
        self.assertIn(chave_esperada_no_context, response.context)

        esperado_quantidade_itens = 2

        self.assertEqual(
            len(response.context['products']), esperado_quantidade_itens
        )

    def test_list_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de listagem de produtos.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('product_list'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de listagem de produtos.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('product_list'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

    def tearDown(self):
        """Limpa os dados criados no banco de dados após cada teste."""
        Product.objects.all().delete()

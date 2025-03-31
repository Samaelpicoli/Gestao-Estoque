from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from products.models import Product


class TestsUpdateProductView(TestCase):
    """Testa a view de atualização de um produto."""

    def setUp(self):
        """Configura os dados iniciais para os testes."""
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_product')
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

    def test_update_view_a_ser_acessada_retorna_status_code_200(self):
        """
        Verifica se a página de atualização de produto pode ser
        acessada e retorna status HTTP 200.
        """
        esperado_status_code = HTTPStatus.OK
        response = self.client.get(
            reverse('product_update', args=[self.product.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_template_utilizado_retorna_product_update_html(self):
        """
        Verifica se a view de atualização de produto utiliza o
        template correto.
        """
        esperado_nome_template = 'product_update.html'

        response = self.client.get(
            reverse('product_update', args=[self.product.id])
        )
        self.assertTemplateUsed(response, esperado_nome_template)

    def test_update_view_atualiza_produto_valido(self):
        """
        Testa se a atualização de um produto válido ocorre corretamente
        e redireciona para a página de detalhes.
        """
        self.client.post(
            reverse('product_update', args=[self.product.id]),
            data={
                'title': 'Mouse Com Fio',
                'brand': self.brand.id,
                'category': self.category.id,
                'serie_number': '31436912',
                'cost_price': 88.00,
                'selling_price': 130.00,
                'quantity': 20,
            },
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Mouse Com Fio')

    def test_update_view_produto_inexistente_retorna_not_found(self):
        """
        Verifica se a tentativa de atualizar um produto
        inexistente retorna um status HTTP 404 (Not Found).
        """
        esperado_status_code = HTTPStatus.NOT_FOUND
        response = self.client.post(reverse('product_update', args=[9999]))
        self.assertEqual(response.status_code, esperado_status_code)

    def test_update_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de atualização de um produto.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(
            reverse('product_update', args=[self.product.id])
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de atualização de produtos.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.post(
            reverse('product_update', args=[self.product.id])
        )
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

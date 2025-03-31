from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from products.models import Product


class TestsNewProductView(TestCase):
    """
    Testes para a view de criação de um produto na aplicação.
    Verifica se a página de criação está acessível, se o template
    correto é renderizado, se os dados são validados corretamente
    e se o redirecionamento ocorre conforme esperado.
    """

    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_product')
        )
        self.user.user_permissions.add(
            Permission.objects.get(codename='view_product')
        )
        self.client.login(username='testuser', password='12345')
        self.brand = Brand.objects.create(name='Microsoft')
        self.category = Category.objects.create(name='Mouse')

    def test_new_view_a_ser_acessado_retorna_status_code_200(self):
        """
        Testa se a página de criação de um produto está acessível
        e retorna o status code 200.
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, esperado)

    def test_new_view_template_utilizado_retorna_product_create_html(self):
        """
        Testa se o template correto ('product_create.html')
        é utilizado na página de criação de produto.
        """
        esperado = 'product_create.html'
        response = self.client.get(reverse('product_create'))
        self.assertTemplateUsed(response, esperado)

    def test_new_view_valido_cadastra_produto_e_retorna_qtd_produtos_e_redirecionamento(  # noqa: E501
        self,
    ):  # noqa: E501
        """
        Testa se, ao enviar um formulário válido, um produto é cadastrado,
        a quantidade de produtos aumenta para 1 e ocorre o redirecionamento
        para a lista de produtos.
        """
        esperado_status_code = HTTPStatus.FOUND
        esperado_quantidade_produtos = 1
        esperado_redirect = 'product_list'

        response = self.client.post(
            reverse('product_create'),
            data={
                'title': 'Mouse com Fio Longo',
                'brand': self.brand.id,
                'category': self.category.id,
                'serie_number': '9999191',
                'cost_price': 110,
                'selling_price': 152,
                'quantity': 15,
            },
        )

        self.assertEqual(response.status_code, esperado_status_code)
        self.assertEqual(Product.objects.count(), esperado_quantidade_produtos)
        self.assertRedirects(response, reverse(esperado_redirect))

    def test_new_view_invalido_retorna_invalido_e_zero_produtos(self):
        """
        Testa se, ao enviar um formulário com dados inválidos (sem nome),
        o formulário é invalidado, nenhum produto é criado e o template
        correto é renderizado.
        """
        esperado_status_code = HTTPStatus.OK
        esperado_template_utilizado = 'product_create.html'
        esperado_quantidade_produtos = 0

        response = self.client.post(
            reverse('product_create'),
            data={'title': ''},
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTemplateUsed(response, esperado_template_utilizado)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Product.objects.count(), esperado_quantidade_produtos)

    def test_create_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de criação de produtos.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('product_create'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de criação de produtos.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('product_create'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

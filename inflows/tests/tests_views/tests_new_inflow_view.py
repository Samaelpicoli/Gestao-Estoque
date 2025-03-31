from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from brand.models import Brand
from categories.models import Category
from inflows.models import Inflow
from products.models import Product
from suppliers.models import Supplier


class TestsNewInflowView(TestCase):
    """
    Testes para a view de criação de uma entrada na aplicação.
    Verifica se a página de criação está acessível, se o template
    correto é renderizado, se os dados são validados corretamente
    e se o redirecionamento ocorre conforme esperado.
    """

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
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_inflow')
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

    def test_new_view_a_ser_acessado_retorna_status_code_200(self):
        """
        Testa se a página de criação de uma entrada está acessível
        e retorna o status code 200.
        """
        esperado = HTTPStatus.OK
        response = self.client.get(reverse('inflow_create'))
        self.assertEqual(response.status_code, esperado)

    def test_new_view_template_utilizado_retorna_inflow_create_html(self):
        """
        Testa se o template correto ('inflow_create.html')
        é utilizado na página de criação de entrada.
        """
        esperado = 'inflow_create.html'
        response = self.client.get(reverse('inflow_create'))
        self.assertTemplateUsed(response, esperado)

    def test_new_view_valido_cadastra_entrada_e_retorna_qtd_entrada_e_redirecionamento(  # noqa: E501
        self,
    ):  # noqa: E501
        """
        Testa se, ao enviar um formulário válido, uma entrada é cadastrado,
        a quantidade de entradas aumenta para 1 e ocorre o redirecionamento
        para a lista de entradas.
        """
        esperado_status_code = HTTPStatus.FOUND
        esperado_quantidade_entradas = 1
        esperado_redirect = 'inflow_list'

        response = self.client.post(
            reverse('inflow_create'),
            data={
                'supplier': self.supplier.id,
                'product': self.product.id,
                'quantity': 10,
                'description': '',
            },
        )

        self.assertEqual(response.status_code, esperado_status_code)
        self.assertEqual(Inflow.objects.count(), esperado_quantidade_entradas)
        self.assertRedirects(response, reverse(esperado_redirect))

    def test_new_view_invalido_retorna_invalido_e_zero_entradas(self):
        """
        Testa se, ao enviar um formulário com dados inválidos (sem nome),
        o formulário é invalidado, nenhuma entrada é criado e o template
        correto é renderizado.
        """
        esperado_status_code = HTTPStatus.OK
        esperado_template_utilizado = 'inflow_create.html'
        esperado_quantidade_entradas = 0

        response = self.client.post(
            reverse('inflow_create'),
            data={
                'supplier': '',
                'product': self.product,
                'quantity': 10,
            },
        )
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTemplateUsed(response, esperado_template_utilizado)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Inflow.objects.count(), esperado_quantidade_entradas)

    def test_create_view_sem_login_retorna_redirecionameto_a_url_login(self):
        """
        Testa se um usuário não autenticado é redirecionado para a página de
        login quando tenta acessar a view de criação de uma entrada.
        """
        esperado_status_code = HTTPStatus.FOUND
        self.client.logout()
        response = self.client.post(reverse('inflow_create'))
        self.assertEqual(response.status_code, esperado_status_code)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_view_user_sem_permissao_retorna_bloqueado(self):
        """
        Testa se um usuário sem permissão recebe um erro 403 FORBIDDEN
        quando tenta acessar a view de criação de entradas.
        """

        User.objects.create_user(username='test2', password='12345')
        self.client.login(username='test2', password='12345')
        esperado = HTTPStatus.FORBIDDEN
        response = self.client.get(reverse('inflow_create'))
        resultado = response.status_code
        self.assertEqual(esperado, resultado)

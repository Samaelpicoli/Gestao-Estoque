from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountLoginViewTests(TestCase):
    """Classe de Testes para a View de Login."""

    def setUp(self):
        """Configura um usuário de teste para os métodos de teste."""
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_login_view_template_utilizado_retorna_login_html(self):
        """Teste se a página de login é renderizada corretamente."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_valido_retorna_redirecionamento(self):
        """Teste se o login bem-sucedido redireciona para a página inicial."""
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpassword'},
        )
        self.assertRedirects(response, reverse('home'))

    def test_login_view_invalido_retorna_erros(self):
        """Teste se um login inválido exibe uma mensagem de erro apropriada."""
        response = self.client.post(
            reverse('login'),
            {'username': 'wronguser', 'password': 'wrongpassword'},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Por favor')

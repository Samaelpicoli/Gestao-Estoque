from django.test import TestCase
from django.urls import resolve, reverse

from accounts import views


class TestsUrlsAccounts(TestCase):
    """Teste das URLS de Brand."""

    def test_url_login_possui_a_url_correta(self):
        """
        Testa se a URL para a página de login está correta.

        Este teste verifica se a URL associada à view de login
        corresponde ao caminho esperado. O resultado deve ser a URL
        '/login/'.
        """
        esperado = '/login/'
        resultado = reverse('login')
        self.assertEqual(esperado, resultado)

    def test_url_login_retorna_a_view_account_login_view(self):
        """
        Testa se a URL de Login retorna a view correta (AccountLoginView).

        Este teste verifica se, ao resolver a URL de login, a
        view retornada é a `AccountLoginView`, garantindo que a configuração
        de URLs está correta.
        """
        esperado = views.AccountLoginView
        resultado = resolve(reverse('login'))
        self.assertIs(esperado, resultado.func.view_class)

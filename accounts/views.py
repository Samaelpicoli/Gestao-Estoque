from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AccountLoginView(LoginView):
    """
    View personalizada para o login de usuários.

    Esta view estende a LoginView padrão do Django e personaliza
    o comportamento de exibição de erros e redirecionamento para
    usuários já autenticados.

    Attributes:
        template_name: O template a ser renderizado para o login.
        success_url: A URL para redirecionar após um login bem-sucedido.
    """

    template_name = 'login.html'
    success_url = reverse_lazy('home')

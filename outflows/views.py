from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from dashboards.metrics import get_sales_metrics
from outflows.forms import OutflowForm
from outflows.models import Outflow


class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar saídas.

    Esta view exibe uma lista paginada de saídas. Os usuários devem estar
    autenticados e ter permissão para visualizar saídas.

    Attributes:
        model: O modelo de dados a ser utilizado (Outflow).
        template_name: O template a ser renderizado para a lista de saídas.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de saídas a serem exibidas por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10
    permission_required = 'outflows.view_outflow'

    def get_queryset(self):
        """
        Obtém a lista de saídas, aplicando filtro pelo nome do produto,
        se fornecido.

        Returns:
            QuerySet: Lista de saídas filtradas pelo nome do produto
            (se fornecido).
        """
        queryset = super().get_queryset()
        product = self.request.GET.get('product')
        if product:
            queryset = queryset.filter(product__title__istartswith=product)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adiciona métricas de vendas ao contexto da lista de saídas.

        Este método estende o contexto padrão para incluir métricas de vendas,
        que podem ser utilizadas no template.

        Args:
            **kwargs: Argumentos adicionais passados para o método.

        Returns:
            dict: O contexto atualizado, incluindo as métricas de vendas.
        """
        context = super().get_context_data(**kwargs)
        context['sales_metrics'] = get_sales_metrics()
        return context


class OutflowCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """
    View para criar uma nova saída.

    Esta view permite que usuários autenticados e autorizados criem uma nova
    saída. Após a criação, o usuário é redirecionado para a lista de saídas.

    Attributes:
        model: O modelo de dados a ser utilizado (Outflow).
        template_name: O template a ser renderizado para a criação de saídas.
        form_class: O formulário a ser utilizado para a criação de saídas.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Outflow
    template_name = 'outflow_create.html'
    form_class = OutflowForm
    success_url = reverse_lazy('outflow_list')
    permission_required = 'outflows.add_outflow'


class OutflowDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    View para exibir os detalhes de uma saída.

    Esta view exibe as informações detalhadas de uma saída específica.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Outflow).
        template_name: O template a ser renderizado para os detalhes da saída.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Outflow
    template_name = 'outflow_detail.html'
    permission_required = 'outflows.view_outflow'

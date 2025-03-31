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

from inflows.forms import InflowForm
from inflows.models import Inflow


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar entradas.

    Esta view exibe uma lista paginada de entradas. Os usuários devem estar
    autenticados e ter permissão para visualizar entradas.

    Attributes:
        model: O modelo de dados a ser utilizado (Inflow).
        template_name: O template a ser renderizado para a lista de entradas.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de entradas a serem exibidas por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflows.view_inflow'

    def get_queryset(self):
        """
        Obtém a lista de entradas, aplicando filtro pelo nome caso fornecido.

        Returns:
            QuerySet: Lista de entradas filtradas pelo nome (se fornecido).
        """
        queryset = super().get_queryset()
        product = self.request.GET.get('product')
        if product:
            queryset = queryset.filter(product__title__istartswith=product)
        return queryset


class InflowCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """
    View para criar uma nova entrada.

    Esta view permite que usuários autenticados e autorizados criem uma nova
    entrada. Após a criação, o usuário é redirecionado
    para a lista de entradas.

    Attributes:
        model: O modelo de dados a ser utilizado (Inflow).
        template_name: O template a ser renderizado para a criação de entradas.
        form_class: O formulário a ser utilizado para a criação de entradas.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Inflow
    template_name = 'inflow_create.html'
    form_class = InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflows.add_inflow'


class InflowDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    View para exibir os detalhes de uma entrada.

    Esta view exibe as informações detalhadas de uma entrada específica.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Inflow).
        template_name: O template a ser renderizado para
        os detalhes da entrada.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Inflow
    template_name = 'inflow_detail.html'
    permission_required = 'inflows.view_inflow'

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from suppliers.forms import SupplierForm
from suppliers.models import Supplier


class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar fornecedores.

    Esta view exibe uma lista paginada de fornecedores. Os usuários devem
    estar autenticados e ter permissão para visualizar fornecedores. O
    usuário pode filtrar a lista de fornecedores pelo nome.

    Attributes:
        model: O modelo de dados a ser utilizado (Supplier).
        template_name: O template a ser renderizado para a
        lista de fornecedores.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de fornecedores a serem exibidos por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    permission_required = 'suppliers.view_supplier'

    def get_queryset(self):
        """
        Obtém a lista de fornecedores, aplicando filtro pelo nome,
        se fornecido.

        Retorna um QuerySet filtrado de acordo com o parâmetro de nome
        fornecido na requisição.

        Returns:
            QuerySet: Lista de fornecedores filtrados.
        """
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class SupplierCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """
    View para criar um novo fornecedor.

    Esta view permite que usuários autenticados e autorizados criem um novo
    fornecedor. Após a criação, o usuário é redirecionado para a lista de
    fornecedores.

    Attributes:
        model: O modelo de dados a ser utilizado (Supplier).
        template_name: O template a ser renderizado para
        a criação de fornecedores.
        form_class: O formulário a ser utilizado
        para a criação de fornecedores.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Supplier
    template_name = 'supplier_create.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.add_supplier'


class SupplierDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    View para exibir os detalhes de um fornecedor.

    Esta view exibe as informações detalhadas de um fornecedor específico.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Supplier).
        template_name: O template a ser renderizado para os
        detalhes do fornecedor.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Supplier
    template_name = 'supplier_detail.html'
    permission_required = 'suppliers.view_supplier'


class SupplierUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """
    View para atualizar um fornecedor existente.

    Esta view permite que usuários autenticados e autorizados atualizem as
    informações de um fornecedor existente. Após a atualização, o usuário é
    redirecionado para a lista de fornecedores.

    Attributes:
        model: O modelo de dados a ser utilizado (Supplier).
        template_name: O template a ser renderizado
        para a atualização do fornecedor.
        form_class: O formulário a ser utilizado
        para a atualização do fornecedor.
        success_url: URL para redirecionar após a atualização bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Supplier
    template_name = 'supplier_update.html'
    form_class = SupplierForm
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.change_supplier'


class SupplierDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """
    View para deletar um fornecedor.

    Esta view permite que usuários autenticados e autorizados deletam um
    fornecedor existente. Após a exclusão, o usuário é redirecionado para
    a lista de fornecedores.

    Attributes:
        model: O modelo de dados a ser utilizado (Supplier).
        template_name: O template a ser renderizado
        para a confirmação de exclusão.
        success_url: URL para redirecionar após a exclusão bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Supplier
    template_name = 'supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.delete_supplier'

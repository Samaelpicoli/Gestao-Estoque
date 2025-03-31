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

from categories.forms import CategoryForm
from categories.models import Category


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar categorias.

    Esta view exibe uma lista paginada de categorias. Os usuários devem estar
    autenticados e ter permissão para visualizar categorias.

    Attributes:
        model: O modelo de dados a ser utilizado (Category).
        template_name: O template a ser renderizado para a lista de categorias.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de categorias a serem exibidas por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    permission_required = 'categories.view_category'

    def get_queryset(self):
        """
        Obtém a lista de categorias, aplicando filtro pelo nome caso fornecido.

        Returns:
            QuerySet: Lista de categorias filtradas pelo nome (se fornecido).
        """
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class CategoryCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """
    View para criar uma nova categoria.

    Esta view permite que usuários autenticados e autorizados criem uma nova
    categoria. Após a criação, o usuário é redirecionado
    para a lista de categorias.

    Attributes:
        model: O modelo de dados a ser utilizado (Category).
        template_name: O template a ser renderizado para a
        criação de categorias.
        form_class: O formulário a ser utilizado para a criação de categorias.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.add_category'


class CategoryDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    View para exibir os detalhes de uma categoria.

    Esta view exibe as informações detalhadas de uma categoria específica.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Category).
        template_name: O template a ser renderizado para os
        detalhes da categoria.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Category
    template_name = 'category_detail.html'
    permission_required = 'categories.view_category'


class CategoryUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """
    View para atualizar uma categoria existente.

    Esta view permite que usuários autenticados e autorizados atualizem as
    informações de uma categoria. Após a atualização,
    o usuário é redirecionado para a lista de categorias.

    Attributes:
        model: O modelo de dados a ser utilizado (Category).
        template_name: O template a ser renderizado para a
        atualização da categoria.
        form_class: O formulário a ser utilizado para atualizar a categoria.
        success_url: URL para redirecionar após a atualização bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Category
    template_name = 'category_update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.change_category'


class CategoryDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """
    View para deletar uma categoria.

    Esta view permite que usuários autenticados e autorizados removam uma
    categoria existente. Após a exclusão, o usuário é redirecionado para a
    lista de categorias.

    Attributes:
        model: O modelo de dados a ser utilizado (Category).
        template_name: O template a ser renderizado para
        a confirmação de exclusão.
        success_url: URL para redirecionar após a exclusão bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.delete_category'

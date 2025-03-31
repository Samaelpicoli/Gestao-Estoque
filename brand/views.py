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

from brand.forms import BrandForm
from brand.models import Brand


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar marcas.

    Esta view exibe uma lista paginada de marcas. Os usuários devem estar
    autenticados e ter permissão para visualizar marcas.

    Attributes:
        model: O modelo de dados a ser utilizado (Brand).
        template_name: O template a ser renderizado para a lista de marcas.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de marcas a serem exibidas por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10
    permission_required = 'brand.view_brand'

    def get_queryset(self):
        """
        Obtém a lista de marcas, aplicando filtro pelo nome caso fornecido.

        Returns:
            QuerySet: Lista de marcas filtradas pelo nome (se fornecido).
        """
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class BrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View para criar uma nova marca.

    Esta view permite que usuários autenticados e autorizados criem uma nova
    marca. Após a criação, o usuário é redirecionado para a lista de marcas.

    Attributes:
        model: O modelo de dados a ser utilizado (Brand).
        template_name: O template a ser renderizado para a criação de marcas.
        form_class: O formulário a ser utilizado para a criação de marcas.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Brand
    template_name = 'brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brand.add_brand'


class BrandDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    View para exibir os detalhes de uma marca.

    Esta view exibe as informações detalhadas de uma marca específica.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Brand).
        template_name: O template a ser renderizado para os detalhes da marca.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Brand
    template_name = 'brand_detail.html'
    permission_required = 'brand.view_brand'


class BrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View para atualizar uma marca existente.

    Esta view permite que usuários autenticados e autorizados atualizem
    as informações de uma marca. Após a atualização, o usuário é redirecionado
    para a lista de marcas.

    Attributes:
        model: O modelo de dados a ser utilizado (Brand).
        template_name: O template a ser renderizado para
        a atualização da marca.
        form_class: O formulário a ser utilizado para atualizar a marca.
        success_url: URL para redirecionar após a atualização bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Brand
    template_name = 'brand_update.html'
    form_class = BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brand.change_brand'


class BrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    View para deletar uma marca.

    Esta view permite que usuários autenticados e autorizados removam
    uma marca existente. Após a exclusão, o usuário é redirecionado para
    a lista de marcas.

    Attributes:
        model: O modelo de dados a ser utilizado (Brand).
        template_name: O template a ser renderizado
        para a confirmação de exclusão.
        success_url: URL para redirecionar após a exclusão bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Brand
    template_name = 'brand_delete.html'
    success_url = reverse_lazy('brand_list')
    permission_required = 'brand.delete_brand'

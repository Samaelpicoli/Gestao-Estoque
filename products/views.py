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

from brand.models import Brand
from categories.models import Category
from dashboards.metrics import get_product_metrics
from products.forms import ProductForm
from products.models import Product


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar produtos.

    Esta view exibe uma lista paginada de produtos. Os usuários devem estar
    autenticados e ter permissão para visualizar produtos. O usuário pode
    filtrar a lista de produtos por título, número de série, categoria e marca.

    Attributes:
        model: O modelo de dados a ser utilizado (Product).
        template_name: O template a ser renderizado para a lista de produtos.
        context_object_name: O nome do contexto a ser utilizado no template.
        paginate_by: Número de produtos a serem exibidos por página.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    permission_required = 'products.view_product'

    def get_queryset(self):
        """
        Obtém a lista de produtos, aplicando filtros se fornecidos.

        Filtros disponíveis incluem título, número de série, categoria e
        marca. Retorna um QuerySet filtrado de acordo com os parâmetros
        fornecidos na requisição.

        Returns:
            QuerySet: Lista de produtos filtrados.
        """
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        serie_number = self.request.GET.get('serie_number')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')

        if serie_number:
            queryset = queryset.filter(serie_number__istartswith=serie_number)

        if title:
            queryset = queryset.filter(title__istartswith=title)

        if category:
            queryset = queryset.filter(category__id=category)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adiciona categorias, marcas e métricas de produtos ao contexto.

        Este método estende o contexto padrão para incluir listas de
        categorias e marcas, além das métricas de produtos, que podem ser
        utilizadas no template.

        Args:
            **kwargs: Argumentos adicionais passados para o método.

        Returns:
            dict: O contexto atualizado, incluindo categorias,
            marcas e métricas.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['product_metrics'] = get_product_metrics()
        return context


class ProductCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    """
    View para criar um novo produto.

    Esta view permite que usuários autenticados e autorizados criem um novo
    produto. Após a criação, o usuário é redirecionado
    para a lista de produtos.

    Attributes:
        model: O modelo de dados a ser utilizado (Product).
        template_name: O template a ser renderizado para a criação de produtos.
        form_class: O formulário a ser utilizado para a criação de produtos.
        success_url: URL para redirecionar após a criação bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'


class ProductDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    View para exibir os detalhes de um produto.

    Esta view exibe as informações detalhadas de um produto específico.
    Apenas usuários autenticados e autorizados podem acessar esta view.

    Attributes:
        model: O modelo de dados a ser utilizado (Product).
        template_name: O template a ser renderizado para os
        detalhes do produto.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Product
    template_name = 'product_detail.html'
    permission_required = 'products.view_product'


class ProductUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """
    View para atualizar um produto existente.

    Esta view permite que usuários autenticados e autorizados atualizem as
    informações de um produto existente. Após a atualização, o usuário é
    redirecionado para a lista de produtos.

    Attributes:
        model: O modelo de dados a ser utilizado (Product).
        template_name: O template a ser renderizado para
        a atualização do produto.
        form_class: O formulário a ser utilizado para a atualização do produto.
        success_url: URL para redirecionar após a atualização bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Product
    template_name = 'product_update.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.change_product'


class ProductDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """
    View para deletar um produto.

    Esta view permite que usuários autenticados e autorizados deletam um
    produto existente. Após a exclusão, o usuário é redirecionado para
    a lista de produtos.

    Attributes:
        model: O modelo de dados a ser utilizado (Product).
        template_name: O template a ser renderizado
        para a confirmação de exclusão.
        success_url: URL para redirecionar após a exclusão bem-sucedida.
        permission_required: Permissão necessária para acessar a view.
    """

    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'

from django.db import models

from brand.models import Brand
from categories.models import Category


class Product(models.Model):
    """
    Modelo que representa um produto no estoque.

    Attributes:
        title (str): Nome do produto.
        brand (Brand): Marca associada ao produto.
        category (Category): Categoria do produto.
        description (str, optional): Descrição do produto.
        serie_number (str, optional): Número de série do produto.
        cost_price (Decimal): Preço de custo do produto.
        selling_price (Decimal): Preço de venda do produto.
        quantity (int): Quantidade disponível em estoque.
        created_at (datetime): Data e hora de criação do registro.
        updated_at (datetime): Data e hora da última atualização do registro.
    """

    title = models.CharField(max_length=300)
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name='products'
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )
    description = models.TextField(null=True, blank=True)
    serie_number = models.CharField(max_length=200, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Retorna uma representação em string do título do produto."""
        return self.title

    class Meta:
        """
        Metadados para a configuração do modelo Product.

        Attributes:
            ordering (list): Define a ordenação padrão pelo campo 'title'.
        """

        ordering = ['title']

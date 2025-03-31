from django.db import models

from products.models import Product
from suppliers.models import Supplier


class Inflow(models.Model):
    """
    Modelo que representa a entrada de produtos no estoque.

    Attributes:
        supplier (Supplier): Fornecedor responsável pela entrada do produto.
        product (Product): Produto que está sendo adicionado ao estoque.
        quantity (int): Quantidade do produto adicionada.
        description (str, optional): Descrição opcional sobre a entrada
        do produto.
        created_at (datetime): Data e hora de criação do registro.
        updated_at (datetime): Data e hora da última atualização do registro.
    """

    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name='inflows'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='inflows'
    )
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Retorna o nome do produto associado à entrada no estoque.

        Returns:
            str: Nome do produto.
        """
        return str(self.product)

    class Meta:
        """
        Configurações do modelo no banco de dados.

        Attributes:
            ordering (list): Define a ordenação padrão pela data de criação,
            da mais recente para a mais antiga.
        """

        ordering = ['-created_at']

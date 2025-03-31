from django.db import models

from products.models import Product


class Outflow(models.Model):
    """
    Modelo que representa a saída de produtos do estoque.

    Attributes:
        product (Product): Produto que está sendo retirado do estoque.
        quantity (int): Quantidade do produto retirada.
        description (str, optional): Descrição opcional sobre a saída
        do produto.
        created_at (datetime): Data e hora de criação do registro.
        updated_at (datetime): Data e hora da última atualização
        do registro.
    """

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='outflows'
    )
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Retorna o nome do produto associado à saída do estoque.

        Returns:
            str: Nome do produto.
        """
        return str(self.product)

    class Meta:
        """
        Configurações do modelo no banco de dados.

        Attributes:
            ordering (list): Define a ordenação padrão pela data
            de criação, da mais recente para a mais antiga.
        """

        ordering = ['-created_at']

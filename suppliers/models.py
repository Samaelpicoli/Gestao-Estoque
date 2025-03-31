from django.db import models


class Supplier(models.Model):
    """
    Modelo representando um fornecedor de produtos.

    Attributes:
        name (CharField): Nome do fornecedor (único, máx. 100 caracteres).
        description (TextField): Descrição opcional do fornecedor.
        created_at (DateTimeField): Data e hora da criação do registro.
        updated_at (DateTimeField): Data e hora da última atualização
        do registro.

    Methods:
        __str__: Retorna o nome do fornecedor.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Retorna uma representação em string do fornecedor."""
        return self.name

    class Meta:
        """Metadados para a configuração do modelo Supplier.

        Attributes:
            ordering (list): Define a ordenação padrão pelo campo 'name'.
        """

        ordering = ['name']

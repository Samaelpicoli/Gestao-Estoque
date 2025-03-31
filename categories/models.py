from django.db import models


class Category(models.Model):
    """
    Modelo representando uma categoria de produtos.

    Attributes:
        name (CharField): Nome da categoria (único, máx. 100 caracteres).
        description (TextField): Descrição opcional da categoria.
        created_at (DateTimeField): Data e hora da criação do registro.
        updated_at (DateTimeField): Data e hora da última atualização
        do registro.

    Methods:
        __str__: Retorna o nome da categoria.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Retorna uma representação em string da categoria."""
        return self.name

    class Meta:
        """
        Metadados para a configuração do modelo Category.

        Attributes:
            ordering (list): Define a ordenação padrão pelo campo 'name'.
        """

        ordering = ['name']

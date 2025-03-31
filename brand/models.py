from django.db import models


class Brand(models.Model):
    """
    Modelo representando uma marca de produtos.

    Attributes:
        name (CharField): Nome da marca (único, máx. 100 caracteres).
        description (TextField): Descrição opcional da marca.
        created_at (DateTimeField): Data e hora da criação do registro.
        updated_at (DateTimeField): Data e hora da última atualização
        do registro.

    Methods:
        __str__: Retorna o nome da marca.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Retorna uma representação em string da marca."""
        return self.name

    class Meta:
        """
        Metadados para a configuração do modelo Brand.

        Attributes:
            ordering (list): Define a ordenação padrão pelo campo 'name'.
        """

        ordering = ['name']

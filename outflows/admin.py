from django.contrib import admin

from outflows.models import Outflow


class OutflowAdmin(admin.ModelAdmin):
    """
    Configuração do painel de administração para o modelo Outflow.

    Esta classe define a aparência e o comportamento do modelo Outflow no
    painel de administração do Django. Permite que os administradores
    visualizem e gerenciem saídas de forma eficiente.

    Attributes:
        list_display (tuple): Campos a serem exibidos na lista de saídas.
        search_fields (tuple): Campos nos quais é possível realizar buscas
        no painel de administração.
    """

    list_display = (
        'product',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = ('product__title',)


admin.site.register(Outflow, OutflowAdmin)

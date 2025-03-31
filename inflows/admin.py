from django.contrib import admin

from inflows.models import Inflow


class InflowAdmin(admin.ModelAdmin):
    """
    Configuração do painel de administração para o modelo Inflow.

    Esta classe define a aparência e o comportamento do modelo Inflow no
    painel de administração do Django. Permite que os administradores
    visualizem e gerenciem entradas de forma eficiente.

    Attributes:
        list_display (tuple): Campos a serem exibidos na lista de entradas.
        search_fields (tuple): Campos nos quais é possível realizar buscas
        no painel de administração.
    """

    list_display = (
        'supplier',
        'product',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'supplier__name',
        'product__title',
    )


admin.site.register(Inflow, InflowAdmin)

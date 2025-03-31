from django.contrib import admin

from suppliers.models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    """
    Administração do modelo Supplier no painel de administração do Django.
    Esta classe define as configurações de exibição e busca para o modelo
    Supplier na interface de administração. As configurações incluem quais
    campos devem ser exibidos na lista e quais campos devem ser pesquisáveis.

    list_display: Campos a serem exibidos na lista de objetos Supplier.
    search_fields: Campos que podem ser utilizados para pesquisa de Suppliers.
    """

    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Supplier, SupplierAdmin)

from django.contrib import admin

from brand.models import Brand


class BrandAdmin(admin.ModelAdmin):
    """
    Administração do modelo Brand no painel de administração do Django.
    Esta classe define as configurações de exibição e busca para o modelo
    Brand na interface de administração. As configurações incluem quais
    campos devem ser exibidos na lista e quais campos devem ser pesquisáveis.

    list_display: Campos a serem exibidos na lista de objetos Brand.
    search_fields: Campos que podem ser utilizados para pesquisa de brands.
    """

    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Brand, BrandAdmin)

from django.contrib import admin

from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    """
    Administração do modelo Category no painel de administração do Django.
    Esta classe define as configurações de exibição e busca para o modelo
    Category na interface de administração. As configurações incluem quais
    campos devem ser exibidos na lista e quais campos devem ser pesquisáveis.

    list_display: Campos a serem exibidos na lista de objetos Category.
    search_fields: Campos que podem ser utilizados para pesquisa de Categories.
    """

    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)

from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'serie_number',
    )
    search_fields = ('title',)


admin.site.register(Product, ProductAdmin)

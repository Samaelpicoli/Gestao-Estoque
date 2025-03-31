from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    """
    Formulário para a criação de produtos.

    Attributes:
        model (Product): Modelo associado ao formulário.
        fields (list): Lista de campos incluídos no formulário.
        widgets (dict): Dicionário de widgets personalizados para os campos.
        labels (dict): Dicionário de rótulos personalizados para os campos.
    """

    class Meta:
        """
        Configurações do formulário, associando-o ao modelo Product.
        """

        model = Product
        fields = [
            'title',
            'category',
            'brand',
            'description',
            'serie_number',
            'cost_price',
            'selling_price',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'serie_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'title': 'Título',
            'category': 'Categoria',
            'brand': 'Marca',
            'description': 'Descrição',
            'serie_number': 'Número de Série',
            'cost_price': 'Preço de Custo',
            'selling_price': 'Preço de Venda',
        }

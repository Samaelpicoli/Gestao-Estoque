from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from outflows.models import Outflow


class OutflowForm(forms.ModelForm):
    """
    Formulário para a criação de saídas.

    Attributes:
        model (Outflow): Modelo associado ao formulário.
        fields (list): Lista de campos incluídos no formulário.
        widgets (dict): Dicionário de widgets personalizados para os campos.
        labels (dict): Dicionário de rótulos personalizados para os campos.
    """

    class Meta:
        """
        Configurações do formulário, associando-o ao modelo Outflow.
        """

        model = Outflow
        fields = ['product', 'quantity', 'description']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }

    def clean_quantity(self) -> Any:
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if quantity > product.quantity:
            raise ValidationError(
                f'A quantidade disponível em estoque para o produto {product.title} é de {product.quantity} unidades.'  # noqa: E501
            )
        return quantity

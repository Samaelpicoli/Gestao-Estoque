from django import forms

from inflows.models import Inflow


class InflowForm(forms.ModelForm):
    """
    Formulário para a criação de entradas.

    Attributes:
        model (Inflow): Modelo associado ao formulário.
        fields (list): Lista de campos incluídos no formulário.
        widgets (dict): Dicionário de widgets personalizados para os campos.
        labels (dict): Dicionário de rótulos personalizados para os campos.
    """

    class Meta:
        """
        Configurações do formulário, associando-o ao modelo Inflow.
        """

        model = Inflow
        fields = ['supplier', 'product', 'quantity', 'description']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
        labels = {
            'supplier': 'Fornecedor',
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }

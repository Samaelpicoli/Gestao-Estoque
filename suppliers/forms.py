from django import forms

from suppliers.models import Supplier


class SupplierForm(forms.ModelForm):
    """
    Formulário para a criação e edição de fornecedores.

    Attributes:
        model (Supplier): Modelo associado ao formulário.
        fields (list): Lista de campos incluídos no formulário.
        widgets (dict): Dicionário de widgets personalizados para os campos.
        labels (dict): Dicionário de rótulos personalizados para os campos.
    """

    class Meta:
        """
        Configurações do formulário, associando-o ao modelo Supplier.
        """

        model = Supplier
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
        labels = {'name': 'Nome', 'description': 'Descrição'}

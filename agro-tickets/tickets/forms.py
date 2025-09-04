from django import forms
from import_export.forms import ImportForm, ExportForm
from .models import Category, Ticket

class CustomImportForm(ImportForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Categoría por defecto para tickets importados"
    )
    
    update_existing = forms.BooleanField(
        required=False,
        initial=True,
        label="Actualizar registros existentes"
    )

class CustomExportForm(ExportForm):
    status_filter = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Ticket.STATUS_CHOICES),
        required=False,
        label="Filtrar por estado"
    )
    
    date_range = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD to YYYY-MM-DD'}),
        label="Rango de fechas (creación)"
    )
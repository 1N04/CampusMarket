from django import forms
from .models import Item, Category, Condition


class ItemForm(forms.ModelForm):
    """Form for creating and editing items."""

    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'category', 'condition', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your item...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'condition': forms.Select(attrs={
                'class': 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class ItemSearchForm(forms.Form):
    """Form for searching and filtering items."""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search items...',
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Min price',
        }),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Max price',
        }),
    )
    condition = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Condition')] + Condition.choices,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

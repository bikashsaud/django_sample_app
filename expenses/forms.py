# expenses/forms.py
from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'title', 'description', 'amount', 'category']
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Choose your option', widget=forms.Select(attrs={'class': 'form-select'}))
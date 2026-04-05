from django import forms
from .models import Transaction, Budget


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'date']


from django import forms
from .models import Budget
import datetime


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']

    def clean_month(self):
        month = self.cleaned_data.get('month')
        if month < 1 or month > 12:
            raise forms.ValidationError("Month must be between 1 and 12")
        return month

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = datetime.datetime.now().year
        if year < current_year - 5 or year > current_year + 5:
            raise forms.ValidationError("Invalid year selected")
        return year

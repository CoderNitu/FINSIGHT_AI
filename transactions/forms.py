from django import forms
from .models import Transaction, Category


class CategoryForm(forms.ModelForm):
        """
        A simple form for creating a new Category.
        """
        class Meta:
            model = Category
            fields = ['name']
            widgets = {
                'name': forms.TextInput(attrs={'placeholder': 'e.g., Groceries, Salary'}),
            }
    

class TransactionForm(forms.ModelForm):
        """
        A form for creating and updating Transaction instances.
        """
        class Meta:
            model = Transaction
            # We only want users to fill in these fields. The 'user' will be set automatically.
            fields = ['transaction_type', 'amount', 'description', 'category', 'date']
            widgets = {
                'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            }

        def __init__(self, *args, **kwargs):
            # We need to get the user from the view to filter the categories
            user = kwargs.pop('user', None)
            super(TransactionForm, self).__init__(*args, **kwargs)
            
            # This is the magic! We are filtering the 'category' queryset
            # to only show categories that belong to the currently logged-in user.
            if user:
                self.fields['category'].queryset = Category.objects.filter(user=user)
            
            # We can also add a placeholder for categories if none exist
            self.fields['category'].empty_label = "Select a Category (Optional)"

            # Making the form look better with Bootstrap classes
            for field_name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})

    


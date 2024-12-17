from django import forms
from .models import Transaction, Product


class TransactionForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label='Quantity')

    class Meta:
        model = Transaction
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['quantity'].widget.attrs['max'] = product.stock
            if product.stock == 0:
                self.fields['quantity'].widget.attrs['disabled'] = True


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['quantity'].widget.attrs['max'] = product.stock
            if product.stock == 0:
                self.fields['quantity'].widget.attrs['disabled'] = True

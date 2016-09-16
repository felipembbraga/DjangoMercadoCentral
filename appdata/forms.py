from django import forms

from appdata.models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'sections']

    def clean(self):
        return super(ProductAddForm, self).clean()




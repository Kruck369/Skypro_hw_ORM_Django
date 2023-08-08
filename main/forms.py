from django import forms


from main.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-select'})


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'preview', 'price', 'category', 'is_published')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        forbidden_names = ['казино',
                           'криптовалюта',
                           'крипта',
                           'биржа',
                           'дешево',
                           'бесплатно',
                           'обман',
                           'полиция',
                           'радар'
                           ]
        for name in forbidden_names:
            if name.lower() in cleaned_data.lower():
                raise forms.ValidationError('Запрещенный продукт')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


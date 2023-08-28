from django import forms


from mailing.models import Newsletter, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-select'})


class NewsletterForm(StyleFormMixin, forms.ModelForm):
    client = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Client.objects.all(),
    )

    class Meta:
        model = Newsletter
        fields = ('client', 'time', 'message', 'frequency')


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'comment',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ('subject', 'body',)

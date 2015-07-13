from django import forms
from django.utils.translation import gettext
from application.apps.interest.models import Interest


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ('first_name', 'last_name', 'email', 'phone',)

    def __init__(self, *args, **kwargs):
        super(InterestForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = gettext('First name')
        self.fields['last_name'].label = gettext('Last name')
        self.fields['email'].label = gettext('Email')
        self.fields['phone'].label = gettext('Phone')

        for name, field in self.fields.items():
            if field.widget.__class__ == forms.widgets.TextInput:
                if field.widget.attrs.has_key('class'):
                    field.widget.attrs['class'] += ' span5'
                else:
                    field.widget.attrs.update({'class': 'span5'})

from django import forms
from models import Ticket


class ContactForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('ip', )

    def __init__(self, request=None, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.request = request

    def save(self, commit=True):
        m = super(forms.ModelForm, self).save(commit=False)

        m.ip = self.request.META['REMOTE_ADDR']

        if commit:
            m.save()
        return m

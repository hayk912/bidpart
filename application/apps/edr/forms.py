from django import forms
from application.apps.edr.models import OptOut


class OptOutForm(forms.ModelForm):
    class Meta:
        model = OptOut
        fields = ('email',)

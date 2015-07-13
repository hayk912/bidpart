from django.forms import ModelChoiceField, ModelMultipleChoiceField

class LocalizedFieldMixin(object):

    def __init__(self, *args, **kwargs):
        self.locale = kwargs.pop('locale', 'en')
        self.model_field = kwargs.pop('model_field')

        super(LocalizedFieldMixin, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return obj.get_localized(self.model_field, self.locale)


class LocalizedModelChoiceField(LocalizedFieldMixin, ModelChoiceField):
    pass


class LocalizedModelMultipleChoiceField(LocalizedFieldMixin, ModelMultipleChoiceField):
    pass

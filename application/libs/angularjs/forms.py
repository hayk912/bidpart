from django.forms.widgets import Select


class AngularSelect(Select):
    def __init__(self, attrs=None, choices=(), options_tmpl=None):
        self.options_tmpl = options_tmpl
        super(AngularSelect, self).__init__(attrs, choices)

    def render_options(self, choices, selected_choices):
        return self.options_tmpl or ''

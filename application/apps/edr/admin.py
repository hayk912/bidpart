from django.contrib import admin
from application.apps.edr.models import OptOut


class OptOutAdmin(admin.ModelAdmin):
    pass


admin.site.register(OptOut, OptOutAdmin)

from django.contrib import admin
from application.apps.interest.models import Interest


class InterestAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'phone', 'created')
    pass


admin.site.register(Interest, InterestAdmin)

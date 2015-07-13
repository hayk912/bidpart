from django.db import models
from django.utils.translation import gettext


class OptOut(models.Model):
   email = models.EmailField()

   updated = models.DateTimeField(auto_now=True, verbose_name=gettext('Updated'))
   created = models.DateTimeField(auto_now_add=True, verbose_name=gettext('Created'))

from django.db import models


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    cc_myself = models.BooleanField()
    ip = models.IPAddressField()

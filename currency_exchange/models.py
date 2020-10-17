from django.db import models

class currency_details(models.Model):
    currency_name = models.CharField(max_length=50, default='')
    currency_abbrev = models.CharField(max_length=5, default='')

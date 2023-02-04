from django.db import models

# Create your models here.

class Candle(models.Model):
    id = models.AutoField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    date = models.DateTimeField()

from django.db import models

# Create your models here.
class SensorData(models.Model):

    reading_timestamp = models.FloatField(default=0)
    reading = models.FloatField(default=0.0)
    sensor_type = models.CharField(max_length=100,null=True,blank=True)
    reading_date = models.DateField(null=True,blank=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
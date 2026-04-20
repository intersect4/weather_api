from django.db import models

# Create your models here.
class WeatherRecord(models.Model): 
    city = models.CharField(max_length=100) 
    temperature = models.FloatField()
    humidity = models.FloatField() 
    timestamp = models.DateTimeField(auto_now_add=True)  # Campo obligatorio 

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"
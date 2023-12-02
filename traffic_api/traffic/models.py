from django.db import models

# Create your models here.
from django.db import models

class RoadSegment(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.JSONField()
    speed_limit = models.IntegerField(null=True)

class TrafficDatum(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    avg_speed = models.FloatField(null=True)
    congestion_level = models.IntegerField(null=True)

class HistoricalTrafficData(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    date = models.DateField()
    data = models.JSONField()
class TrafficUpdateLog(models.Model):
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
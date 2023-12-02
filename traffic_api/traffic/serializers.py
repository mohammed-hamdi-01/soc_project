from rest_framework import serializers
from .models import RoadSegment, TrafficDatum, HistoricalTrafficData

class RoadSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSegment
        fields = "__all__"

class TrafficDatumSerializer(serializers.ModelSerializer):
    road_segment = RoadSegmentSerializer()
    class Meta:
        model = TrafficDatum
        fields = "__all__"

class HistoricalTrafficDataSerializer(serializers.ModelSerializer):
    road_segment = RoadSegmentSerializer()
    class Meta:
        model = HistoricalTrafficData
        fields = "__all__"

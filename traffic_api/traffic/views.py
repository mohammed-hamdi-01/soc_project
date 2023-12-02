from rest_framework import viewsets
from .models import RoadSegment, TrafficDatum, HistoricalTrafficData
from .serializers import RoadSegmentSerializer, TrafficDatumSerializer, HistoricalTrafficDataSerializer
from .tasks import update_traffic_data

class TrafficViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer

    def list(self, request):
        # Update traffic data before returning list
        update_traffic_data.delay()
        return super().list(request)

    def retrieve(self, request, pk=None):
        # Update traffic data before retrieving specific road segment
        update_traffic_data.delay()
        return super().retrieve(request, pk)

class TrafficDatumViewSet(viewsets.ModelViewSet):
    queryset = TrafficDatum.objects.all()
    serializer_class = TrafficDatumSerializer

class HistoricalTrafficDataViewSet(viewsets.ModelViewSet):
    queryset = HistoricalTrafficData.objects.all()
    serializer_class = HistoricalTrafficDataSerializer

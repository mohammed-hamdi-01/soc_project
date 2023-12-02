from celery import shared_task
import requests
from .models import RoadSegment, TrafficDatum, HistoricalTrafficData, TrafficUpdateLog
import logging
import datetime
logger = logging.getLogger(__name__)

@shared_task
def update_traffic_data():
    # Initialize TomTom API URL
    api_url = "https://api.tomtom.com/traffic/flow/json"

    # Loop through all road segments
    for road_segment in RoadSegment.objects.all():
        try:
            # Set API request parameters
            params = {
                "point": f"[{road_segment.coordinates[0]}, {road_segment.coordinates[1]}]",
                "zoom": 16,
                "key": "YOUR_API_KEY",  # Replace with your TomTom API key
            }

            # Make the API request
            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                json_data = response.json()
                traffic_data = json_data.get("flow")

                # Process and save traffic data
                avg_speed = traffic_data.get("averageSpeed", None)
                congestion_level = traffic_data.get("congestionLevel", None)

                TrafficDatum.objects.create(
                    road_segment=road_segment,
                    avg_speed=avg_speed,
                    congestion_level=congestion_level
                )

                # Save historical data for the day
                historical_data = {
                    "avg_speed": avg_speed,
                    "congestion_level": congestion_level
                }
                HistoricalTrafficData.objects.create(
                    road_segment=road_segment,
                    date=datetime.now().date(),
                    data=historical_data
                )

                # Log successful update
                TrafficUpdateLog.objects.create(road_segment=road_segment, success=True)
            else:
                logger.error(f"Error fetching traffic data for road segment {road_segment.id}: {response.status_code}")
                TrafficUpdateLog.objects.create(road_segment=road_segment, success=False, error_message=str(response.status_code))

        except Exception as e:
            logger.error(f"Unexpected error updating traffic data for road segment {road_segment.id}: {e}")
            TrafficUpdateLog.objects.create(road_segment=road_segment, success=False, error_message=str(e))


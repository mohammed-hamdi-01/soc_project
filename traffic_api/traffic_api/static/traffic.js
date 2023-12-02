mapboxgl.accessToken = "YOUR_MAPBOX_ACCESS_TOKEN";
const map = new mapboxgl.Map({
    container: "map-container",
    style: "mapbox://styles/mapbox/streets-v11",
    zoom: 9,
    center: [9.537499, 33.886917]
});

// Fetch all road segments
axios.get("/traffic/")
    .then(response => {
        const roadSegments = response.data;
        // Add markers and info to UI
        for (const roadSegment of roadSegments) {
            const marker = new mapboxgl.Marker()
                .setLngLat([roadSegment.coordinates[0], roadSegment.coordinates[1]])
                .addTo(map);

            const infoElement = document.createElement("li");
            infoElement.innerText = `${roadSegment.name}: Loading...`;
            document.getElementById("traffic-info-list").appendChild(infoElement);

            // Update info with real-time data
            axios.get(`/traffic/${roadSegment.id}/data/`)
                .then(data => {
                    const trafficData = data.data;
                    infoElement.innerText = `${roadSegment.name}: Avg Speed: ${trafficData.avg_speed} km/h, Congestion Level: ${trafficData.congestion_level}`;
                })
                .catch(error => {
                    console.error(error);
                    infoElement.innerText = `${roadSegment.name}: Error fetching data`;
                });
        }
    })
    .catch(error => {
        console.error(error);
    });

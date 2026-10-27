import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { ItineraryItem } from '../../types';

interface TripMapProps {
  destination: string;
  activities: ItineraryItem[];
  selectedDay?: number | null;
}

export const TripMap: React.FC<TripMapProps> = ({ destination, activities, selectedDay }) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerGroupRef = useRef<L.LayerGroup | null>(null);

  // Filter activities if a specific day is selected
  const displayedActivities = selectedDay
    ? activities.filter((a) => a.day_number === selectedDay)
    : activities;

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Find initial center from activities with valid lat/lng
      const firstValid = activities.find((a) => a.latitude && a.longitude);
      const initialLat = firstValid?.latitude || 15.2993;
      const initialLng = firstValid?.longitude || 74.1240;

      const map = L.map(mapContainerRef.current, {
        center: [initialLat, initialLng],
        zoom: 12,
        zoomControl: true,
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }).addTo(map);

      layerGroupRef.current = L.layerGroup().addTo(map);
      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;
    const layerGroup = layerGroupRef.current;
    if (!map || !layerGroup) return;

    layerGroup.clearLayers();

    const validCoordinates: L.LatLngTuple[] = [];

    // Custom Emerald Map Marker Icon
    const createCustomIcon = (dayNum: number, idx: number) => {
      return L.divIcon({
        className: 'custom-map-marker',
        html: `
          <div style="
            background: linear-gradient(135deg, #143628, #10B981);
            color: white;
            font-size: 11px;
            font-weight: 700;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid white;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
          ">
            D${dayNum}
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -14],
      });
    };

    displayedActivities.forEach((act, idx) => {
      if (act.latitude && act.longitude) {
        const coord: L.LatLngTuple = [act.latitude, act.longitude];
        validCoordinates.push(coord);

        const popupContent = `
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; padding: 4px; min-width: 180px;">
            <div style="font-size: 10px; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 0.5px;">
              Day ${act.day_number} &bull; ${act.suggested_start_time}
            </div>
            <div style="font-size: 13px; font-weight: 700; color: #0F1E28; margin-top: 2px;">
              ${act.activity_name}
            </div>
            <p style="font-size: 11px; color: #5A6D7C; margin-top: 4px; margin-bottom: 6px;">
              ${act.description.substring(0, 110)}...
            </p>
            <div style="font-size: 10px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 4px;">
              Duration: ${act.estimated_duration_hours}h &bull; Cost: ₹${act.estimated_cost.toLocaleString()}
            </div>
          </div>
        `;

        const marker = L.marker(coord, { icon: createCustomIcon(act.day_number, idx) })
          .bindPopup(popupContent);
        layerGroup.addLayer(marker);
      }
    });

    // Draw route line connecting chronological stops if there are at least 2 points
    if (validCoordinates.length >= 2) {
      const polyline = L.polyline(validCoordinates, {
        color: '#10B981',
        weight: 3,
        dashArray: '5, 8',
        opacity: 0.8,
      });
      layerGroup.addLayer(polyline);
    }

    if (validCoordinates.length > 0) {
      const bounds = L.latLngBounds(validCoordinates);
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
    }

    setTimeout(() => {
      map.invalidateSize();
    }, 200);
  }, [displayedActivities, selectedDay]);

  return (
    <div className="relative w-full h-[450px] rounded-2xl overflow-hidden shadow-sm border border-[#E7E5DF]">
      <div ref={mapContainerRef} className="w-full h-full z-10" />
      <div className="absolute top-3 right-3 z-20 bg-white/95 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-[#E2E0D8] text-[11px] font-semibold text-[#143628] shadow-sm">
        {selectedDay ? `Filtering Day ${selectedDay}` : `All ${displayedActivities.length} Itinerary Stops`} &bull; {destination}
      </div>
    </div>
  );
};

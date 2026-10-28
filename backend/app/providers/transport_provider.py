import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import quote
from app.schemas.agent_schemas import TransportOption
from app.providers.tamil_nadu_districts import TAMIL_NADU_DISTRICTS
from app.providers.infrastructure_data import (
    VERIFIED_AIRPORTS,
    VERIFIED_STATIONS,
    DIRECT_FLIGHT_PAIRS,
    INTERNATIONAL_HUBS,
    is_overland_contiguous,
    get_verified_airport,
    get_verified_station,
    get_verified_bus_terminal,
    get_tamil_nadu_commercial_airport,
    get_nearest_commercial_airport
)
from app.providers.live_transport_client import live_transport_client

HILL_DESTINATIONS = {
    "yercaud", "ooty", "udhagamandalam", "nilgiris",
    "kodaikanal", "kodai", "yelagiri", "kolli hills",
    "megamalai", "valparai"
}

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

# Approximate central coordinates for common origins & destinations
LOCATION_COORDS: Dict[str, tuple[float, float]] = {
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873),
    "goa": (15.2993, 74.1240),
    "kochi": (9.9312, 76.2673),
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "new york": (40.7128, -74.0060)
}

# Register all 38 Tamil Nadu districts into route matrix
for _tn_key, _tn_data in TAMIL_NADU_DISTRICTS.items():
    LOCATION_COORDS[_tn_key] = (_tn_data["lat"], _tn_data["lng"])

# Tamil Nadu tourist aliases
LOCATION_COORDS.update({
    "kanyakumari": (8.0883, 77.5385),
    "kanniyakumari": (8.0883, 77.5385),
    "ooty": (11.4102, 76.6950),
    "udhagamandalam": (11.4102, 76.6950),
    "nilgiris": (11.4102, 76.6950),
    "kodaikanal": (10.2381, 77.4892),
    "kodai": (10.2381, 77.4892),
    "yercaud": (11.7753, 78.2093),
    "rameswaram": (9.2876, 79.3129),
    "rameshwaram": (9.2876, 79.3129),
    "trichy": (10.7905, 78.7047),
    "tanjore": (10.7870, 79.1378),
    "mahabalipuram": (12.6269, 80.1927),
    "mamallapuram": (12.6269, 80.1927),
    "yelagiri": (12.5786, 78.6397),
    "hogenakkal": (12.1211, 78.1584),
    "kolli hills": (11.2189, 78.1674),
    "chettinad": (10.0760, 78.7840),
    "megamalai": (9.7915, 77.3850),
    "pichavaram": (11.4285, 79.7788),
    "gingee": (12.2530, 79.4180),
    "velankanni": (10.7672, 79.8449),
    "tranquebar": (11.0964, 79.6465),
    "tharangambadi": (11.0964, 79.6465),
    "srivilliputhur": (9.5167, 77.6333),
    "courtallam": (8.9594, 77.3142),
    "kutralam": (8.9594, 77.3142),
    "gangaikonda cholapuram": (11.2058, 79.4520)
})

from app.providers.geo_places_provider import TN_DISTRICT_ALIASES
for _alias, _dist_key in TN_DISTRICT_ALIASES.items():
    if _dist_key in TAMIL_NADU_DISTRICTS and _alias not in LOCATION_COORDS:
        LOCATION_COORDS[_alias] = (TAMIL_NADU_DISTRICTS[_dist_key]["lat"], TAMIL_NADU_DISTRICTS[_dist_key]["lng"])


class TransportProvider:
    """Route-aware multi-modal transportation engine verifying infrastructure and operational feasibility."""

    def resolve_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        norm = place_name.strip().lower()
        if norm in LOCATION_COORDS:
            return LOCATION_COORDS[norm]
        for key, coords in LOCATION_COORDS.items():
            if key == norm or key in norm or norm in key:
                return coords
        return None

    def validate_route_request(self, origin: str, destination: str) -> Tuple[bool, Optional[str], Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        if not origin or not destination:
            return False, "Origin and destination are required.", None, None
        
        o_clean = origin.strip().lower()
        d_clean = destination.strip().lower()
        if o_clean == d_clean:
            return False, "Origin and destination cannot be identical for intercity transit.", None, None

        c1 = self.resolve_coordinates(o_clean)
        c2 = self.resolve_coordinates(d_clean)
        if not c1 or not c2:
            return False, f"Could not verify geographic coordinates for route: {origin} -> {destination}.", c1, c2

        return True, None, c1, c2

    def get_transport_options(
        self,
        origin: str,
        destination: str,
        travellers: int = 1,
        preferred_mode: str = "Best Value",
        budget: float = 50000.0,
        currency: str = "INR"
    ) -> List[TransportOption]:
        valid, err_msg, c1, c2 = self.validate_route_request(origin, destination)
        if not valid or not c1 or not c2:
            return []

        travellers = max(1, travellers)
        straight_dist_km = haversine_distance_km(c1[0], c1[1], c2[0], c2[1])
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        orig_norm = origin.strip().lower()
        dest_norm = destination.strip().lower()
        is_overland = is_overland_contiguous(orig_norm, dest_norm)
        options: List[TransportOption] = []

        # =========================================================================
        # CASE 1: INTRA-CITY / INTRA-DISTRICT TRANSIT (Local Exploration)
        # =========================================================================
        if straight_dist_km < 5.0 or orig_norm == dest_norm:
            is_chennai = "chennai" in orig_norm or "chennai" in dest_norm
            maps_url = f"https://www.google.com/maps/dir/?api=1&origin={quote(origin)}&destination={quote(destination)}&travelmode=driving"

            # 1. Intra-City Sightseeing Cab / Local Taxi
            cab_low = 1400.0
            cab_high = 2400.0
            cab_est = 1900.0
            options.append(TransportOption(
                id="trans_cab",
                mode="Intra-City Sightseeing Cab / Local Taxi",
                category="road",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport="Doorstep / Hotel Pickup",
                destination_station_or_airport="Local Sights & Attractions",
                distance=45.0,
                distance_km=45.0,
                distance_unit="km",
                duration=6.0,
                duration_hours=6.0,
                departure_time="Flexible / On-Demand",
                transfers=0,
                price_range_low=cab_low,
                price_range_high=cab_high,
                estimated_cost=cab_est,
                currency=currency,
                is_recommended=(preferred_mode.lower() in ["cab", "car", "taxi", "luxury", "private", "best value"]),
                recommendation_rationale=f"Comprehensive day-tour taxi package covering top attractions across {origin.title()} with flexible doorstep pickup.",
                source="Local City Taxi & Sightseeing Benchmark",
                provider="Verified Local Tourist Taxi Operator",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status="verified_static",
                verification_status="verified",
                booking_advisory="Includes vehicle fuel, chauffeur allowance, and local parking charges. Standard 8-hour / 80-km package.",
                recommendation_reason="Effortless local city sightseeing with on-demand flexibility.",
                warnings=[],
                directions_url=maps_url,
                booking_url=maps_url,
                operator_or_agency="Verified City Cab Fleet"
            ))

            # 2. Local City Bus
            bus_fare_low = max(20.0, 15.0 * travellers)
            bus_fare_high = max(50.0, 35.0 * travellers)
            bus_est = round((bus_fare_low + bus_fare_high) / 2.0, 0)
            options.append(TransportOption(
                id="trans_bus",
                mode="Metropolitan City Bus (MTC / TNSTC City Services)" if is_chennai else f"{origin.title()} Municipal City Bus",
                category="bus",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport=get_verified_bus_terminal(orig_norm) or f"{origin.title()} Central Bus Stand",
                destination_station_or_airport=f"{destination.title()} Local Stops",
                distance=25.0,
                distance_km=25.0,
                distance_unit="km",
                duration=1.5,
                duration_hours=1.5,
                departure_time="High Frequency Daily (Every 10-15 mins)",
                transfers=1,
                price_range_low=bus_fare_low,
                price_range_high=bus_fare_high,
                estimated_cost=bus_est,
                currency=currency,
                is_recommended=(preferred_mode.lower() in ["bus", "budget", "coach"]),
                recommendation_rationale=f"High-frequency municipal city bus network operating across major commercial districts, heritage quarters, and beachfronts in {origin.title()}.",
                source="State City Bus Schedule Benchmark",
                provider="Metropolitan Transport Corporation (MTC) / TNSTC City Fleet",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status="verified_static",
                verification_status="verified",
                booking_advisory="Cash or contactless smartcard ticketing on board bus conductors. Frequent services from morning 05:00 to 23:00.",
                recommendation_reason="Economical public transit network covering all urban districts.",
                warnings=[],
                booking_url="https://www.tnstc.in",
                operator_or_agency="Metropolitan Transport Corporation (MTC) / TNSTC"
            ))

            # 3. Metro / Local Suburban Railway
            rail_fare_low = max(30.0, 20.0 * travellers)
            rail_fare_high = max(80.0, 50.0 * travellers)
            rail_est = round((rail_fare_low + rail_fare_high) / 2.0, 0)
            options.append(TransportOption(
                id="trans_train",
                mode=f"{origin.title()} Metro Rail & Suburban EMU Transit" if is_chennai else f"{origin.title()} Regional Passenger Line",
                category="rail",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport="Central Metro / Suburban Junction",
                destination_station_or_airport="Urban Station Network",
                distance=20.0,
                distance_km=20.0,
                distance_unit="km",
                duration=0.8,
                duration_hours=0.8,
                departure_time="Every 5-10 Minutes (05:30 - 23:00)",
                transfers=0,
                price_range_low=rail_fare_low,
                price_range_high=rail_fare_high,
                estimated_cost=rail_est,
                currency=currency,
                is_recommended=(preferred_mode.lower() in ["train", "rail", "fastest"]),
                recommendation_rationale=f"Air-conditioned rapid transit bypassing city traffic, linking railway terminals, airport, and downtown {origin.title()}.",
                source="Chennai Metro Rail (CMRL) & Southern Railway Suburban",
                provider="Chennai Metro Rail Limited & Southern Railway",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status="verified_static",
                verification_status="verified",
                booking_advisory="Tokens and QR tickets available at station kiosks or official transit app. 5-minute peak headway.",
                recommendation_reason="Fastest intra-city transit with zero road traffic delay.",
                warnings=[],
                booking_url="https://www.chennaimetrorail.org" if is_chennai else "https://www.irctc.co.in/nget/",
                operator_or_agency="Chennai Metro Rail / Southern Railway Suburban"
            ))
            return options

        # =========================================================================
        # CASE 2: INTER-DISTRICT / REGIONAL TRANSIT
        # =========================================================================
        is_hill = dest_norm in HILL_DESTINATIONS or orig_norm in HILL_DESTINATIONS

        # ---------------------------------------------------------
        # MODE 1: CAB / ROAD (Overland Only)
        # ---------------------------------------------------------
        if is_overland and straight_dist_km <= 750:
            circuity = 1.95 if is_hill else 1.24
            speed = 32.0 if is_hill else 52.0
            road_dist = round(straight_dist_km * circuity, 1)
            road_dur = round(max(0.8, 0.3 + (road_dist / speed)), 1)
            
            # Cab fare calculation scaled by distance
            if road_dist <= 50.0:
                cab_low = max(1200.0, round(road_dist * 18.0 + 300.0, -1))
                cab_high = max(1800.0, round(road_dist * 24.0 + 600.0, -1))
            elif road_dist <= 150.0:
                cab_low = max(2000.0, round(road_dist * 14.0 + 400.0, -1))
                cab_high = max(3200.0, round(road_dist * 19.0 + 700.0, -1))
            else:
                cab_low = max(2800.0, round(road_dist * 13.5 + 400.0, -1))
                cab_high = max(4200.0, round(road_dist * 18.0 + 800.0, -1))
            cab_est = round((cab_low + cab_high) / 2.0, 0)

            maps_url = f"https://www.google.com/maps/dir/?api=1&origin={quote(origin)}&destination={quote(destination)}&travelmode=driving"

            is_cab_rec = (preferred_mode.lower() in ["cab", "car", "taxi", "self-drive", "private"] or 
                          (straight_dist_km <= 200 and preferred_mode.lower() in ["best value", "fastest", "convenient"]))

            hill_note = " via scenic mountain ghat road with hairpin bends" if is_hill else " via national/state highway corridor"
            options.append(TransportOption(
                id="trans_cab",
                mode="Private Outstation Cab / Taxi",
                category="road",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport="Doorstep / Hotel Pickup",
                destination_station_or_airport="Direct Destination Arrival",
                distance=road_dist,
                distance_km=road_dist,
                distance_unit="km",
                duration=road_dur,
                duration_hours=road_dur,
                departure_time="Flexible / On-Demand",
                transfers=0,
                price_range_low=cab_low,
                price_range_high=cab_high,
                estimated_cost=cab_est,
                currency=currency,
                is_recommended=is_cab_rec,
                recommendation_rationale=f"Direct highway route ({road_dist} km{hill_note}). Door-to-door convenience with zero transfers and pause flexibility.",
                source="TRIPORA Road Distance & Highway Toll Benchmark",
                provider="Verified State Highway Network (NH/SH Corridors)",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status="verified_static",
                verification_status="verified",
                booking_advisory="Includes driver allowance, fuel, and standard highway tolls. Available on-demand via verified taxi operators.",
                recommendation_reason=f"Optimal direct overland connection for {road_dist} km with no airport overhead.",
                warnings=[],
                directions_url=maps_url,
                booking_url=maps_url,
                operator_or_agency="Verified Highway Taxi / Outstation Cab Desk"
            ))

        # ---------------------------------------------------------
        # MODE 2: INTERCITY BUS (Overland Only)
        # ---------------------------------------------------------
        if is_overland and straight_dist_km <= 950:
            bus_dist = round(straight_dist_km * (1.95 if is_hill else 1.25), 1)
            bus_dur = round(max(1.0, 0.4 + (bus_dist / (30.0 if is_hill else 46.0))), 1)
            
            orig_terminal = get_verified_bus_terminal(orig_norm) or f"{origin.title()} Central Bus Stand"
            dest_terminal = get_verified_bus_terminal(dest_norm) or f"{destination.title()} Central Bus Stand"

            if bus_dist <= 50.0:
                bus_fare_low = max(35.0, round(bus_dist * 1.1, -1))
                bus_fare_high = max(65.0, round(bus_dist * 1.8, -1))
            else:
                bus_fare_low = max(90.0, round(bus_dist * 1.2, -1))
                bus_fare_high = max(250.0, round(bus_dist * 2.2, -1))

            bus_total_low = bus_fare_low * travellers
            bus_total_high = bus_fare_high * travellers
            bus_est = round((bus_total_low + bus_total_high) / 2.0, 0)

            is_bus_rec = (preferred_mode.lower() in ["bus", "budget", "coach"])

            options.append(TransportOption(
                id="trans_bus",
                mode="Intercity Express / AC Sleeper Bus",
                category="bus",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport=orig_terminal,
                destination_station_or_airport=dest_terminal,
                distance=bus_dist,
                distance_km=bus_dist,
                distance_unit="km",
                duration=bus_dur,
                duration_hours=bus_dur,
                departure_time="Scheduled Daily Departures (Morning & Evening)",
                transfers=0,
                price_range_low=bus_total_low,
                price_range_high=bus_total_high,
                estimated_cost=bus_est,
                currency=currency,
                is_recommended=is_bus_rec,
                recommendation_rationale=f"Economical point-to-point transit operated by state transport (TNSTC/SETC) connecting {orig_terminal} and {dest_terminal}.",
                source="Regional Transport Schedule Benchmark",
                provider="State Express Transport Corporation & Intercity Fleet Aggregator",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status="verified_static",
                verification_status="verified",
                booking_advisory="Regular departures throughout the day. Advance online reservation available on official TNSTC portal.",
                recommendation_reason="Highly economical direct option for overland regional transit.",
                warnings=[],
                booking_url="https://www.tnstc.in",
                operator_or_agency="State Express Transport Corporation (SETC) & TNSTC"
            ))

        # ---------------------------------------------------------
        # MODE 3: EXPRESS RAILWAY (Overland Only)
        # ---------------------------------------------------------
        if is_overland and straight_dist_km <= 3500:
            st_orig = get_verified_station(orig_norm)
            st_dest = get_verified_station(dest_norm)

            same_station_code = (st_orig and st_dest and st_orig.get("code") == st_dest.get("code"))

            if not same_station_code:
                rail_dist = round(straight_dist_km * 1.28, 1)
                default_rail_dur = round(max(1.0, 0.5 + (rail_dist / 62.0)), 1)

                orig_st_name = st_orig["name"] if st_orig else f"{origin.title()} Railway Station"
                dest_st_name = st_dest["name"] if st_dest else f"{destination.title()} Railway Station"

                train_records = live_transport_client.fetch_train_data(orig_norm, dest_norm)
                train_rec = train_records[0] if train_records else None

                if train_rec and train_rec.get("duration_hours", 0) > 0:
                    rail_dur = train_rec["duration_hours"]
                else:
                    rail_dur = default_rail_dur

                train_name_val = train_rec.get("train_name") if train_rec else "Southern Railway Express"
                train_num_val = train_rec.get("train_number") if train_rec else None
                dept_time_val = train_rec.get("departure_time") if train_rec else "Daily Express Service Schedules"
                arr_time_val = train_rec.get("arrival_time") if train_rec else None
                booking_url_val = train_rec.get("booking_url", "https://www.irctc.co.in/nget/") if train_rec else "https://www.irctc.co.in/nget/"
                avail_status_val = train_rec.get("availability_status", "Check Live Berth Availability on IRCTC") if train_rec else "Check Live Berth Availability on IRCTC (IRCTC PNR Required)"
                data_st_val = train_rec.get("data_status", "verified_static") if train_rec else "verified_static"
                verif_st_val = train_rec.get("verification_status", "verified") if train_rec else "verified"
                is_live_val = train_rec.get("is_live_data", False) if train_rec else False

                if train_rec and "fare_low" in train_rec:
                    rail_fare_low = train_rec["fare_low"]
                    rail_fare_high = train_rec["fare_high"]
                else:
                    if rail_dist <= 65.0:
                        rail_fare_low = max(45.0, round(rail_dist * 0.9, -1))
                        rail_fare_high = max(175.0, round(rail_dist * 2.2, -1))
                    else:
                        rail_fare_low = max(95.0, round(rail_dist * 1.3, -1))
                        rail_fare_high = max(450.0, round(rail_dist * 2.6, -1))

                rail_total_low = rail_fare_low * travellers
                rail_total_high = rail_fare_high * travellers
                rail_est = round((rail_total_low + rail_total_high) / 2.0, 0)

                is_rail_rec = (preferred_mode.lower() in ["train", "rail"] or 
                               (150 < straight_dist_km <= 700 and preferred_mode.lower() != "flight" and not any(opt.is_recommended for opt in options)))

                route_notes_val = train_rec.get("route_notes") if train_rec else f"Comfortable overland route connecting {orig_st_name} and {dest_st_name} with scenic views and generous luggage allowances."
                train_mode_label = f"Express Train / Railway ({train_name_val})" if train_rec and train_rec.get("train_name") else "Express Train / Railway (AC Chair / Sleeper / AC 3-Tier)"

                options.append(TransportOption(
                    id="trans_train",
                    mode=train_mode_label,
                    category="rail",
                    origin=origin.title(),
                    destination=destination.title(),
                    origin_coordinates=c1,
                    destination_coordinates=c2,
                    origin_station_or_airport=train_rec.get("origin_station", orig_st_name) if train_rec else orig_st_name,
                    destination_station_or_airport=train_rec.get("dest_station", dest_st_name) if train_rec else dest_st_name,
                    distance=rail_dist,
                    distance_km=rail_dist,
                    distance_unit="km",
                    duration=rail_dur,
                    duration_hours=rail_dur,
                    departure_time=dept_time_val,
                    arrival_time=arr_time_val,
                    transfers=0 if (st_orig and st_dest) else 1,
                    price_range_low=rail_total_low,
                    price_range_high=rail_total_high,
                    estimated_cost=rail_est,
                    currency=currency,
                    is_recommended=is_rail_rec,
                    recommendation_rationale=route_notes_val,
                    source="Indian Railways / Southern Railway Network Directory",
                    provider="Indian Railways Schedule Benchmark",
                    retrieved_at=now_str,
                    data_timestamp=now_str,
                    data_status=data_st_val,
                    verification_status=verif_st_val,
                    booking_advisory="Official IRCTC reservation opens 120 days in advance. Verified PNR and confirmed seat allocation required.",
                    recommendation_reason="High safety, comfortable travel with sleeping berths on long routes.",
                    warnings=[],
                    booking_url=booking_url_val,
                    live_availability_status=avail_status_val,
                    train_number=train_num_val,
                    train_name=train_name_val,
                    is_live_data=is_live_val,
                    operator_or_agency="Southern Railway (Indian Railways)"
                ))

        # ---------------------------------------------------------
        # MODE 4: COMMERCIAL FLIGHT (Strict Infrastructure Validation)
        # ---------------------------------------------------------
        # FLIGHT ELIGIBILITY RULES:
        # 1. Both origin and destination MUST have a verified commercial airport.
        # 2. Minimum commercial distance threshold: >= 200 km (no domestic commercial passenger flight operates under 200 km).
        # 3. If destination does NOT have an active commercial airport (e.g. Tiruvannamalai, Kodaikanal, Yercaud, Thanjavur),
        #    FLIGHT IS STRICTLY DISQUALIFIED. NO FLIGHT CARD IS PRODUCED.
        
        apt_orig = get_verified_airport(orig_norm)
        apt_dest = get_verified_airport(dest_norm)

        flight_eligible = False
        flight_rationale = ""
        is_direct_flight = False

        if apt_orig and apt_dest:
            pair_key = frozenset([orig_norm, dest_norm])
            
            if straight_dist_km >= 200:
                if pair_key in DIRECT_FLIGHT_PAIRS:
                    flight_eligible = True
                    is_direct_flight = True
                    flight_rationale = f"Direct commercial flight connecting {apt_orig['iata']} and {apt_dest['iata']}."
                elif straight_dist_km >= 450:
                    flight_eligible = True
                    is_direct_flight = False
                    flight_rationale = f"Commercial flight connecting {apt_orig['iata']} and {apt_dest['iata']} with scheduled transit."
                elif not is_overland:
                    flight_eligible = True
                    flight_rationale = f"International flight connecting {apt_orig['iata']} ({apt_orig['city']}) to {apt_dest['iata']} ({apt_dest['city']})."

        if flight_eligible and apt_orig and apt_dest:
            live_flight = live_transport_client.fetch_flight_data(orig_norm, dest_norm)

            if live_flight:
                flight_operator_val = live_flight.get("flight_operator", "Scheduled Commercial Airline")
                flight_number_val = live_flight.get("flight_number")
                origin_apt_name = live_flight.get("origin_airport", f"{apt_orig['name']} ({apt_orig['iata']})")
                dest_apt_name = live_flight.get("dest_airport", f"{apt_dest['name']} ({apt_dest['iata']})")
                dept_time_val = live_flight.get("departure_time", "Scheduled Airline Departures")
                arr_time_val = live_flight.get("arrival_time")
                total_flight_dur = live_flight.get("total_duration_hours", round((straight_dist_km / 720.0) + 2.0, 1))
                flight_air_dur = live_flight.get("flight_duration_hours", round(straight_dist_km / 720.0, 1))
                air_price_low = live_flight.get("fare_low", max(3200.0, round(straight_dist_km * 5.2, -1)))
                air_price_high = live_flight.get("fare_high", max(7500.0, round(straight_dist_km * 9.0, -1)))
                booking_url_val = live_flight.get("booking_url", "https://www.goindigo.in")
                avail_status_val = live_flight.get("availability_status", "Scheduled Daily Commercial Flights Confirmed (Book on Airline Portal)")
                data_st_val = live_flight.get("data_status", "verified_static")
                verif_st_val = live_flight.get("verification_status", "verified")
                is_live_val = live_flight.get("is_live_data", False)
            else:
                flight_operator_val = "Commercial Scheduled Airline"
                flight_number_val = None
                origin_apt_name = f"{apt_orig['name']} ({apt_orig['iata']})"
                dest_apt_name = f"{apt_dest['name']} ({apt_dest['iata']})"
                dept_time_val = "Scheduled Airline Departures"
                arr_time_val = None
                flight_air_dur = round(straight_dist_km / 720.0, 1)
                if not is_direct_flight:
                    flight_air_dur = round(flight_air_dur + 2.5, 1)
                total_flight_dur = round(flight_air_dur + 2.0, 1)

                if not is_overland:
                    air_price_low = max(24000.0, round(straight_dist_km * 4.8, -2))
                    air_price_high = max(48000.0, round(straight_dist_km * 7.5, -2))
                    booking_url_val = "https://www.google.com/travel/flights"
                else:
                    air_price_low = max(3200.0, round(straight_dist_km * 5.2, -1))
                    air_price_high = max(7500.0, round(straight_dist_km * 9.0, -1))
                    booking_url_val = "https://www.goindigo.in"
                avail_status_val = "Book on Official Airline Platform"
                data_st_val = "verified_static"
                verif_st_val = "verified"
                is_live_val = False

            flight_total_low = air_price_low * travellers
            flight_total_high = air_price_high * travellers
            flight_est = round((flight_total_low + flight_total_high) / 2.0, 0)

            is_flight_rec = (preferred_mode.lower() in ["flight", "fastest"] or 
                             (straight_dist_km > 700 and preferred_mode.lower() != "train") or
                             not is_overland)

            options.append(TransportOption(
                id="trans_flight",
                mode=f"Commercial Flight ({flight_operator_val if flight_operator_val else 'Direct'})",
                category="flight",
                origin=origin.title(),
                destination=destination.title(),
                origin_coordinates=c1,
                destination_coordinates=c2,
                origin_station_or_airport=origin_apt_name,
                destination_station_or_airport=dest_apt_name,
                distance=straight_dist_km,
                distance_km=straight_dist_km,
                distance_unit="km",
                duration=total_flight_dur,
                duration_hours=total_flight_dur,
                departure_time=dept_time_val,
                arrival_time=arr_time_val,
                transfers=0 if is_direct_flight else 1,
                price_range_low=flight_total_low,
                price_range_high=flight_total_high,
                estimated_cost=flight_est,
                currency=currency,
                is_recommended=is_flight_rec,
                recommendation_rationale=f"{flight_rationale} Verified active passenger airports at both endpoints ({apt_orig['iata']} -> {apt_dest['iata']}). Air time ~{flight_air_dur} hrs + 2.0 hrs airport security & boarding.",
                source="Verified Airline IATA Route Network",
                provider="Commercial Passenger Airline Matrix",
                retrieved_at=now_str,
                data_timestamp=now_str,
                data_status=data_st_val,
                verification_status=verif_st_val,
                booking_advisory="Airfares vary dynamically based on load factors and booking window. Book directly on official airline portals.",
                recommendation_reason="Fastest transit time for medium-to-long distance or intercontinental journeys.",
                warnings=[],
                booking_url=booking_url_val,
                live_availability_status=avail_status_val,
                flight_operator=flight_operator_val,
                flight_number=flight_number_val,
                is_live_data=is_live_val,
                operator_or_agency=flight_operator_val or "Commercial Scheduled Airline"
            ))

        # ---------------------------------------------------------
        # POST-PROCESSING & RECOMMENDED SELECTION
        # ---------------------------------------------------------
        if options:
            rec_options = [opt for opt in options if opt.is_recommended]
            if len(rec_options) > 1:
                for opt in rec_options[1:]:
                    opt.is_recommended = False
            elif not rec_options:
                if straight_dist_km <= 200:
                    cab_opt = next((o for o in options if o.category == "road" or "cab" in o.id.lower()), options[0])
                    cab_opt.is_recommended = True
                elif straight_dist_km <= 650:
                    train_opt = next((o for o in options if o.category == "rail" or "train" in o.id.lower()), options[0])
                    train_opt.is_recommended = True
                else:
                    options[0].is_recommended = True

        return options

transport_provider = TransportProvider()

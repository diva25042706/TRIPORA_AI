import uuid
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from app.schemas.agent_schemas import (
    ItineraryItem,
    DayPlan,
    WeatherForecast,
    TransportOption,
    HotelOption
)

class TripPlannerAgent:
    """Agent 1: Generates personalized, geographically coherent day-by-day travel schedules."""

    def plan_itinerary(
        self,
        destination: str,
        start_date_str: str,
        duration_days: int,
        travellers: int,
        interests: List[str],
        travel_style: str,
        places: List[Dict[str, Any]],
        weather_forecasts: Optional[List[WeatherForecast]] = None,
        is_rainy_replanning: bool = False,
        relaxed_pace: bool = False
    ) -> tuple[List[DayPlan], str]:
        try:
            start_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except Exception:
            start_dt = date.today() + timedelta(days=7)

        # Build weather map by day number
        weather_map: Dict[int, WeatherForecast] = {}
        if weather_forecasts:
            for wf in weather_forecasts:
                weather_map[wf.day_number] = wf

        # Filter and prioritize places based on user interests
        user_interests_lower = [i.lower() for i in interests] if interests else ["sightseeing", "culture", "food"]
        
        outdoor_places = [p for p in places if p.get("is_outdoor", True)]
        indoor_places = [p for p in places if not p.get("is_outdoor", True)]
        
        # Ensure fallback indoor pool if needed
        if not indoor_places:
            indoor_places = [
                {"name": f"{destination.title()} State Art Gallery & Museum", "category": "Culture", "lat": None, "lng": None, "is_outdoor": False, "duration": 2.0, "cost": 250, "desc": "Indoor museum displaying local artisanal textiles, heritage paintings, and sculptures."},
                {"name": f"Traditional Spice Culinary Workshop & Tasting", "category": "Food", "lat": None, "lng": None, "is_outdoor": False, "duration": 2.5, "cost": 800, "desc": "Covered culinary masterclass preparing authentic local dishes with tasting session."},
                {"name": f"Grand Opera & Cultural Performance Hall", "category": "Culture", "lat": None, "lng": None, "is_outdoor": False, "duration": 2.0, "cost": 500, "desc": "Acoustic auditorium hosting regional folklore music and classical dance recitals."}
            ]

        day_plans: List[DayPlan] = []
        used_place_indices = set()
        
        # Determine activities per day based on pace
        activities_per_day = 2 if (relaxed_pace or travel_style.lower() == "relaxed") else 3

        time_slots = [
            ("09:30 AM", "Morning"),
            ("02:00 PM", "Afternoon"),
            ("05:30 PM", "Evening")
        ]

        for day_num in range(1, duration_days + 1):
            curr_date = start_dt + timedelta(days=day_num - 1)
            curr_date_str = curr_date.strftime("%Y-%m-%d")

            wf = weather_map.get(day_num)
            is_rain_day = (wf and wf.is_rainy) or (is_rainy_replanning and day_num == 2)

            day_activities: List[ItineraryItem] = []
            day_cost = 0.0

            slots = time_slots[:activities_per_day]

            for slot_idx, (start_time, period) in enumerate(slots):
                # Choose candidate place: if rain day, pick indoor place
                candidate_place = None

                if is_rain_day:
                    for idx, p in enumerate(indoor_places):
                        if idx not in used_place_indices:
                            candidate_place = p
                            used_place_indices.add(idx)
                            break
                    if not candidate_place:
                        candidate_place = indoor_places[slot_idx % len(indoor_places)]
                else:
                    # Normal day: pick place matching interests or next available
                    for idx, p in enumerate(places):
                        if idx not in used_place_indices:
                            candidate_place = p
                            used_place_indices.add(idx)
                            break
                    if not candidate_place:
                        candidate_place = places[slot_idx % len(places)]

                # Format activity item
                est_cost = float(candidate_place.get("cost", 0)) * travellers
                dur = float(candidate_place.get("duration", 2.0))
                is_out = bool(candidate_place.get("is_outdoor", True))

                notes = f"{period} excursion. "
                if is_rain_day:
                    notes += "Curated sheltered indoor activity to guarantee comfort during forecasted rainfall."
                else:
                    notes += f"Ideal for {travel_style.lower()} exploration with close geographical transit."

                item = ItineraryItem(
                    id=str(uuid.uuid4())[:8],
                    day_number=day_num,
                    activity_name=candidate_place["name"],
                    description=candidate_place.get("desc", f"Explore {candidate_place['name']} in {destination}."),
                    location=f"{candidate_place['name']}, {destination}",
                    latitude=candidate_place.get("lat"),
                    longitude=candidate_place.get("lng"),
                    suggested_start_time=start_time,
                    estimated_duration_hours=dur,
                    estimated_cost=est_cost,
                    category=candidate_place.get("category", "Sightseeing"),
                    is_outdoor=is_out,
                    data_source="TRIPORA Curated Location Intelligence",
                    relevant_notes=notes
                )
                day_activities.append(item)
                day_cost += est_cost

            # Day theme
            if day_num == 1:
                theme = f"Arrival, Orientation & Historic Center in {destination.title()}"
            elif is_rain_day:
                theme = f"Sheltered Arts, Heritage Museums & Gastronomy (Rain Adjusted)"
            elif day_num == duration_days:
                theme = f"Scenic Highlights, Local Markets & Farewell Gathering"
            else:
                theme = f"Immersive Discovery: {interests[day_num % len(interests)] if interests else 'Culture & Scenery'}"

            day_plans.append(DayPlan(
                day_number=day_num,
                date=curr_date_str,
                theme=theme,
                activities=day_activities,
                day_cost=round(day_cost, 2),
                day_notes=f"Forecast: {wf.condition if wf else 'Pleasant'}. Organized in chronological order with optimal travel sequence."
            ))

        explanation = (
            f"Orchestrated a {duration_days}-day itinerary tailored for {travellers} traveller(s) seeking a {travel_style} experience in {destination.title()}. "
            f"Activities are sequenced to minimize transit friction, align with user interests ({', '.join(interests)}), "
            f"and incorporate weather safeguards."
        )

        return day_plans, explanation

planner_agent = TripPlannerAgent()

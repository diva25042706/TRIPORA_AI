import pytest
from app.agents.planner_agent import planner_agent
from app.schemas.agent_schemas import WeatherForecast

def test_planner_creates_requested_days():
    """Verify that planner produces exact day count with sequential items."""
    places = [
        {"name": "Landmark A", "category": "Culture", "lat": 15.1, "lng": 74.1, "is_outdoor": True, "duration": 2.0, "cost": 100},
        {"name": "Landmark B", "category": "Food", "lat": 15.2, "lng": 74.2, "is_outdoor": True, "duration": 1.5, "cost": 200},
        {"name": "Landmark C", "category": "Nature", "lat": 15.3, "lng": 74.3, "is_outdoor": True, "duration": 2.5, "cost": 0},
    ]

    days, explanation = planner_agent.plan_itinerary(
        destination="Goa",
        start_date_str="2026-11-15",
        duration_days=3,
        travellers=2,
        interests=["Culture", "Food"],
        travel_style="Balanced",
        places=places
    )

    assert len(days) == 3
    assert days[0].day_number == 1
    assert days[1].day_number == 2
    assert days[2].day_number == 3
    assert len(days[0].activities) > 0
    assert "Goa" in explanation

def test_planner_rain_adaptation():
    """Verify that rain flags cause indoor substitution."""
    places = [
        {"name": "Sunny Beach", "category": "Nature", "lat": 15.1, "lng": 74.1, "is_outdoor": True, "duration": 2.0, "cost": 0},
    ]
    wf = [
        WeatherForecast(
            date="2026-11-15", day_number=1, condition="Heavy Rain", temp_high_c=24, temp_low_c=20,
            precipitation_chance=90, is_rainy=True, is_outdoor_suitable=False,
            risk_assessment="Rain", suggested_alternatives=[], affected_activities=[],
            data_source="Test", freshness="Live"
        )
    ]

    days, _ = planner_agent.plan_itinerary(
        destination="Goa",
        start_date_str="2026-11-15",
        duration_days=1,
        travellers=1,
        interests=["Culture"],
        travel_style="Balanced",
        places=places,
        weather_forecasts=wf
    )

    # All activities on rainy day should be indoor or sheltered
    for act in days[0].activities:
        assert act.is_outdoor is False or "sheltered" in act.relevant_notes.lower()

@pytest.mark.asyncio
async def test_tamil_nadu_districts_catalog_resolution():
    """Verify that Tamil Nadu districts and popular aliases resolve verified POIs and coordinates."""
    from app.providers.geo_places_provider import geo_places_provider
    from app.providers.transport_provider import LOCATION_COORDS

    # Test direct district name
    madurai_info = await geo_places_provider.get_destination_info("Madurai")
    assert madurai_info["is_curated"] is True
    assert "Meenakshi Amman Temple" in [p["name"] for p in madurai_info["places"]]
    assert 9.0 < madurai_info["latitude"] < 10.5

    # Test alias resolution (e.g. Ooty -> Nilgiris)
    ooty_info = await geo_places_provider.get_destination_info("Ooty")
    assert ooty_info["is_curated"] is True
    assert any("Botanical" in p["name"] for p in ooty_info["places"])

    # Test coordinate registration for intercity transport
    assert "chennai" in LOCATION_COORDS
    assert "nilgiris" in LOCATION_COORDS
    assert "ooty" in LOCATION_COORDS
    assert "thanjavur" in LOCATION_COORDS


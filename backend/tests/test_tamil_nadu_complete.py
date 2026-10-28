import pytest
from httpx import AsyncClient, ASGITransport
from datetime import date, timedelta
from main import app
from app.providers.tamil_nadu_complete_data import TAMIL_NADU_ALL_DISTRICTS_DATA
from app.providers.geo_places_provider import (
    TN_DISTRICT_ALIASES,
    resolve_destination_district,
    get_places_for_destination,
    geo_places_provider,
)
from app.agents.planner_agent import planner_agent

EXPECTED_38_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
    "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram",
    "Kanniyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
    "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
    "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi",
    "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur",
    "Vellore", "Viluppuram", "Virudhunagar"
]

def test_all_38_districts_present_and_curated():
    """Verify all 38 districts exist with >= 4 verified attractions and valid schemas."""
    assert len(TAMIL_NADU_ALL_DISTRICTS_DATA) == 38, f"Expected 38 districts, got {len(TAMIL_NADU_ALL_DISTRICTS_DATA)}"
    
    total_attractions = 0
    for district in EXPECTED_38_DISTRICTS:
        dist_key = district.lower()
        assert dist_key in TAMIL_NADU_ALL_DISTRICTS_DATA, f"Missing district: {dist_key}"
        dist_data = TAMIL_NADU_ALL_DISTRICTS_DATA[dist_key]
        places = dist_data["places"]
        assert len(places) >= 4, f"District {district} has fewer than 4 places: {len(places)}"
        total_attractions += len(places)

        for p in places:
            # Required fields
            assert "id" in p and p["id"], f"Missing id in place {p}"
            assert "name" in p and p["name"], f"Missing name in place {p}"
            assert "category" in p and p["category"], f"Missing category in place {p}"
            assert "lat" in p and isinstance(p["lat"], (int, float)), f"Invalid lat in {p}"
            assert "lng" in p and isinstance(p["lng"], (int, float)), f"Invalid lng in {p}"
            assert "address" in p and p["address"], f"Missing address in place {p}"
            assert "opening_hours" in p, f"Missing opening_hours in place {p}"
            assert "closed_days" in p, f"Missing closed_days in place {p}"
            assert "ticket_price_inr" in p and isinstance(p["ticket_price_inr"], (int, float)), f"Invalid price in {p}"
            assert "visit_duration_hours" in p and isinstance(p["visit_duration_hours"], (int, float)), f"Invalid duration in {p}"
            assert "is_outdoor" in p and isinstance(p["is_outdoor"], bool), f"Invalid is_outdoor in {p}"
            assert "source_attribution" in p, f"Missing source_attribution in place {p}"

            # Coordinates in Tamil Nadu bounding box
            assert 8.0 <= p["lat"] <= 13.6, f"Lat {p['lat']} out of bounds for {p['name']} in {district}"
            assert 76.2 <= p["lng"] <= 80.5, f"Lng {p['lng']} out of bounds for {p['name']} in {district}"

    # Verify overall dataset size
    assert total_attractions >= 220, f"Expected at least 220 attractions across TN, got {total_attractions}"

def test_town_and_landmark_alias_resolution():
    """Verify alias mapping resolves towns and tourist spots to their respective districts."""
    test_cases = [
        ("Ooty", "nilgiris"),
        ("Udhagamandalam", "nilgiris"),
        ("Coonoor", "nilgiris"),
        ("Kodaikanal", "dindigul"),
        ("Palani", "dindigul"),
        ("Rameswaram", "ramanathapuram"),
        ("Dhanushkodi", "ramanathapuram"),
        ("Mahabalipuram", "chengalpattu"),
        ("Mamallapuram", "chengalpattu"),
        ("Srirangam", "tiruchirappalli"),
        ("Trichy", "tiruchirappalli"),
        ("Tanjore", "thanjavur"),
        ("Kumbakonam", "thanjavur"),
        ("Kovalam", "chengalpattu"),
        ("Yelagiri", "tirupathur"),
        ("Hogenakkal", "dharmapuri"),
        ("Kolli Hills", "namakkal"),
        ("Chettinad", "sivaganga"),
        ("Karaikudi", "sivaganga"),
        ("Megamalai", "theni"),
        ("Pichavaram", "cuddalore"),
        ("Chidambaram", "cuddalore"),
        ("Gingee", "viluppuram"),
        ("Velankanni", "nagapattinam"),
        ("Nagore", "nagapattinam"),
        ("Tranquebar", "mayiladuthurai"),
        ("Tharangambadi", "mayiladuthurai"),
        ("Courtallam", "tenkasi"),
        ("Gangaikonda Cholapuram", "ariyalur"),
        ("Yercaud", "salem"),
        ("Mettur", "salem"),
        ("Tiruchendur", "thoothukudi"),
        ("Tuticorin", "thoothukudi"),
        ("Pollachi", "coimbatore"),
        ("Valparai", "coimbatore"),
        ("Bhavani", "erode"),
        ("Tiruthani", "tiruvallur"),
        ("Pulicat", "tiruvallur"),
        ("Mannargudi", "tiruvarur"),
        ("Arcot", "ranipet"),
    ]

    for town, expected_district in test_cases:
        res = resolve_destination_district(town)
        assert res == expected_district, f"Expected '{town}' -> '{expected_district}', got '{res}'"

    # Non-TN cities should return None
    assert resolve_destination_district("Paris") is None
    assert resolve_destination_district("Tokyo") is None
    assert resolve_destination_district("Goa") is None

@pytest.mark.asyncio
async def test_places_api_districts_endpoint():
    """Verify /api/v1/places/districts returns all 38 districts with counts."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/v1/places/districts")
        assert resp.status_code == 200
        districts = resp.json()
        assert len(districts) == 38
        for d in districts:
            assert "district" in d
            assert "attraction_count" in d
            assert d["attraction_count"] >= 4
            assert "popular_attractions" in d
            assert len(d["popular_attractions"]) >= 2

@pytest.mark.asyncio
async def test_places_api_resolve_endpoint():
    """Verify /api/v1/places/resolve endpoint maps aliases correctly."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp_ooty = await ac.get("/api/v1/places/resolve?query=Ooty")
        assert resp_ooty.status_code == 200
        d_ooty = resp_ooty.json()
        assert d_ooty["is_tamil_nadu"] is True
        assert d_ooty["district"] == "nilgiris"
        assert d_ooty["total_attractions"] >= 6

        resp_paris = await ac.get("/api/v1/places/resolve?query=Paris")
        assert resp_paris.status_code == 200
        d_paris = resp_paris.json()
        assert d_paris["is_tamil_nadu"] is False

@pytest.mark.asyncio
@pytest.mark.parametrize("destination,days", [
    ("Chennai", 3),
    ("Coimbatore", 3),
    ("Madurai", 3),
    ("Ooty", 3),
    ("Thanjavur", 3),
    ("Kanyakumari", 3),
    ("Tiruvannamalai", 3),
    ("Chennai", 5),
    ("Madurai", 4),
])
async def test_multi_day_itinerary_unique_places(destination: str, days: int):
    """
    Core acceptance test: Multi-day itineraries must NEVER repeat attractions across days.
    Total unique place names must equal the total number of place slots generated.
    """
    start_dt = date(2026, 11, 10)

    dest_info = await geo_places_provider.get_destination_info(destination)
    places = dest_info.get("places", [])
    assert len(places) > 0, f"No places retrieved for {destination}"

    day_plans, explanation = planner_agent.plan_itinerary(
        destination=destination,
        start_date_str=start_dt.isoformat(),
        duration_days=days,
        travellers=2,
        interests=["Culture", "Sightseeing", "Nature"],
        travel_style="Balanced",
        places=places
    )

    assert len(day_plans) == days, f"Expected {days} days, got {len(day_plans)}"

    all_activities = []
    all_place_ids = []

    for day_plan in day_plans:
        assert day_plan.day_number >= 1
        assert day_plan.date
        activities = day_plan.activities
        assert len(activities) >= 2, f"Day {day_plan.day_number} has fewer than 2 activities"

        for act in activities:
            name = act.activity_name
            assert name, f"Activity missing name in day {day_plan.day_number}"
            all_activities.append(name.strip().lower())

    # ZERO REPETITION CHECK
    unique_activities = set(all_activities)
    assert len(all_activities) == len(unique_activities), (
        f"Duplicate activities found in {destination} ({days} days)! "
        f"Total: {len(all_activities)}, Unique: {len(unique_activities)}. "
        f"Duplicates: {[act for act in all_activities if all_activities.count(act) > 1]}"
    )

@pytest.mark.asyncio
async def test_non_tamil_nadu_destinations_remain_functional():
    """Ensure worldwide destinations (Goa, Paris, Tokyo) continue to work properly."""
    start_dt = date(2026, 12, 1)

    dest_info = await geo_places_provider.get_destination_info("Goa")
    places = dest_info.get("places", [])
    assert len(places) > 0

    day_plans, _ = planner_agent.plan_itinerary(
        destination="Goa",
        start_date_str=start_dt.isoformat(),
        duration_days=3,
        travellers=2,
        interests=["Beaches", "Relaxation"],
        travel_style="Balanced",
        places=places
    )
    assert len(day_plans) == 3
    goa_activities = [act.activity_name.strip().lower() for d in day_plans for act in d.activities]
    assert len(goa_activities) == len(set(goa_activities)), (
        f"Duplicate activities in Goa: {[act for act in goa_activities if goa_activities.count(act) > 1]}"
    )

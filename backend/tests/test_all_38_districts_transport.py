import pytest
from app.agents.transport_agent import transport_agent
from app.providers.transport_provider import transport_provider
from app.providers.tamil_nadu_districts import TAMIL_NADU_DISTRICTS
from app.providers.infrastructure_data import (
    VERIFIED_AIRPORTS,
    VERIFIED_STATIONS,
    VERIFIED_BUS_TERMINALS,
    TAMIL_NADU_COMMERCIAL_AIRPORTS,
    get_verified_airport,
    get_verified_station,
    get_verified_bus_terminal,
    get_nearest_commercial_airport
)

ALL_38_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
    "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram",
    "Kanniyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
    "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
    "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi",
    "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli",
    "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur",
    "Vellore", "Viluppuram", "Virudhunagar"
]

SIX_CERTIFIED_AIRPORTS = {"chennai", "coimbatore", "madurai", "tiruchirappalli", "salem", "thoothukudi"}

REQUIRED_14_ROUTES = [
    ("Chennai", "Tiruvannamalai"),
    ("Chennai", "Vellore"),
    ("Chennai", "Kancheepuram"),
    ("Chennai", "Chengalpattu"),
    ("Chennai", "Coimbatore"),
    ("Chennai", "Madurai"),
    ("Chennai", "Tiruchirappalli"),
    ("Chennai", "Salem"),
    ("Chennai", "Thanjavur"),
    ("Chennai", "Tirunelveli"),
    ("Coimbatore", "Ooty"),
    ("Madurai", "Rameswaram"),
    ("Tiruchirappalli", "Thanjavur"),
    ("Salem", "Yercaud")
]

def test_all_38_districts_present_in_catalog():
    """Verify all 38 Tamil Nadu districts are registered and distinct."""
    assert len(ALL_38_DISTRICTS) == 38
    for dist in ALL_38_DISTRICTS:
        key = dist.lower()
        assert key in TAMIL_NADU_DISTRICTS or dist in TAMIL_NADU_DISTRICTS

def test_all_38_districts_have_verified_station_and_bus_terminal():
    """Verify that every district maps to a verified railway station/railhead and bus terminal."""
    for dist in ALL_38_DISTRICTS:
        station = get_verified_station(dist)
        bus_term = get_verified_bus_terminal(dist)
        assert station is not None, f"District {dist} missing railway station/railhead mapping"
        assert "code" in station, f"District {dist} station missing code"
        assert bus_term is not None, f"District {dist} missing bus terminal"
        assert len(bus_term) > 3, f"District {dist} bus terminal name too short"

def test_six_certified_airports_strictly_enforced():
    """Verify Tamil Nadu commercial airport certification is strictly limited to 6 active hubs."""
    assert len(TAMIL_NADU_COMMERCIAL_AIRPORTS) == 6
    airport_codes = set(TAMIL_NADU_COMMERCIAL_AIRPORTS.keys())
    assert airport_codes == {"MAA", "CJB", "IXM", "TRZ", "SXV", "TCR"}

    # Non-airport districts must return None from get_verified_airport
    non_airport_sample = ["Tiruvannamalai", "Kancheepuram", "Vellore", "Yercaud", "Ooty", "Thanjavur", "Dindigul"]
    for city in non_airport_sample:
        apt = get_verified_airport(city)
        assert apt is None, f"{city} must not have a commercial airport"

def test_nearest_commercial_airport_resolution():
    """Verify nearest commercial airport helper returns verified airport and realistic road distance."""
    # Tiruvannamalai -> nearest commercial airport (SXV ~140-160 km or MAA ~165-200 km)
    tvm_apt, tvm_dist = get_nearest_commercial_airport(12.2253, 79.0747)
    assert tvm_apt is not None
    assert tvm_apt["airport_code"] in ["SXV", "MAA", "TRZ"]
    assert 120 <= tvm_dist <= 220

    # Thanjavur -> nearest TRZ (~55-65 km)
    tj_apt, tj_dist = get_nearest_commercial_airport(10.7870, 79.1378)
    assert tj_apt is not None
    assert tj_apt["airport_code"] == "TRZ"
    assert 40 <= tj_dist <= 80

def test_required_14_routes_coverage_and_integrity():
    """Verify all 14 required prompt routes return valid options with zero empty results."""
    for orig, dest in REQUIRED_14_ROUTES:
        options, recommended = transport_agent.evaluate_transportation(orig, dest, travellers=2)
        assert len(options) >= 2, f"Route {orig} -> {dest} returned fewer than 2 options"
        assert recommended is not None, f"Route {orig} -> {dest} missing recommended option"
        assert recommended.is_recommended is True

        categories = {opt.category for opt in options}
        # Every route must have road and bus
        assert "road" in categories, f"Route {orig} -> {dest} missing road"
        assert "bus" in categories, f"Route {orig} -> {dest} missing bus"

        # Check booking links and distance
        for opt in options:
            assert opt.distance_km > 0, f"Distance must be positive for {orig} -> {dest}"
            assert opt.duration_hours > 0, f"Duration must be positive for {orig} -> {dest}"
            assert opt.estimated_cost > 0, f"Cost must be positive for {orig} -> {dest}"
            if opt.category == "road":
                assert "maps" in opt.booking_url or "maps" in (opt.directions_url or "")
            elif opt.category == "rail":
                assert "irctc" in opt.booking_url.lower()
            elif opt.category == "bus":
                assert "tnstc" in opt.booking_url.lower()

def test_route_salem_to_yercaud_mountain_ghat():
    """Verify Salem -> Yercaud is recognized as a scenic ghat road with realistic distance and zero fake train."""
    options, rec = transport_agent.evaluate_transportation("Salem", "Yercaud")
    categories = [opt.category for opt in options]
    assert "road" in categories
    assert "bus" in categories
    assert "flight" not in categories
    assert "rail" not in categories, "Yercaud hilltop has no railway line; direct rail must not exist"

    road_opt = next(opt for opt in options if opt.category == "road")
    assert 20 <= road_opt.distance_km <= 40, "Ghat road distance must reflect 20-hairpin bend SH 188 (~27-32 km)"
    assert road_opt.duration_hours >= 1.0, "Mountain driving duration must reflect ghat speed"

def test_route_chennai_to_tiruvannamalai_rail_and_road():
    """Verify Chennai -> Tiruvannamalai provides verified train, bus, cab, and strictly zero flights."""
    options, rec = transport_agent.evaluate_transportation("Chennai", "Tiruvannamalai")
    categories = [opt.category for opt in options]
    assert "rail" in categories
    assert "bus" in categories
    assert "road" in categories
    assert "flight" not in categories, "Tiruvannamalai has no commercial airport; flights must be strictly excluded"

    train_opt = next(opt for opt in options if opt.category == "rail")
    assert "tiruvannamalai" in train_opt.mode.lower() or "16115" in (train_opt.train_number or "")
    assert "irctc" in train_opt.booking_url.lower()

def test_route_chennai_to_coimbatore_flight_rail_bus_cab():
    """Verify Chennai -> Coimbatore (commercial airport pair) returns all 4 categories."""
    options, rec = transport_agent.evaluate_transportation("Chennai", "Coimbatore")
    categories = {opt.category for opt in options}
    assert categories == {"road", "bus", "rail", "flight"}

    flight_opt = next(opt for opt in options if opt.category == "flight")
    assert "indigo" in (flight_opt.flight_operator or "").lower() or "air india" in (flight_opt.flight_operator or "").lower()
    assert flight_opt.duration_hours <= 3.5

def test_all_38_districts_from_chennai_never_return_zero():
    """Verify sweeping across all 38 districts from Chennai never returns zero results."""
    for dist in ALL_38_DISTRICTS:
        if dist.lower() == "chennai":
            continue
        options, recommended = transport_agent.evaluate_transportation("Chennai", dist)
        assert len(options) >= 2, f"Chennai -> {dist} returned {len(options)} options, expected at least 2"
        assert recommended is not None

def test_cross_district_hub_connectivity():
    """Verify key regional hubs connect to various districts without zero results."""
    pairs = [
        ("Coimbatore", "Madurai"),
        ("Tiruchirappalli", "Salem"),
        ("Madurai", "Tirunelveli"),
        ("Salem", "Dharmapuri"),
        ("Erode", "Tiruppur"),
        ("Thanjavur", "Nagapattinam"),
        ("Vellore", "Tirupathur"),
        ("Dindigul", "Theni")
    ]
    for o, d in pairs:
        opts, rec = transport_agent.evaluate_transportation(o, d)
        assert len(opts) >= 2, f"Hub route {o} -> {d} returned {len(opts)} options"
        assert rec is not None

import pytest
from app.providers.transport_provider import transport_provider
from app.agents.transport_agent import transport_agent
from app.agents.budget_agent import budget_agent
from app.schemas.agent_schemas import TransportOption, DayPlan

# ==============================================================================
# SECTION 10 AUTOMATED REGRESSION TESTS FOR TRANSPORTATION AGENT & ROUTING
# ==============================================================================

def test_a_chennai_to_tiruvannamalai_regression():
    """
    Test A: Chennai to Tiruvannamalai
    - Road travel (cab/taxi) is recommended and present.
    - Bus and train appear with supported verification status.
    - FLIGHT MUST STRICTLY NOT BE DISPLAYED OR RECOMMENDED (Tiruvannamalai has no commercial airport).
    """
    options, recommended = transport_agent.evaluate_transportation(
        origin="Chennai",
        destination="Tiruvannamalai",
        travellers=2,
        preferred_mode="Best Value",
        budget=40000.0,
        currency="INR"
    )

    assert len(options) >= 2, "Should return overland options (Cab, Bus, Train)"
    
    # Verify modes present
    modes = [opt.mode.lower() for opt in options]
    assert any("cab" in m or "taxi" in m for m in modes), "Road / cab must be present"
    assert any("bus" in m for m in modes), "Intercity bus must be present"
    assert any("train" in m for m in modes), "Railway express must be present"

    # STRICT CHECK: Absolutely NO flight on Chennai -> Tiruvannamalai
    assert not any("flight" in m or "airline" in m or "plane" in m or "aviation" in m for m in modes), "CRITICAL: Flight must NOT be generated for Chennai -> Tiruvannamalai!"
    assert recommended is not None
    assert "flight" not in recommended.mode.lower(), "Recommended option cannot be a flight!"
    
    # Distance should reflect road/overland (~180-240 km), not straight line alone
    cab_opt = next(o for o in options if "cab" in o.mode.lower())
    assert 170.0 <= cab_opt.distance_km <= 250.0
    assert 3.0 <= cab_opt.duration_hours <= 5.5

def test_b_chennai_to_madurai_multimodal():
    """
    Test B: Chennai to Madurai
    - Both Chennai (MAA) and Madurai (IXM) have active commercial airports.
    - Road, train, and flight options are evaluated independently.
    - Flight is eligible and includes airport IATA codes (MAA, IXM).
    - Train (Tejas/Vaigai) is eligible.
    """
    options, recommended = transport_agent.evaluate_transportation(
        origin="Chennai",
        destination="Madurai",
        travellers=2,
        preferred_mode="Fastest",
        budget=60000.0,
        currency="INR"
    )

    modes = [opt.mode.lower() for opt in options]
    assert any("flight" in m for m in modes), "Commercial flight should be eligible between MAA and IXM"
    assert any("train" in m for m in modes), "Train should be eligible between Chennai and Madurai"
    assert any("bus" in m or "cab" in m for m in modes), "Overland road/bus should be eligible"

    flight_opt = next(o for o in options if "flight" in o.mode.lower())
    assert "MAA" in flight_opt.origin_station_or_airport
    assert "IXM" in flight_opt.destination_station_or_airport
    assert flight_opt.duration_hours < 4.0  # Fast transit
    assert flight_opt.is_recommended is True  # Preferred was "Fastest"

def test_c_chennai_to_london_international():
    """
    Test C: Chennai to London
    - International flight search returns valid commercial flight.
    - Road, bus, and train are excluded (intercontinental ocean separation).
    """
    options, recommended = transport_agent.evaluate_transportation(
        origin="Chennai",
        destination="London",
        travellers=1,
        preferred_mode="Best Value",
        budget=150000.0,
        currency="INR"
    )

    assert len(options) >= 1
    modes = [opt.mode.lower() for opt in options]
    assert all("flight" in m for m in modes), "Only flights are physically eligible for Chennai to London"
    assert not any("cab" in m or "bus" in m or "train" in m for m in modes)

    flight_opt = options[0]
    assert "LHR" in flight_opt.destination_station_or_airport or "Heathrow" in flight_opt.destination_station_or_airport
    assert flight_opt.distance_km > 7000.0
    assert flight_opt.is_recommended is True

def test_d_missing_provider_credentials_graceful_handling():
    """
    Test D: Missing provider credentials / offline fallback
    - Application continues functioning with verified infrastructure models.
    - Data is marked clearly as verified_static or estimated, never as live API claim without real auth.
    - No fabricated booking confirmation or fake flight numbers.
    """
    options = transport_provider.get_transport_options(
        origin="Chennai",
        destination="Coimbatore",
        travellers=2
    )

    assert len(options) > 0
    for opt in options:
        assert opt.data_status in ["verified_static", "estimated"]
        assert opt.verification_status in ["verified", "estimated"]
        assert "confirmed booking" not in opt.booking_advisory.lower()
        assert opt.estimated_cost > 0

def test_e_invalid_provider_response_rejection():
    """
    Test E: Invalid provider response
    - Rejects empty, missing, or identical origin and destination.
    """
    # Identical origin and destination
    same_opts = transport_provider.get_transport_options(origin="Chennai", destination="Chennai")
    assert same_opts == [], "Must reject identical origin and destination"

    # Missing origin or destination
    empty_opts = transport_provider.get_transport_options(origin="", destination="Madurai")
    assert empty_opts == [], "Must reject empty origin"

def test_f_empty_provider_results_no_fabrication():
    """
    Test F: Empty provider results
    - When unknown coordinates or impossible route occurs, returns clean empty state.
    - Does NOT fabricate replacement flights.
    """
    options = transport_provider.get_transport_options(
        origin="NonExistentCityXYZ123",
        destination="NowhereCityABC987"
    )
    assert options == [], "Must return empty list for unverified destinations rather than inventing fake data"

def test_g_budget_integration_reconciliation():
    """
    Test G: Budget integration
    - Do not include invalid transport options in the trip budget.
    - Ensure transport costs reconcile with the overall budget.
    """
    # Get Chennai to Tiruvannamalai options
    options, recommended = transport_agent.evaluate_transportation(
        origin="Chennai",
        destination="Tiruvannamalai",
        travellers=2,
        budget=50000.0
    )

    assert recommended is not None
    assert "flight" not in recommended.mode.lower()

    # Pass recommended transport into BudgetOptimizationAgent
    budget_breakdown = budget_agent.calculate_budget(
        total_budget=50000.0,
        travellers=2,
        duration_days=3,
        selected_transport=recommended,
        selected_hotel=None,
        days=[],
        currency="INR"
    )

    # Check that transport cost category exactly matches recommended transport cost
    trans_cat = next(c for c in budget_breakdown.categories if c.category == "Transportation")
    assert trans_cat.amount == recommended.estimated_cost
    assert budget_breakdown.total_estimated_cost > 0
    
    # Grand total must reconcile with category sum
    cat_sum = sum(c.amount for c in budget_breakdown.categories)
    assert round(cat_sum, 2) == round(budget_breakdown.total_estimated_cost, 2)

def test_h_replanning_route_isolation():
    """
    Test H: Replanning
    - Changing destination from Tiruvannamalai to London produces completely different transport modes.
    - Tiruvannamalai results have NO flights; London results have ONLY flights.
    - Old results are not cached or leaked across route lookups.
    """
    opts_tnm, _ = transport_agent.evaluate_transportation("Chennai", "Tiruvannamalai")
    opts_lon, _ = transport_agent.evaluate_transportation("Chennai", "London")

    assert not any("flight" in o.mode.lower() for o in opts_tnm)
    assert all("flight" in o.mode.lower() for o in opts_lon)
    assert len(opts_tnm) != len(opts_lon)

def test_i_chennai_to_coimbatore_verified_services():
    """
    Test I: Chennai to Coimbatore corridor
    - Verified flight (MAA -> CJB) with real airline operator and booking url.
    - Verified train (MAS -> CBE) with Vande Bharat / Kovai Express and IRCTC booking url.
    - Road and bus transit present.
    """
    options, recommended = transport_agent.evaluate_transportation("Chennai", "Coimbatore", travellers=2)
    assert len(options) >= 3

    # Flight verification
    flight_opt = next((o for o in options if "flight" in o.mode.lower()), None)
    assert flight_opt is not None, "Flight must be present between Chennai and Coimbatore"
    assert "MAA" in flight_opt.origin_station_or_airport
    assert "CJB" in flight_opt.destination_station_or_airport
    assert flight_opt.flight_operator is not None
    assert "indigo" in flight_opt.booking_url.lower() or "airline" in flight_opt.booking_url.lower()

    # Train verification
    train_opt = next((o for o in options if "train" in o.mode.lower()), None)
    assert train_opt is not None, "Train must be present between Chennai and Coimbatore"
    assert "MAS" in train_opt.origin_station_or_airport or "Central" in train_opt.origin_station_or_airport
    assert "CBE" in train_opt.destination_station_or_airport or "Coimbatore" in train_opt.destination_station_or_airport
    assert "20643" in train_opt.train_number or "12675" in train_opt.train_number or "Vande Bharat" in train_opt.train_name
    assert "irctc.co.in" in train_opt.booking_url

def test_j_chennai_to_tiruchirappalli_verified_services():
    """
    Test J: Chennai to Tiruchirappalli (Trichy) corridor
    - Verified flight (MAA -> TRZ).
    - Verified train (MS -> TPJ) with Vande Bharat #20605 / Pallavan Express #12605.
    - IRCTC booking link and official airline booking link present.
    """
    options, recommended = transport_agent.evaluate_transportation("Chennai", "Tiruchirappalli", travellers=1)
    
    flight_opt = next((o for o in options if "flight" in o.mode.lower()), None)
    assert flight_opt is not None
    assert "TRZ" in flight_opt.destination_station_or_airport

    train_opt = next((o for o in options if "train" in o.mode.lower()), None)
    assert train_opt is not None
    assert "TPJ" in train_opt.destination_station_or_airport or "Tiruchirappalli" in train_opt.destination_station_or_airport
    assert "20605" in train_opt.train_number or "12605" in train_opt.train_number or "Vande Bharat" in train_opt.train_name
    assert "irctc.co.in" in train_opt.booking_url

def test_k_chennai_to_salem_verified_services():
    """
    Test K: Chennai to Salem corridor
    - Scheduled regional UDAN flight (MAA -> SXV) via Alliance Air.
    - Express train (MAS -> SA) with Vande Bharat / Kovai / Yercaud Express.
    """
    options, recommended = transport_agent.evaluate_transportation("Chennai", "Salem", travellers=1)
    
    flight_opt = next((o for o in options if "flight" in o.mode.lower()), None)
    assert flight_opt is not None
    assert "SXV" in flight_opt.destination_station_or_airport
    assert "allianceair" in flight_opt.booking_url or "udan" in flight_opt.mode.lower() or "regional" in flight_opt.mode.lower() or "alliance" in str(flight_opt.flight_operator).lower()

    train_opt = next((o for o in options if "train" in o.mode.lower()), None)
    assert train_opt is not None
    assert "SA" in train_opt.destination_station_or_airport or "Salem" in train_opt.destination_station_or_airport
    assert "irctc.co.in" in train_opt.booking_url

def test_l_chennai_to_thoothukudi_verified_services():
    """
    Test L: Chennai to Thoothukudi (Tuticorin) corridor
    - Verified domestic passenger flight (MAA -> TCR).
    - Prestigious overnight Pearl City Superfast Express #12693 (MS -> TN).
    """
    options, recommended = transport_agent.evaluate_transportation("Chennai", "Thoothukudi", travellers=2)
    
    flight_opt = next((o for o in options if "flight" in o.mode.lower()), None)
    assert flight_opt is not None
    assert "TCR" in flight_opt.destination_station_or_airport
    assert "goindigo" in flight_opt.booking_url or "indigo" in str(flight_opt.flight_operator).lower()

    train_opt = next((o for o in options if "train" in o.mode.lower()), None)
    assert train_opt is not None
    assert "TN" in train_opt.destination_station_or_airport or "Tuticorin" in train_opt.destination_station_or_airport
    assert "12693" in train_opt.train_number or "Pearl City" in train_opt.train_name
    assert "irctc.co.in" in train_opt.booking_url

def test_m_tamil_nadu_38_districts_airport_isolation():
    """
    Test M: Rigorous check of 38 Tamil Nadu districts
    - The 6 certified commercial airports: Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem, Thoothukudi
    - Non-airport districts: Tiruvannamalai, Kodaikanal, Thanjavur, Rameswaram, Kanyakumari, Vellore, Cuddalore, Dharmapuri, etc.
    - NEVER generate flights to districts without verified commercial airports.
    """
    non_airport_districts = [
        "Tiruvannamalai",
        "Kodaikanal",
        "Thanjavur",
        "Rameswaram",
        "Kanyakumari",
        "Vellore",
        "Cuddalore",
        "Dharmapuri"
    ]

    for dest in non_airport_districts:
        opts, _ = transport_agent.evaluate_transportation("Chennai", dest)
        modes = [o.mode.lower() for o in opts]
        assert not any("flight" in m or "airline" in m or "plane" in m for m in modes), f"CRITICAL: Flight hallucinated for {dest} which has no commercial passenger airport!"
        # Must have overland options (Cab, Bus, or Train)
        assert any("cab" in m or "taxi" in m for m in modes)
        assert any("train" in m for m in modes)


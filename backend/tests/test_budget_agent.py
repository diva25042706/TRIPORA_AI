import pytest
from app.agents.budget_agent import budget_agent
from app.schemas.agent_schemas import DayPlan, ItineraryItem, TransportOption, HotelOption

def test_budget_reconciliation():
    """Verify deterministic financial arithmetic: categories must exactly sum to total cost."""
    items = [
        ItineraryItem(
            id="1", day_number=1, activity_name="Fort Excursion", description="Visit fort",
            location="Goa", suggested_start_time="09:30 AM", estimated_duration_hours=2.0,
            estimated_cost=400.0, category="Culture", is_outdoor=True, data_source="Test"
        ),
        ItineraryItem(
            id="2", day_number=1, activity_name="Beach Walk", description="Sunset beach",
            location="Goa", suggested_start_time="05:30 PM", estimated_duration_hours=1.5,
            estimated_cost=0.0, category="Nature", is_outdoor=True, data_source="Test"
        )
    ]
    days = [DayPlan(day_number=1, date="2026-11-10", theme="Heritage", activities=items, day_cost=400.0)]

    trans = TransportOption(
        id="t1", mode="Express Train", origin="Mumbai", destination="Goa",
        distance_km=550.0, duration_hours=8.0, price_range_low=1200.0, price_range_high=2400.0,
        estimated_cost=3600.0, currency="INR", is_recommended=True,
        recommendation_rationale="Value", source="Test", data_timestamp="2026",
        booking_advisory="Book early"
    )

    hotel = HotelOption(
        id="h1", name="Resort", location="North Goa", price_per_night=3500.0, total_price=7000.0,
        currency="INR", rating=4.5, amenities=["Pool"], distance_to_center_km=1.5,
        description="Resort", provider_source="Test", is_verified=True,
        availability_status="Available", ranking_rationale="Great"
    )

    budget_breakdown = budget_agent.calculate_budget(
        total_budget=50000.0,
        travellers=2,
        duration_days=3,
        selected_transport=trans,
        selected_hotel=hotel,
        days=days,
        currency="INR"
    )

    # Reconcile category sum with total estimated cost
    category_sum = sum(cat.amount for cat in budget_breakdown.categories)
    assert round(category_sum, 2) == round(budget_breakdown.total_estimated_cost, 2)
    assert budget_breakdown.budget_status == "Under Budget"
    assert budget_breakdown.remaining_budget > 0
    assert budget_breakdown.budget_deficit == 0.0
    assert budget_breakdown.cost_per_person == round(budget_breakdown.total_estimated_cost / 2, 2)

def test_over_budget_detection():
    """Verify that exceeding budget triggers deficit and status change."""
    budget_breakdown = budget_agent.calculate_budget(
        total_budget=5000.0,  # Very small budget
        travellers=2,
        duration_days=5,
        selected_transport=None,
        selected_hotel=None,
        days=[],
        currency="INR"
    )

    assert budget_breakdown.budget_status == "Over Budget"
    assert budget_breakdown.budget_deficit > 0
    assert len(budget_breakdown.cost_saving_recommendations) > 0

import pytest
from app.workflows.trip_workflow import trip_graph
from app.schemas.agent_schemas import FullTripPlan

@pytest.mark.asyncio
async def test_langgraph_full_trip_workflow():
    """Verify that LangGraph executes all specialized agents in the workflow graph."""
    initial_state = {
        "trip_id": "test-uuid-12345",
        "title": "Test 3-Day Goa Tour",
        "origin": "Mumbai",
        "destination": "Goa",
        "start_date": "2026-11-20",
        "end_date": "2026-11-22",
        "duration_days": 3,
        "travellers": 2,
        "total_budget": 45000.0,
        "currency": "INR",
        "travel_style": "Balanced",
        "interests": ["Culture", "Food", "Sightseeing"],
        "accommodation_pref": "Hotel",
        "transport_pref": "Best Value",
        "agent_statuses": [],
        "replanning_attempts": 0,
        "max_replanning_attempts": 2
    }

    final_state = await trip_graph.ainvoke(initial_state)

    assert "final_trip_plan" in final_state
    plan: FullTripPlan = final_state["final_trip_plan"]
    assert plan.destination == "Goa"
    assert len(plan.days) == 3
    assert plan.budget.total_estimated_cost > 0
    assert len(plan.transports) > 0
    assert len(plan.hotels) > 0
    assert len(plan.weather_forecasts) == 3
    assert len(plan.safety_findings) > 0

    # Verify agent execution statuses are recorded
    agent_names = [s.agent_name for s in plan.agent_statuses]
    assert "Trip Planner Agent" in agent_names
    assert "Budget Optimization Agent" in agent_names
    assert "Transportation Agent" in agent_names
    assert "Hotel & Accommodation Agent" in agent_names
    assert "Weather Intelligence Agent" in agent_names
    assert "Travel Safety & Reliability Agent" in agent_names

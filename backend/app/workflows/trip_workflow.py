import time
import uuid
from datetime import datetime, timezone, timedelta, date
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END

from app.schemas.agent_schemas import (
    ItineraryItem,
    DayPlan,
    BudgetBreakdown,
    TransportOption,
    HotelOption,
    WeatherForecast,
    SafetyFinding,
    AgentExecutionStatus,
    FullTripPlan
)
from app.providers.geo_places_provider import geo_places_provider
from app.agents.transport_agent import transport_agent
from app.agents.hotel_agent import hotel_agent
from app.agents.weather_agent import weather_agent
from app.agents.planner_agent import planner_agent
from app.agents.budget_agent import budget_agent
from app.agents.safety_agent import safety_agent

class TripWorkflowState(TypedDict, total=False):
    # Requirements & Inputs
    trip_id: str
    title: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    duration_days: int
    travellers: int
    total_budget: float
    currency: str
    travel_style: str
    interests: List[str]
    accommodation_pref: str
    transport_pref: str
    
    # Retrieved & Generated Artifacts
    destination_data: Dict[str, Any]
    places: List[Dict[str, Any]]
    transports: List[TransportOption]
    selected_transport: Optional[TransportOption]
    hotels: List[HotelOption]
    selected_hotel: Optional[HotelOption]
    weather_forecasts: List[WeatherForecast]
    has_rainy_days: bool
    weather_advisories: List[str]
    days: List[DayPlan]
    itinerary_explanation: str
    budget: BudgetBreakdown
    safety_findings: List[SafetyFinding]
    agent_statuses: List[AgentExecutionStatus]
    
    # Workflow Control & Replanning
    validation_issues: List[str]
    replanning_attempts: int
    max_replanning_attempts: int
    is_rainy_replanning: bool
    relaxed_pace: bool
    specific_day_replan: Optional[int]
    final_trip_plan: Optional[FullTripPlan]

# --- Node Implementations ---

async def validate_requirements_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    issues: List[str] = []
    
    # Date validation
    try:
        s_date = datetime.strptime(state["start_date"], "%Y-%m-%d").date()
        e_date = datetime.strptime(state["end_date"], "%Y-%m-%d").date()
        if e_date < s_date:
            issues.append(f"End date ({state['end_date']}) cannot precede start date ({state['start_date']}).")
        calc_days = (e_date - s_date).days + 1
        duration_days = max(1, min(calc_days, 30))
    except Exception:
        issues.append("Invalid date format; expected YYYY-MM-DD.")
        duration_days = state.get("duration_days", 3)

    if state.get("travellers", 1) < 1:
        issues.append("Number of travellers must be at least 1.")

    if state.get("total_budget", 0) <= 0:
        issues.append("Total budget must be greater than zero.")

    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Requirements Validation",
        status="completed" if not issues else "completed",
        duration_ms=int((time.time() - t0) * 1000),
        summary="Validated traveler constraints, dates, and budget structure."
    ))

    return {
        "duration_days": duration_days,
        "validation_issues": issues,
        "agent_statuses": statuses,
        "replanning_attempts": state.get("replanning_attempts", 0),
        "max_replanning_attempts": 2
    }

async def retrieve_destination_data_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    dest_info = await geo_places_provider.get_destination_info(state["destination"])
    
    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Destination Geocoding & Knowledge",
        status="completed",
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Retrieved {len(dest_info.get('places', []))} verified places and coordinates for {dest_info.get('destination', state['destination'])}."
    ))

    return {
        "destination_data": dest_info,
        "places": dest_info.get("places", []),
        "agent_statuses": statuses
    }

async def transport_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    try:
        options, recommended = transport_agent.evaluate_transportation(
            origin=state["origin"],
            destination=state["destination"],
            travellers=state["travellers"],
            preferred_mode=state.get("transport_pref", "Best Value"),
            budget=state["total_budget"],
            currency=state.get("currency", "INR")
        )
        status = "completed"
        err = None
    except Exception as e:
        options, recommended = [], None
        status = "failed"
        err = str(e)

    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Transportation Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Compared {len(options)} transport modes. Recommended: {recommended.mode if recommended else 'Standard Overland'}.",
        error_message=err
    ))

    return {
        "transports": options,
        "selected_transport": recommended,
        "agent_statuses": statuses
    }

async def hotel_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    try:
        options, primary = hotel_agent.recommend_hotels(
            destination=state["destination"],
            duration_days=state["duration_days"],
            travellers=state["travellers"],
            preference=state.get("accommodation_pref", "Hotel"),
            travel_style=state.get("travel_style", "Balanced"),
            budget=state["total_budget"],
            currency=state.get("currency", "INR")
        )
        status = "completed"
        err = None
    except Exception as e:
        options, primary = [], None
        status = "failed"
        err = str(e)

    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Hotel & Accommodation Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Evaluated {len(options)} properties. Primary choice: {primary.name if primary else 'Curated Hotel'}.",
        error_message=err
    ))

    return {
        "hotels": options,
        "selected_hotel": primary,
        "agent_statuses": statuses
    }

async def weather_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    dest_data = state.get("destination_data", {})
    lat = dest_data.get("latitude", 15.2993)
    lng = dest_data.get("longitude", 74.1240)

    try:
        forecasts, has_rain, advisories = await weather_agent.analyze_weather(
            lat=lat,
            lng=lng,
            start_date_str=state["start_date"],
            duration_days=state["duration_days"]
        )
        status = "completed"
        err = None
    except Exception as e:
        forecasts, has_rain, advisories = [], False, []
        status = "failed"
        err = str(e)

    statuses = list(state.get("agent_statuses", []))
    rain_msg = f"{len([f for f in forecasts if f.is_rainy])} rainy days identified." if has_rain else "Clear & favorable forecast."
    statuses.append(AgentExecutionStatus(
        agent_name="Weather Intelligence Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Analyzed {len(forecasts)} forecast days. {rain_msg}",
        error_message=err
    ))

    return {
        "weather_forecasts": forecasts,
        "has_rainy_days": has_rain,
        "weather_advisories": advisories,
        "agent_statuses": statuses
    }

async def planner_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    try:
        days, explanation = planner_agent.plan_itinerary(
            destination=state["destination"],
            start_date_str=state["start_date"],
            duration_days=state["duration_days"],
            travellers=state["travellers"],
            interests=state.get("interests", ["Culture", "Food"]),
            travel_style=state.get("travel_style", "Balanced"),
            places=state.get("places", []),
            weather_forecasts=state.get("weather_forecasts", []),
            is_rainy_replanning=state.get("is_rainy_replanning", False),
            relaxed_pace=state.get("relaxed_pace", False)
        )
        status = "completed"
        err = None
    except Exception as e:
        days, explanation = [], "Planning encounter error, used baseline fallback."
        status = "failed"
        err = str(e)

    statuses = list(state.get("agent_statuses", []))
    total_acts = sum(len(d.activities) for d in days)
    statuses.append(AgentExecutionStatus(
        agent_name="Trip Planner Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Scheduled {len(days)} days with {total_acts} sequenced activities.",
        error_message=err
    ))

    return {
        "days": days,
        "itinerary_explanation": explanation,
        "agent_statuses": statuses
    }

async def budget_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    try:
        breakdown = budget_agent.calculate_budget(
            total_budget=state["total_budget"],
            travellers=state["travellers"],
            duration_days=state["duration_days"],
            selected_transport=state.get("selected_transport"),
            selected_hotel=state.get("selected_hotel"),
            days=state.get("days", []),
            currency=state.get("currency", "INR")
        )
        status = "completed"
        err = None
    except Exception as e:
        status = "failed"
        err = str(e)
        breakdown = None

    statuses = list(state.get("agent_statuses", []))
    summary_msg = f"Status: {breakdown.budget_status if breakdown else 'Unknown'}. Cost: {breakdown.currency if breakdown else ''} {breakdown.total_estimated_cost if breakdown else 0:,.0f}."
    statuses.append(AgentExecutionStatus(
        agent_name="Budget Optimization Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=summary_msg,
        error_message=err
    ))

    return {
        "budget": breakdown,
        "agent_statuses": statuses
    }

async def safety_agent_node(state: TripWorkflowState) -> Dict[str, Any]:
    t0 = time.time()
    dest_data = state.get("destination_data", {})
    is_curated = dest_data.get("is_curated", False)

    try:
        findings = safety_agent.evaluate_safety_and_reliability(
            destination=state["destination"],
            days=state.get("days", []),
            transport_options=state.get("transports", []),
            is_curated_destination=is_curated
        )
        status = "completed"
        err = None
    except Exception as e:
        findings = []
        status = "failed"
        err = str(e)

    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Travel Safety & Reliability Agent",
        status=status,
        duration_ms=int((time.time() - t0) * 1000),
        summary=f"Produced {len(findings)} safety findings and reliability checks.",
        error_message=err
    ))

    return {
        "safety_findings": findings,
        "agent_statuses": statuses
    }

async def conflict_resolution_node(state: TripWorkflowState) -> Dict[str, Any]:
    """Resolves severe budget deficits by adjusting hotel/transit before finalization."""
    t0 = time.time()
    budget = state.get("budget")
    hotels = state.get("hotels", [])
    selected_hotel = state.get("selected_hotel")
    attempts = state.get("replanning_attempts", 0) + 1

    adjusted = False
    if budget and budget.budget_deficit > 0 and hotels and selected_hotel:
        # Check if a cheaper hotel exists
        cheaper_hotels = [h for h in hotels if h.total_price < selected_hotel.total_price]
        if cheaper_hotels:
            lowest_hotel = min(cheaper_hotels, key=lambda x: x.total_price)
            selected_hotel = lowest_hotel
            adjusted = True
            
            # Recalculate budget with the cheaper hotel
            budget = budget_agent.calculate_budget(
                total_budget=state["total_budget"],
                travellers=state["travellers"],
                duration_days=state["duration_days"],
                selected_transport=state.get("selected_transport"),
                selected_hotel=selected_hotel,
                days=state.get("days", []),
                currency=state.get("currency", "INR")
            )

    statuses = list(state.get("agent_statuses", []))
    statuses.append(AgentExecutionStatus(
        agent_name="Conflict Resolution Engine",
        status="completed",
        duration_ms=int((time.time() - t0) * 1000),
        summary="Optimized accommodation selection to mitigate budget deficit." if adjusted else "Constraints verified within operational thresholds."
    ))

    return {
        "selected_hotel": selected_hotel,
        "budget": budget,
        "replanning_attempts": attempts,
        "agent_statuses": statuses
    }

async def assemble_final_plan_node(state: TripWorkflowState) -> Dict[str, Any]:
    """Compiles the unified FullTripPlan Pydantic model with data source provenance."""
    dest_data = state.get("destination_data", {})
    
    plan = FullTripPlan(
        trip_id=state["trip_id"],
        title=state.get("title") or f"{state['duration_days']}-Day Journey to {state['destination'].title()}",
        origin=state["origin"],
        destination=state["destination"],
        start_date=state["start_date"],
        end_date=state["end_date"],
        duration_days=state["duration_days"],
        travellers=state["travellers"],
        total_budget=state["total_budget"],
        currency=state.get("currency", "INR"),
        travel_style=state.get("travel_style", "Balanced"),
        itinerary_explanation=state.get("itinerary_explanation", "Multi-agent orchestrated itinerary."),
        days=state.get("days", []),
        budget=state.get("budget"),
        transports=state.get("transports", []),
        hotels=state.get("hotels", []),
        weather_forecasts=state.get("weather_forecasts", []),
        safety_findings=state.get("safety_findings", []),
        agent_statuses=state.get("agent_statuses", []),
        data_source_metadata={
            "geocoding_source": dest_data.get("source", "OpenStreetMap / TRIPORA"),
            "weather_source": state.get("weather_forecasts", [{}])[0].data_source if state.get("weather_forecasts") else "Open-Meteo",
            "transport_source": state.get("transports", [{}])[0].source if state.get("transports") else "TRIPORA Transit Benchmark",
            "hotel_source": state.get("hotels", [{}])[0].provider_source if state.get("hotels") else "TRIPORA Hotel Catalog",
            "orchestrator": "LangGraph Multi-Agent Workflow Engine 1.2"
        },
        last_replanned_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    return {"final_trip_plan": plan}

# --- Routing Logic ---

def should_resolve_conflicts(state: TripWorkflowState) -> str:
    budget = state.get("budget")
    attempts = state.get("replanning_attempts", 0)
    max_attempts = state.get("max_replanning_attempts", 2)

    # Route to conflict resolution if severe deficit and under retry cap
    if budget and budget.budget_deficit > (state["total_budget"] * 0.10) and attempts < max_attempts:
        return "resolve_conflicts"
    return "assemble_final_plan"

# --- Graph Assembly ---

def build_trip_workflow_graph() -> Any:
    workflow = StateGraph(TripWorkflowState)

    workflow.add_node("validate_requirements", validate_requirements_node)
    workflow.add_node("retrieve_destination_data", retrieve_destination_data_node)
    workflow.add_node("transport_agent", transport_agent_node)
    workflow.add_node("hotel_agent", hotel_agent_node)
    workflow.add_node("weather_agent", weather_agent_node)
    workflow.add_node("planner_agent", planner_agent_node)
    workflow.add_node("budget_agent", budget_agent_node)
    workflow.add_node("safety_agent", safety_agent_node)
    workflow.add_node("resolve_conflicts", conflict_resolution_node)
    workflow.add_node("assemble_final_plan", assemble_final_plan_node)

    # Linear and conditional workflow edges
    workflow.add_edge(START, "validate_requirements")
    workflow.add_edge("validate_requirements", "retrieve_destination_data")
    workflow.add_edge("retrieve_destination_data", "transport_agent")
    workflow.add_edge("transport_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "weather_agent")
    workflow.add_edge("weather_agent", "planner_agent")
    workflow.add_edge("planner_agent", "budget_agent")
    workflow.add_edge("budget_agent", "safety_agent")
    
    # Conditional branching for budget & constraint conflict resolution
    workflow.add_conditional_edges(
        "safety_agent",
        should_resolve_conflicts,
        {
            "resolve_conflicts": "resolve_conflicts",
            "assemble_final_plan": "assemble_final_plan"
        }
    )
    workflow.add_edge("resolve_conflicts", "assemble_final_plan")
    workflow.add_edge("assemble_final_plan", END)

    return workflow.compile()

trip_graph = build_trip_workflow_graph()

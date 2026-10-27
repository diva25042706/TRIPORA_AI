from typing import Dict, Any, List, Optional
from app.providers.llm_provider import llm_provider
from app.schemas.agent_schemas import FullTripPlan

class TravelChatAgent:
    """Conversational travel assistant grounded in the user's active trip state."""

    async def answer_question(
        self,
        trip_plan: FullTripPlan,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        # Build factual grounding context from the actual trip plan
        days_summary = []
        for d in trip_plan.days:
            act_names = [a.activity_name for a in d.activities]
            days_summary.append(f"Day {d.day_number} ({d.date}): {d.theme} - Activities: {', '.join(act_names)}")

        weather_summary = [
            f"Day {w.day_number} ({w.date}): {w.condition}, High {w.temp_high_c}°C, Low {w.temp_low_c}°C, {w.precipitation_chance}% rain"
            for w in trip_plan.weather_forecasts
        ]

        transport_summary = [
            f"{t.mode} ({t.currency} {t.estimated_cost:,.0f}, {t.duration_hours}h)"
            for t in trip_plan.transports
        ]

        hotel_summary = [
            f"{h.name} ({h.currency} {h.total_price:,.0f} total, {h.rating}★)"
            for h in trip_plan.hotels
        ]

        context_prompt = f"""You are TRIPORA AI Travel Assistant, a dedicated concierge for the following trip:
Destination: {trip_plan.destination} (Origin: {trip_plan.origin})
Dates: {trip_plan.start_date} to {trip_plan.end_date} ({trip_plan.duration_days} days)
Travellers: {trip_plan.travellers}
Total Budget: {trip_plan.currency} {trip_plan.total_budget:,.2f}
Estimated Cost: {trip_plan.currency} {trip_plan.budget.total_estimated_cost:,.2f} ({trip_plan.budget.budget_status})
Remaining / Deficit: {trip_plan.currency} {trip_plan.budget.remaining_budget:,.2f} remaining / {trip_plan.currency} {trip_plan.budget.budget_deficit:,.2f} deficit
Travel Style: {trip_plan.travel_style}

Daily Itinerary:
{chr(10).join(days_summary)}

Weather Forecasts:
{chr(10).join(weather_summary)}

Available Transports:
{chr(10).join(transport_summary)}

Available Hotels:
{chr(10).join(hotel_summary)}

CRITICAL SAFETY & TRUTH RULES:
1. Always base your answers on the verified trip facts above.
2. NEVER claim you have made a live booking, purchased tickets, reserved a hotel room, or charged payments.
3. If the user asks to modify the itinerary (e.g. cut budget, replace rainy day activities, relax pace), explain clearly that they can use the "Replan Itinerary" button in their dashboard to execute the change through our multi-agent workflow.
4. Keep your answer helpful, structured, and concise.
"""

        response = await llm_provider.generate_response(
            system_prompt=context_prompt,
            user_prompt=user_message
        )
        return response

travel_chat_agent = TravelChatAgent()

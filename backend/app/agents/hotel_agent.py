from typing import List, Dict, Any, Optional
from app.providers.hotel_provider import hotel_provider
from app.schemas.agent_schemas import HotelOption

class HotelAgent:
    """Agent 4: Recommends and ranks accommodations based on proximity, budget constraints, and traveller style."""

    def recommend_hotels(
        self,
        destination: str,
        duration_days: int,
        travellers: int,
        preference: str = "Hotel",
        travel_style: str = "Balanced",
        budget: float = 50000.0,
        currency: str = "INR"
    ) -> tuple[List[HotelOption], HotelOption]:
        nights = max(1, duration_days - 1)
        options = hotel_provider.get_hotels(
            destination=destination,
            nights=nights,
            travellers=travellers,
            preference=preference,
            style=travel_style,
            budget=budget,
            currency=currency
        )

        # Select primary choice based on style and budget
        # Calculate target hotel budget ceiling (~35% of total budget)
        hotel_budget_target = budget * 0.35

        # Find best candidate within target, or lowest cost if all exceed target
        candidates_within_budget = [h for h in options if h.total_price <= hotel_budget_target]
        if candidates_within_budget:
            primary_hotel = max(candidates_within_budget, key=lambda x: (x.rating or 4.0))
        else:
            primary_hotel = min(options, key=lambda x: x.total_price)

        return options, primary_hotel

hotel_agent = HotelAgent()

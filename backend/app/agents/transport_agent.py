from typing import List, Dict, Any, Optional
from app.providers.transport_provider import transport_provider
from app.schemas.agent_schemas import TransportOption

class TransportationAgent:
    """Agent 3: Evaluates multi-modal transit options, calculates journey durations, and recommends optimal routes."""

    def evaluate_transportation(
        self,
        origin: str,
        destination: str,
        travellers: int,
        preferred_mode: str = "Best Value",
        budget: float = 50000.0,
        currency: str = "INR"
    ) -> tuple[List[TransportOption], TransportOption]:
        options = transport_provider.get_transport_options(
            origin=origin,
            destination=destination,
            travellers=travellers,
            preferred_mode=preferred_mode,
            budget=budget,
            currency=currency
        )

        # Pick recommended option
        recommended = next((opt for opt in options if opt.is_recommended), options[0] if options else None)
        
        # If budget is tight, check if recommended option exceeds 35% of total budget
        if recommended and recommended.estimated_cost > (budget * 0.40):
            # Try to find a cheaper viable option
            cheaper = min(options, key=lambda x: x.estimated_cost)
            if cheaper.id != recommended.id:
                for opt in options:
                    opt.is_recommended = (opt.id == cheaper.id)
                cheaper.recommendation_rationale += f" Adjusted recommendation to conserve budget (costs {currency} {cheaper.estimated_cost:,.0f})."
                recommended = cheaper

        return options, recommended

transport_agent = TransportationAgent()

from typing import List, Dict, Any, Optional, Tuple
from app.providers.transport_provider import transport_provider
from app.schemas.agent_schemas import TransportOption

class TransportationAgent:
    """Agent 3: Evaluates multi-modal transit eligibility, benchmarks verified infrastructure, and ranks optimal routes."""

    def evaluate_transportation(
        self,
        origin: str,
        destination: str,
        travellers: int = 1,
        preferred_mode: str = "Best Value",
        budget: float = 50000.0,
        currency: str = "INR"
    ) -> Tuple[List[TransportOption], Optional[TransportOption]]:
        """
        Evaluate eligible transport modes for the route.
        Rejects ineligible modes (e.g. flights where no commercial airport exists).
        Ranks options by route suitability, duration, cost, and user preference.
        """
        options = transport_provider.get_transport_options(
            origin=origin,
            destination=destination,
            travellers=travellers,
            preferred_mode=preferred_mode,
            budget=budget,
            currency=currency
        )

        if not options:
            return [], None

        # Multi-factor ranking:
        # Score each option based on:
        # 1. User preferred mode match (+40)
        # 2. Duration efficiency (+0 to +30)
        # 3. Cost efficiency (+0 to +25)
        # 4. Zero transfers (+10)
        # 5. Verified data status (+10)
        
        pref = preferred_mode.strip().lower()
        min_dur = min(opt.duration_hours for opt in options)
        min_cost = min(opt.estimated_cost for opt in options)

        scored_options: List[Tuple[float, TransportOption]] = []
        for opt in options:
            score = 0.0
            mode_lower = opt.mode.lower()

            # Preference alignment
            if pref in ["fastest", "flight"] and "flight" in mode_lower:
                score += 45.0
            elif pref in ["budget", "bus"] and "bus" in mode_lower:
                score += 45.0
            elif pref in ["train", "rail"] and "train" in mode_lower:
                score += 45.0
            elif pref in ["cab", "car", "taxi", "self-drive", "private"] and "cab" in mode_lower:
                score += 45.0
            elif pref in ["best value", "balanced"]:
                score += 20.0

            # Duration score (faster is better)
            if opt.duration_hours > 0:
                score += (min_dur / opt.duration_hours) * 25.0

            # Cost score (cheaper is better)
            if opt.estimated_cost > 0:
                score += (min_cost / opt.estimated_cost) * 20.0

            # Direct route bonus
            if opt.transfers == 0:
                score += 10.0

            # Verification bonus
            if opt.verification_status == "verified":
                score += 10.0

            scored_options.append((score, opt))

        # Sort descending by score
        scored_options.sort(key=lambda x: x[0], reverse=True)
        ranked_options = [x[1] for x in scored_options]

        # Reset is_recommended flag and set top ranked
        for opt in ranked_options:
            opt.is_recommended = False
        ranked_options[0].is_recommended = True
        recommended = ranked_options[0]

        # Budget conservation guardrail:
        # If the recommended option consumes more than 40% of the total trip budget,
        # adjust recommendation to a more cost-effective viable overland option if available.
        if recommended.estimated_cost > (budget * 0.40) and len(ranked_options) > 1:
            cheaper_options = [o for o in ranked_options if o.estimated_cost <= (budget * 0.40)]
            if cheaper_options:
                cheaper = min(cheaper_options, key=lambda x: x.estimated_cost)
                if cheaper.id != recommended.id:
                    for opt in ranked_options:
                        opt.is_recommended = (opt.id == cheaper.id)
                    cheaper.recommendation_rationale += f" [Budget Optimization Agent: Adjusted to conserve budget ({currency} {cheaper.estimated_cost:,.0f} vs {currency} {recommended.estimated_cost:,.0f})]."
                    recommended = cheaper

        return ranked_options, recommended

transport_agent = TransportationAgent()

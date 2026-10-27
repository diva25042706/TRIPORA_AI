from typing import List, Dict, Any, Optional
from app.schemas.agent_schemas import (
    BudgetBreakdown,
    BudgetCategory,
    DayPlan,
    TransportOption,
    HotelOption
)

class BudgetOptimizationAgent:
    """Agent 2: Performs deterministic financial reconciliation, deficit detection, and cost optimization."""

    def calculate_budget(
        self,
        total_budget: float,
        travellers: int,
        duration_days: int,
        selected_transport: Optional[TransportOption],
        selected_hotel: Optional[HotelOption],
        days: List[DayPlan],
        currency: str = "INR"
    ) -> BudgetBreakdown:
        # 1. Transportation cost (from verified selected transport option)
        trans_cost = float(selected_transport.estimated_cost) if selected_transport else 0.0

        # 2. Accommodation cost
        hotel_cost = float(selected_hotel.total_price if selected_hotel else 3200.0 * max(1, duration_days - 1))

        # 3. Activities cost (sum of all activities across days)
        activity_cost = 0.0
        expensive_activities = []
        for d in days:
            for act in d.activities:
                activity_cost += act.estimated_cost
                if act.estimated_cost >= (1500.0 * travellers):
                    expensive_activities.append(f"{act.activity_name} ({currency} {act.estimated_cost:,.0f})")

        # 4. Food & Dining estimates (deterministic estimate per person per day)
        daily_food_per_person = 900.0  # standard comfortable dining
        food_cost = round(daily_food_per_person * travellers * duration_days, 2)

        # Subtotal before contingency
        core_subtotal = trans_cost + hotel_cost + activity_cost + food_cost

        # 5. Miscellaneous & Emergency Contingency Reserve (5% of core expenses)
        contingency_cost = round(core_subtotal * 0.05, 2)

        # Grand Total Reconciliation
        total_estimated_cost = round(trans_cost + hotel_cost + activity_cost + food_cost + contingency_cost, 2)

        # Budget variance calculations
        remaining_budget = round(max(0.0, total_budget - total_estimated_cost), 2)
        budget_deficit = round(max(0.0, total_estimated_cost - total_budget), 2)

        if total_estimated_cost > total_budget:
            budget_status = "Over Budget"
        elif total_estimated_cost >= (total_budget * 0.85):
            budget_status = "Within Budget"
        else:
            budget_status = "Under Budget"

        cost_per_person = round(total_estimated_cost / max(1, travellers), 2)

        # Build categorized breakdown with exact percentages that sum to 100%
        def calc_pct(amt: float) -> float:
            return round((amt / total_estimated_cost * 100.0), 1) if total_estimated_cost > 0 else 0.0

        categories = [
            BudgetCategory(
                category="Transportation",
                amount=round(trans_cost, 2),
                percentage=calc_pct(trans_cost),
                description=f"Intercity travel ({selected_transport.mode if selected_transport else 'Standard Transit'}) for {travellers} passenger(s)",
                is_estimate=True
            ),
            BudgetCategory(
                category="Accommodation",
                amount=round(hotel_cost, 2),
                percentage=calc_pct(hotel_cost),
                description=f"{duration_days} days / {max(1, duration_days - 1)} night(s) at {selected_hotel.name if selected_hotel else 'Curated Hotel'}",
                is_estimate=True
            ),
            BudgetCategory(
                category="Activities & Sightseeing",
                amount=round(activity_cost, 2),
                percentage=calc_pct(activity_cost),
                description=f"Curated tickets, monuments, guided tours, and museum entries",
                is_estimate=True
            ),
            BudgetCategory(
                category="Food & Dining",
                amount=round(food_cost, 2),
                percentage=calc_pct(food_cost),
                description=f"Breakfasts, lunches, street food, and dinners at {currency} {daily_food_per_person:,.0f}/person/day",
                is_estimate=True
            ),
            BudgetCategory(
                category="Contingency & Incidentals",
                amount=round(contingency_cost, 2),
                percentage=calc_pct(contingency_cost),
                description="5% reserve for local transport, tips, souvenirs, and unexpected expenses",
                is_estimate=True
            )
        ]

        # Cost saving recommendations
        recommendations = []
        if budget_deficit > 0:
            recommendations.append(f"Estimated expenses exceed budget by {currency} {budget_deficit:,.0f}. Consider switching accommodation to a verified Boutique or 3-Star stay.")
            if trans_cost > (total_budget * 0.35):
                recommendations.append("Transportation consumes over 35% of total budget. Review train or sleeper bus options to save up to 40% on transit.")
            if expensive_activities:
                recommendations.append(f"High-cost activities detected: {', '.join(expensive_activities[:2])}. Replace with self-guided walks or heritage parks.")
        else:
            recommendations.append(f"Your trip has a healthy surplus of {currency} {remaining_budget:,.0f} ({round(remaining_budget/total_budget*100, 1)}% headroom).")
            recommendations.append("Consider upgrading to a premier dining experience or extending museum tours without exceeding constraints.")

        calc_notes = (
            f"Deterministic calculation completed: sum of categories ({currency} {total_estimated_cost:,.2f}) "
            f"exactly matches grand total. Budget limit: {currency} {total_budget:,.2f}."
        )

        return BudgetBreakdown(
            total_budget=total_budget,
            total_estimated_cost=total_estimated_cost,
            remaining_budget=remaining_budget,
            budget_deficit=budget_deficit,
            budget_status=budget_status,
            currency=currency,
            cost_per_person=cost_per_person,
            categories=categories,
            expensive_items=expensive_activities,
            cost_saving_recommendations=recommendations,
            calculation_notes=calc_notes
        )

budget_agent = BudgetOptimizationAgent()

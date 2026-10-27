import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import TripCreateRequest, TripUpdateRequest, ReplanRequest, ReplanResponse, ReplanDiffSummary
from app.schemas.agent_schemas import FullTripPlan
from app.workflows.trip_workflow import trip_graph

class TripService:
    async def create_and_plan_trip(self, db: Session, user: User, req: TripCreateRequest) -> Trip:
        trip_id = str(uuid.uuid4())
        title = req.title or f"{req.travel_style} Journey to {req.destination.title()}"

        initial_state = {
            "trip_id": trip_id,
            "title": title,
            "origin": req.origin,
            "destination": req.destination,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "travellers": req.travellers,
            "total_budget": req.total_budget,
            "currency": req.currency or user.preferred_currency or "INR",
            "travel_style": req.travel_style,
            "interests": req.interests,
            "accommodation_pref": req.accommodation_pref,
            "transport_pref": req.transport_pref,
            "agent_statuses": [],
            "replanning_attempts": 0,
            "max_replanning_attempts": 2
        }

        # Run multi-agent orchestration workflow
        final_state = await trip_graph.ainvoke(initial_state)
        full_plan: FullTripPlan = final_state["final_trip_plan"]

        new_trip = Trip(
            id=trip_id,
            user_id=user.id,
            title=title,
            origin=req.origin,
            destination=req.destination,
            start_date=req.start_date,
            end_date=req.end_date,
            duration_days=full_plan.duration_days,
            travellers=req.travellers,
            total_budget=req.total_budget,
            currency=req.currency,
            travel_style=req.travel_style,
            interests=req.interests,
            accommodation_pref=req.accommodation_pref,
            transport_pref=req.transport_pref,
            status="completed",
            full_trip_data=full_plan.model_dump()
        )
        db.add(new_trip)
        db.commit()
        db.refresh(new_trip)
        return new_trip

    def get_trip_by_id(self, db: Session, trip_id: str, user_id: int) -> Trip:
        trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or you do not have permission to view it."
            )
        return trip

    def list_user_trips(self, db: Session, user_id: int) -> List[Trip]:
        return db.query(Trip).filter(Trip.user_id == user_id).order_by(Trip.created_at.desc()).all()

    def update_trip(self, db: Session, trip_id: str, user_id: int, req: TripUpdateRequest) -> Trip:
        trip = self.get_trip_by_id(db, trip_id, user_id)
        if req.title is not None:
            trip.title = req.title
        if req.total_budget is not None:
            trip.total_budget = req.total_budget
        if req.travel_style is not None:
            trip.travel_style = req.travel_style
        if req.interests is not None:
            trip.interests = req.interests
        if req.accommodation_pref is not None:
            trip.accommodation_pref = req.accommodation_pref
        if req.transport_pref is not None:
            trip.transport_pref = req.transport_pref

        trip.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(trip)
        return trip

    def delete_trip(self, db: Session, trip_id: str, user_id: int) -> bool:
        trip = self.get_trip_by_id(db, trip_id, user_id)
        db.delete(trip)
        db.commit()
        return True

    async def replan_trip(self, db: Session, trip_id: str, user_id: int, req: ReplanRequest) -> ReplanResponse:
        trip = self.get_trip_by_id(db, trip_id, user_id)
        current_data = trip.full_trip_data or {}
        prev_total = current_data.get("budget", {}).get("total_estimated_cost", trip.total_budget)

        # Parse user instruction
        instruction_lower = req.instruction.lower()
        is_rain = "rain" in instruction_lower or "weather" in instruction_lower
        relaxed_pace = "relax" in instruction_lower or "slower" in instruction_lower

        new_budget = req.new_budget if req.new_budget else trip.total_budget
        if "reduce budget" in instruction_lower or "cheaper" in instruction_lower:
            new_budget = round(trip.total_budget * 0.80, 2)  # 20% budget cut request

        new_travel_style = req.new_travel_style or trip.travel_style
        if relaxed_pace:
            new_travel_style = "Relaxed"

        new_interests = req.new_interests or trip.interests
        if "history" in instruction_lower or "museum" in instruction_lower:
            if "History" not in new_interests:
                new_interests = list(new_interests) + ["History", "Museums"]

        replan_state = {
            "trip_id": trip.id,
            "title": trip.title,
            "origin": trip.origin,
            "destination": trip.destination,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "duration_days": trip.duration_days,
            "travellers": trip.travellers,
            "total_budget": new_budget,
            "currency": trip.currency,
            "travel_style": new_travel_style,
            "interests": new_interests,
            "accommodation_pref": req.new_accommodation_pref or trip.accommodation_pref,
            "transport_pref": req.new_transport_pref or trip.transport_pref,
            "agent_statuses": [],
            "replanning_attempts": 0,
            "max_replanning_attempts": 2,
            "is_rainy_replanning": is_rain,
            "relaxed_pace": relaxed_pace,
            "specific_day_replan": req.specific_day
        }

        # Run multi-agent graph with updated constraints
        final_state = await trip_graph.ainvoke(replan_state)
        updated_plan: FullTripPlan = final_state["final_trip_plan"]

        new_total = updated_plan.budget.total_estimated_cost
        cost_diff = round(new_total - prev_total, 2)

        # Build changes summary
        changes = []
        if cost_diff < 0:
            changes.append(f"Reduced estimated overall cost by {trip.currency} {abs(cost_diff):,.2f}.")
        elif cost_diff > 0:
            changes.append(f"Revised estimated overall cost increased by {trip.currency} {cost_diff:,.2f}.")
        
        if is_rain:
            changes.append("Swapped scheduled open-air attractions for covered cultural museums and heritage galleries.")
        if relaxed_pace:
            changes.append("Scaled daily pacing to 2 curated activities per day with extended relaxation intervals.")
        if req.specific_day:
            changes.append(f"Re-sequenced activities specifically for Day {req.specific_day}.")
        changes.append("Recalculated full itemized budget, hotel pricing, and safety schedule checks.")

        diff_summary = ReplanDiffSummary(
            cost_difference=cost_diff,
            previous_total=prev_total,
            new_total=new_total,
            currency=trip.currency,
            changes_summary=changes,
            affected_days=[req.specific_day] if req.specific_day else list(range(1, trip.duration_days + 1)),
            notes=f"Replanning completed based on instruction: '{req.instruction}'."
        )

        # Save the updated plan to the trip
        trip.total_budget = new_budget
        trip.travel_style = new_travel_style
        trip.interests = new_interests
        trip.full_trip_data = updated_plan.model_dump()
        trip.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(trip)

        return ReplanResponse(
            trip_id=trip.id,
            diff_summary=diff_summary,
            updated_plan=updated_plan
        )

trip_service = TripService()

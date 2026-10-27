from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.chat import ChatMessage
from app.models.trip import Trip
from app.agents.travel_chat_agent import travel_chat_agent
from app.schemas.agent_schemas import FullTripPlan

class ChatService:
    async def process_chat_message(
        self,
        db: Session,
        trip_id: str,
        user_id: int,
        content: str
    ) -> Dict[str, Any]:
        # Validate trip ownership
        trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip context not found or access denied."
            )

        if not trip.full_trip_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Trip does not have a completed itinerary plan yet."
            )

        full_plan = FullTripPlan(**trip.full_trip_data)

        # Save user message
        user_msg = ChatMessage(
            trip_id=trip_id,
            user_id=user_id,
            role="user",
            content=content,
            agent_name="User"
        )
        db.add(user_msg)
        db.commit()

        # Query conversational agent
        reply_text = await travel_chat_agent.answer_question(
            trip_plan=full_plan,
            user_message=content
        )

        # Save assistant message
        bot_msg = ChatMessage(
            trip_id=trip_id,
            user_id=user_id,
            role="assistant",
            content=reply_text,
            agent_name="TRIPORA Assistant"
        )
        db.add(bot_msg)
        db.commit()
        db.refresh(bot_msg)

        return {
            "id": bot_msg.id,
            "role": "assistant",
            "content": reply_text,
            "agent_name": "TRIPORA Assistant",
            "created_at": bot_msg.created_at.isoformat()
        }

    def get_conversation_history(self, db: Session, trip_id: str, user_id: int) -> List[ChatMessage]:
        # Enforce trip ownership
        trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found or unauthorized."
            )
        return db.query(ChatMessage).filter(ChatMessage.trip_id == trip_id).order_by(ChatMessage.created_at.asc()).all()

chat_service = ChatService()

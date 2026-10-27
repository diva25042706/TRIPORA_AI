from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(String(36), ForeignKey("trips.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    agent_name = Column(String(50), default="Trip Assistant")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    trip = relationship("Trip", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    duration_days = Column(Integer, default=1)
    travellers = Column(Integer, default=1)
    total_budget = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    travel_style = Column(String(50), default="Balanced")  # "Budget", "Balanced", "Luxury", "Adventurous", "Relaxed"
    interests = Column(JSON, default=list)  # list of strings: ["Culture", "Food", "Nature", ...]
    accommodation_pref = Column(String(50), default="Hotel")  # "Hostel", "Hotel", "Resort", "Apartment"
    transport_pref = Column(String(50), default="Best Value")  # "Flight", "Train", "Bus", "Self-Drive", "Best Value"
    status = Column(String(50), default="draft")  # "draft", "planning", "completed", "archived"
    
    # Store complete structured agent outputs, itinerary days, budgets, maps, forecasts
    full_trip_data = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="trips")
    chat_messages = relationship("ChatMessage", back_populates="trip", cascade="all, delete-orphan")

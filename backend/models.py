"""
SQLAlchemy database models.
Defines the structure of all database tables.
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, Float, ARRAY, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User model: Stores user account information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    school = Column(String(255), nullable=False)
    year = Column(String(50), nullable=False)
    avatar_url = Column(Text)
    interests = Column(ARRAY(Text))  # Array of interest tags
    height_cm = Column(Integer)  # Height in centimeters
    weight_kg = Column(Integer)  # Weight in kilograms
    nationality = Column(String(100))  # Nationality
    ethnicity = Column(String(100))  # Ethnicity
    photos = Column(ARRAY(Text), default=[])  # Array of photo URLs
    profile_completed = Column(Boolean, default=False)  # Whether profile is fully completed
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    verification_token_expires = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    sent_date_requests = relationship("DateRequest", foreign_keys="DateRequest.sender_id", back_populates="sender")
    received_date_requests = relationship("DateRequest", foreign_keys="DateRequest.receiver_id", back_populates="receiver")
    created_events = relationship("Event", back_populates="creator")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")


class DateRequest(Base):
    """DateRequest model: Stores date invitations between users."""
    __tablename__ = "date_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending")  # pending, accepted, rejected
    message = Column(Text)
    proposed_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_date_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_date_requests")
    
    __table_args__ = (
        UniqueConstraint('sender_id', 'receiver_id', name='unique_date_request'),
    )


class Event(Base):
    """Event model: Stores campus events created by users."""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255), nullable=False)
    event_time = Column(TIMESTAMP, nullable=False)
    tags = Column(ARRAY(Text))  # Array of event tags
    max_attendees = Column(Integer)
    image_url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_events")
    attendees = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")


class EventAttendee(Base):
    """EventAttendee model: Stores RSVP status for events."""
    __tablename__ = "event_attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rsvp_status = Column(String(50), default="interested")  # going, interested, declined
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="attendees")
    
    __table_args__ = (
        UniqueConstraint('event_id', 'user_id', name='unique_event_attendee'),
    )


class Message(Base):
    """Message model: Stores chat messages between users."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")


class Match(Base):
    """Match model: Stores mutual matches between users."""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float)  # Optional: AI matching score
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='unique_match'),
        CheckConstraint('user1_id != user2_id', name='check_different_users'),
    )


"""
Buyer — biomass plants, brick kilns, paper mills, etc.
Location: backend/app/models/buyer.py
"""

from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, Text

from app.models.base import Base, TimestampMixin, new_uuid


class Buyer(Base, TimestampMixin):
    __tablename__ = "buyers"

    id = Column(String(36), primary_key=True, default=new_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    business_name = Column(String(200), nullable=False)
    buyer_type = Column(String(50), nullable=False)
    # JSON-serialised list of waste type strings — cross-DB compatible
    accepted_waste = Column(Text, nullable=False)          # e.g. '["rice_straw","wheat_straw"]'
    price_per_kg = Column(Numeric(8, 2))
    min_quantity_kg = Column(Numeric(10, 2), default=500)
    max_capacity_kg = Column(Numeric(10, 2))
    provides_pickup = Column(Boolean, default=False)
    pickup_radius_km = Column(Integer, default=0)
    state = Column(String(50), nullable=False)
    district = Column(String(100))
    pincode = Column(String(6))
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    phone = Column(String(15), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

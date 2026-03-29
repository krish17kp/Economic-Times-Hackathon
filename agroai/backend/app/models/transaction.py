"""
Transaction — marketplace enquiries and deals (Phase 1.5).
Location: backend/app/models/transaction.py
"""

from sqlalchemy import Column, String, Numeric, Date, Enum, ForeignKey

from app.models.base import Base, TimestampMixin, new_uuid
from app.core.constants import TransactionStatus


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=new_uuid)
    waste_log_id = Column(String(36), ForeignKey("waste_logs.id"), nullable=True)
    seller_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    buyer_id = Column(String(36), ForeignKey("buyers.id"), nullable=False, index=True)
    quantity_kg = Column(Numeric(10, 2), nullable=False)
    agreed_price = Column(Numeric(8, 2))
    status = Column(Enum(TransactionStatus), default=TransactionStatus.ENQUIRY)
    pickup_date = Column(Date)

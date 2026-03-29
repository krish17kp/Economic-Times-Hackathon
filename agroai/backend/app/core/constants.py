"""
Enums, magic numbers, unit conversion constants.
Location: backend/app/core/constants.py
"""

from enum import Enum


class WasteType(str, Enum):
    RICE_STRAW = "rice_straw"
    WHEAT_STRAW = "wheat_straw"
    RICE_HUSK = "rice_husk"
    SUGARCANE_BAGASSE = "sugarcane_bagasse"
    COTTON_STALK = "cotton_stalk"


class QualityGrade(str, Enum):
    DRY = "dry"
    SEMI_DRY = "semi_dry"
    WET = "wet"


class ConversionType(str, Enum):
    BIOCHAR = "biochar"
    BRIQUETTE = "briquette"
    MUSHROOM_SUBSTRATE = "mushroom_substrate"


class UserRole(str, Enum):
    FARMER = "farmer"
    BUYER = "buyer"
    FPO_MANAGER = "fpo_manager"
    ADMIN = "admin"


class TransactionStatus(str, Enum):
    ENQUIRY = "enquiry"
    CONFIRMED = "confirmed"
    PICKED_UP = "picked_up"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Quality multiplier applied to price and conversion yield
QUALITY_MULTIPLIER = {
    QualityGrade.DRY: 1.0,
    QualityGrade.SEMI_DRY: 0.85,
    QualityGrade.WET: 0.60,
}

# Transport constants (sourced from FPO interviews in Punjab/Haryana)
TRANSPORT_BASE_COST_INR = 500
TRANSPORT_RATE_PER_KM_PER_TON_TRACTOR = 8.0
TRANSPORT_RATE_PER_KM_PER_TON_TRUCK = 5.5
TRACTOR_MAX_CAPACITY_KG = 5000
ROAD_CONDITION_FACTOR = 1.3  # Rural roads are ~1.3x straight-line distance

# Buyer scoring weights (sum to 1.0)
BUYER_WEIGHT_PRICE = 0.35
BUYER_WEIGHT_DISTANCE = 0.25
BUYER_WEIGHT_PICKUP = 0.15
BUYER_WEIGHT_VERIFIED = 0.10
BUYER_WEIGHT_CAPACITY = 0.15

# Equipment amortization default
DEFAULT_AMORTIZATION_BATCHES = 20

# Raw sale default time (days)
RAW_SALE_TIME_DAYS = 3

# Converted product selling time (added to processing time)
CONVERTED_PRODUCT_SELL_TIME_DAYS = 7

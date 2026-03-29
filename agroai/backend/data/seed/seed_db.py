"""
Seeds the database with initial data from JSON/CSV files.
Location: backend/data/seed/seed_db.py

Usage: python data/seed/seed_db.py
"""

import json
import csv
from pathlib import Path
from datetime import date

# Add parent to path so we can import app
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.database import get_engine, SessionLocal
from app.models import Base
from app.models.market_price import MarketPrice
from app.models.buyer import Buyer
from app.models.conversion_rule import ConversionRule
from app.models.carbon_factor import CarbonFactor

SEED_DIR = Path(__file__).parent


def seed_market_prices(db):
    """Load market_prices_2024.csv into database."""
    csv_path = SEED_DIR / "market_prices_2024.csv"
    if not csv_path.exists():
        print("  ⚠ market_prices_2024.csv not found, skipping")
        return

    existing = db.query(MarketPrice).count()
    if existing > 0:
        print(f"  → Market prices already seeded ({existing} rows), skipping")
        return

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            entry = MarketPrice(
                waste_type=row["waste_type"],
                region=row["region"],
                district=row.get("district"),
                price_min=float(row["price_min"]),
                price_max=float(row["price_max"]),
                price_avg=float(row["price_avg"]),
                source=row.get("source", "manual"),
                recorded_date=date.fromisoformat(row["recorded_date"]),
            )
            db.add(entry)
            count += 1

    db.commit()
    print(f"  ✓ Seeded {count} market price records")


def seed_buyers(db):
    """Load buyers_seed.json into database safely."""
    json_path = SEED_DIR / "buyers_seed.json"
    if not json_path.exists():
        print("  ⚠ buyers_seed.json not found, skipping")
        return

    with open(json_path, "r") as f:
        buyers = json.load(f)

    count = 0
    for b in buyers:
        # Idempotent check: Does the buyer already exist?
        existing_buyer = db.query(Buyer).filter(Buyer.business_name == b["business_name"]).first()
        if existing_buyer:
            continue

        # Store accepted_waste as JSON string (DB-agnostic SQLite safe)
        accepted_waste_json = json.dumps(b["accepted_waste"])
        entry = Buyer(
            business_name=b["business_name"],
            buyer_type=b["buyer_type"],
            accepted_waste=accepted_waste_json,
            price_per_kg=b.get("price_per_kg"),
            min_quantity_kg=b.get("min_quantity_kg", 500),
            max_capacity_kg=b.get("max_capacity_kg"),
            provides_pickup=b.get("provides_pickup", False),
            pickup_radius_km=b.get("pickup_radius_km", 0),
            state=b["state"],
            district=b.get("district"),
            pincode=b.get("pincode"),
            latitude=b["latitude"],
            longitude=b["longitude"],
            phone=b["phone"],
            is_verified=b.get("is_verified", False),
            is_active=True,
        )
        db.add(entry)
        count += 1

    db.commit()
    print(f"  ✓ Seeded {count} new buyers")


def seed_conversion_rules(db):
    """Load conversion_rules.json into database."""
    json_path = SEED_DIR / "conversion_rules.json"
    if not json_path.exists():
        print("  ⚠ conversion_rules.json not found, skipping")
        return

    existing = db.query(ConversionRule).count()
    if existing > 0:
        print(f"  → Conversion rules already seeded ({existing} rows), skipping")
        return

    with open(json_path, "r") as f:
        rules = json.load(f)

    count = 0
    for r in rules:
        entry = ConversionRule(
            input_waste=r["input_waste"],
            output_product=r["output_product"],
            conversion_ratio=r["conversion_ratio"],
            processing_cost_per_kg=r["processing_cost_per_kg"],
            output_price_per_kg=r["output_price_per_kg"],
            equipment_cost=r.get("equipment_cost"),
            min_viable_qty_kg=r.get("min_viable_qty_kg", 1000),
            processing_time_days=r.get("processing_time_days", 7),
            skill_level=r.get("skill_level", "moderate"),
            source=r.get("source"),
            last_updated=date.today(),
        )
        db.add(entry)
        count += 1

    db.commit()
    print(f"  ✓ Seeded {count} conversion rules")


def seed_carbon_factors(db):
    """Load carbon_factors.json into database."""
    json_path = SEED_DIR / "carbon_factors.json"
    if not json_path.exists():
        print("  ⚠ carbon_factors.json not found, skipping")
        return

    existing = db.query(CarbonFactor).count()
    if existing > 0:
        print(f"  → Carbon factors already seeded ({existing} rows), skipping")
        return

    with open(json_path, "r") as f:
        factors = json.load(f)

    count = 0
    for cf in factors:
        entry = CarbonFactor(
            waste_type=cf["waste_type"],
            burn_emission_kg_co2_per_kg=cf["burn_emission_kg_co2_per_kg"],
            conversion_type=cf.get("conversion_type"),
            sequestration_kg_co2_per_kg=cf.get("sequestration_kg_co2_per_kg", 0),
            source=cf.get("source"),
        )
        db.add(entry)
        count += 1

    db.commit()
    print(f"  ✓ Seeded {count} carbon factors")


def main():
    print("=" * 50)
    print("AgroAI Database Seeder")
    print("=" * 50)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=get_engine())
    print("✓ Tables created/verified")

    db = SessionLocal()
    try:
        seed_market_prices(db)
        seed_buyers(db)
        seed_conversion_rules(db)
        seed_carbon_factors(db)
        print("\n✓ Seeding complete!")
    except Exception as e:
        print(f"\n✗ Seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

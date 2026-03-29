"""
Carbon impact estimation.
Location: backend/app/services/carbon_calculator.py
"""

from sqlalchemy.orm import Session
from app.models.carbon_factor import CarbonFactor


def estimate_carbon(db: Session, waste_type: str, quantity_kg: float) -> dict:
    """
    Estimates CO2 impact for burning vs selling vs converting.
    """
    factors = db.query(CarbonFactor).filter(CarbonFactor.waste_type == waste_type).all()

    # Crop-specific fallback factors (kg CO2 per kg waste)
    burn_defaults = {
        "rice_straw": 1.46,
        "wheat_straw": 1.62,
        "cotton_stalk": 1.35,
        "sugarcane_bagasse": 1.20,
        "rice_husk": 1.40
    }
    
    burn_factor = burn_defaults.get(waste_type, 1.5)
    biochar_seq = 0.0
    source = "ICAR/IPCC 2006 Estimates"

    if factors:
        for f in factors:
            burn_factor = float(f.burn_emission_kg_co2_per_kg or burn_factor)
            source = f.source or "Database"
            # Safely check conversion_type — it can be None or an Enum
            conv_type = f.conversion_type
            if conv_type is not None:
                # Handle both Enum object and plain string
                conv_str = conv_type.value if hasattr(conv_type, "value") else str(conv_type)
                if conv_str == "biochar":
                    biochar_seq = float(f.sequestration_kg_co2_per_kg or 0)

    co2_burned = round(quantity_kg * burn_factor, 2)
    co2_sequestered = round(quantity_kg * (biochar_seq or 0.8), 2)  # 0.8kg seq if biochar fallback

    tonnes_burned = co2_burned / 1000
    tonnes_seq = co2_sequestered / 1000

    # Tree equivalent: ~22 kg CO2 per tree per year
    trees = int(co2_burned / 22)

    return {
        "if_burned": {
            "co2_kg": co2_burned,
            "label_en": f"Burning releases {tonnes_burned:.1f} tonnes CO₂",
            "label_hi": f"जलाने से {tonnes_burned:.1f} टन CO₂ उत्सर्जन होता है",
        },
        "if_sold": {
            "co2_kg": co2_burned,
            "label_en": f"Selling avoids {tonnes_burned:.1f} tonnes CO₂ emissions",
            "label_hi": f"बेचने से {tonnes_burned:.1f} टन CO₂ उत्सर्जन से बचाव होता है",
        },
        "if_biochar": {
            "co2_kg": co2_sequestered,
            "label_en": f"Biochar sequesters {tonnes_seq:.2f} tonnes CO₂",
            "label_hi": f"बायोचार {tonnes_seq:.2f} टन CO₂ को सोखता है",
        },
        "equivalent_en": f"Equivalent to planting {trees} trees",
        "equivalent_hi": f"यह {trees} पेड़ लगाने के बराबर है",
        "source": source,
    }

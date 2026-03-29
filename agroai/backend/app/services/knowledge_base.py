"""
Embedded knowledge base for hackathon-friendly offline AI assistant.
Covers the 4 assistant topics with real agricultural domain knowledge.
Location: backend/app/services/knowledge_base.py
"""

# Category-based grounded knowledge chunks
# Source: ICAR guidelines, MNRE biochar manual, Punjab FPO interviews
KNOWLEDGE = {
    "how_to_convert": [
        """
RICE STRAW TO BIOCHAR:
1. Dry rice straw to below 15% moisture content (takes 2-3 sunny days).
2. Load into a pyrolysis kiln or drum kiln. Fill 70% capacity.
3. Ignite from the top (top-lit updraft method).
4. Burn at 350-500°C for 4-6 hours. Restrict oxygen by partially closing vents.
5. Cool for 12 hours. Do NOT add water - it cracks the biochar and lowers quality.
6. Yield: 1 tonne rice straw → 250-300 kg biochar.
7. Sell price: ₹8-15 per kg. Net margin: ₹2,000-4,500 per tonne raw straw.
""",
        """
WHEAT STRAW TO BRIQUETTES:
1. Chop straw into 2-5 cm pieces using a chaff cutter.
2. Dry to 10-12% moisture (crucial for briquette binding).
3. Feed into screw-press or piston-press briquette machine at 100-150 MPa pressure.
4. No binder needed when moisture is correct and pressure is high.
5. Output briquettes: 60-90 mm diameter, 150-300 mm length.
6. Yield: 1 tonne wheat straw → 900-950 kg briquettes.
7. Sell price: ₹4-6 per kg. Net margin: ₹1,800-3,200 per tonne raw straw.
""",
        """
SUGARCANE BAGASSE TO MUSHROOM SUBSTRATE:
1. Steam-sterilize bagasse at 121°C for 90 minutes to kill competing fungi.
2. Cool to 28°C before inoculating.
3. Mix with wheat bran (10:1 ratio) to improve nutrition.
4. Inoculate with oyster mushroom spawn (Pleurotus ostreatus).
5. Incubate in dark at 25-28°C for 18-21 days until fully colonized.
6. Move to fruiting room with 85-90% humidity and indirect light.
7. First flush harvest in 5-7 days. 3-4 flushes total.
8. Yield: 1 tonne bagasse → 300-500 kg fresh mushrooms.
9. Mushroom sell price: ₹80-150/kg. Highly profitable.
""",
    ],

    "equipment": [
        """
BIOCHAR KILN OPTIONS AND COSTS:
1. Brick batch kiln (DIY): ₹15,000-25,000. Capacity 200-500 kg/batch. For small farmers.
2. Retort drum kiln: ₹40,000-80,000. Capacity 300-800 kg/batch. Best for FPOs.
3. Continuous pyrolysis unit: ₹5-20 lakhs. High capacity. For large aggregators only.
4. Key parts to check: temperature gauge, air vents, loading door seal quality.
5. MNRE subsidizes 30-50% cost under biomass program. Check with local KVK.
""",
        """
BRIQUETTE MACHINE TYPES AND COSTS:
1. Screw-press briquette machine: ₹80,000-2,50,000. Output 100-300 kg/hour.
   - Best for: wheat straw, rice husk, cotton stalk.
   - Produces: solid cylindrical log briquettes.
2. Piston-press machine: ₹1-5 lakhs. Output 300-1000 kg/hour.
   - Best for: mixed biomass, commercial scale.
   - Produces: hollow or solid briquettes.
3. Hydraulic baler (for raw sale): ₹2-8 lakhs. Does NOT convert, just compresses.
4. Essential accessories: chaff cutter (₹15,000-40,000), dryer or drying yard.
5. Pay-per-use Custom Hiring Centers (CHC) available in most districts.
""",
        """
WHERE TO BUY EQUIPMENT IN INDIA:
- MNRE approved vendors list: https://mnre.gov.in
- Major brands: Radhe Industrial (Gujarat), Agro Power (Punjab), Sri Ram Biomass (Tamil Nadu)
- Local KVK and FPOs often have equipment for hire at ₹500-2000/day
- Second-hand machines available at agricultural fairs (Kisan Mela)
- Always check motor warranty minimum 2 years, and die/mould quality
""",
    ],

    "quality_tips": [
        """
HOW TO TEST MOISTURE CONTENT:
- Ideal range: 10-15% for briquettes, below 20% for biochar, below 25% for sale.
- Field test: Grab a handful. If it crumbles and doesn't clump, moisture is okay.
- Accurate test: Weigh 100g wet sample. Dry in oven at 105°C for 24 hours. Re-weigh.
  Formula: Moisture% = (wet weight - dry weight) / wet weight × 100
- Invest ₹1,500-3,000 in a handheld moisture meter for fast readings.
""",
        """
STORAGE BEST PRACTICES FOR CROP WASTE:
1. Never store wet or damp biomass - it molds within 5-7 days.
2. Raise bales off the ground on wooden pallets or plastic sheets.
3. Cover with tarpaulin but leave sides open for airflow (prevent condensation).
4. Store away from standing water. Flood-prone areas: use elevated platforms.
5. Biochar: once made, store in sealed bags. It absorbs moisture from air rapidly.
6. Briquettes: store indoors or under covered shed. Do not stack over 8 feet.
7. Maximum storage time: raw straw 3-4 months, briquettes 12+ months, biochar indefinitely.
""",
        """
HOW DRY STRAW INCREASES YOUR INCOME:
- Wet straw (30% moisture): buyers pay ₹0.5-1.5/kg
- Dry straw (15% moisture): buyers pay ₹2-3.5/kg
- Briquettes need: below 12% moisture (highest value conversion)
- Simple drying method: Spread in thin layer (6-8 inch) on flat surface in sun.
  Turn every 4-6 hours. Achieves 15% moisture in 2-3 sunny days.
- Do not dry on roads (crushes material and mixes with soil, reduces grade).
""",
    ],

    "general_policy": [
        """
PARALI (CROP RESIDUE) BURNING BAN IN INDIA:
- Supreme Court of India has banned open burning of paddy straw since 2015.
- Penalty: ₹2,500 per acre in Punjab, Haryana, UP (as per NGT order).
- Enforcement is increasing — check with local Block Agriculture Officer.
- Alternative: Apply for PUSA bio-decomposer spray (free from governments of Delhi, Haryana).
""",
        """
GOVERNMENT SCHEMES FOR BIOMASS:
1. MNRE Biomass Power and Cogeneration Programme: subsidy for biomass plants.
2. PM-KUSUM Scheme: for solar-powered biomass processing equipment.
3. Agriculture Infrastructure Fund (AIF): 3% interest subvention loan for agro-processing.
4. National Clean Energy Fund (NCEF): for large community biochar/briquette units.
5. State-level schemes: Punjab Biomass Policy 2021, Maharashtra Green Energy Mission.
6. Contact: nearest KVK (Krishi Vigyan Kendra) for application assistance.
""",
        """
CARBON CREDITS FROM CROP RESIDUE MANAGEMENT:
- Biochar application to soil earns carbon credits under Verra VCS Standard.
- Price: $10-50 per tonne CO₂ equivalent (₹800-4,000).
- Aggregators like Varaha Climate, Gold Standard India can onboard small farmers.
- Required: GPS coordinates of field, before/after photos, quantity of biochar applied.
- Not burning paddy = 1 tonne of straw = prevents ~1.5 tonnes CO₂ emission.
- Minimum viable scale: 50 acres+ for aggregated carbon project.
""",
    ],
}


def get_grounded_answer(question: str, category: str) -> str:
    """
    Provides a grounded answer from the embedded knowledge base.
    Used as both primary (no API key) and fallback (API failure) mode.
    Returns the most relevant knowledge chunk for the category.
    """
    chunks = KNOWLEDGE.get(category, [])
    if not chunks:
        return "I don't have information about this topic. Please consult your local KVK (Krishi Vigyan Kendra)."

    question_lower = question.lower()

    # Keyword-based chunk selection
    scored = []
    for chunk in chunks:
        score = 0
        for word in question_lower.split():
            if len(word) > 3 and word in chunk.lower():
                score += 1
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_chunk = scored[0][1].strip()

    if scored[0][0] == 0:
        # No keyword match — return all chunks combined summary
        return chunks[0].strip()

    return best_chunk

"""
Standardized Tamil Nadu 38-District Knowledge Base Adapter.
Integrates the complete 38-district verified repository from app.providers.tamil_nadu_complete_data.
"""

from typing import Dict, Any, List
from app.providers.tamil_nadu_complete_data import TAMIL_NADU_ALL_DISTRICTS_DATA

# Create adapted TAMIL_NADU_DISTRICTS with backwards-compatible place keys
TAMIL_NADU_DISTRICTS: Dict[str, Dict[str, Any]] = {}

for d_key, d_info in TAMIL_NADU_ALL_DISTRICTS_DATA.items():
    adapted_places = []
    for p in d_info.get("places", []):
        adapted_place = dict(p)
        # Ensure backward compatibility keys
        adapted_place["duration"] = p.get("visit_duration_hours", 2.0)
        adapted_place["cost"] = p.get("ticket_price_inr", 0.0)
        adapted_place["is_outdoor"] = p.get("is_outdoor", True)
        adapted_place["locality"] = p.get("locality", d_info.get("city", "Tamil Nadu"))
        adapted_places.append(adapted_place)

    TAMIL_NADU_DISTRICTS[d_key] = {
        "city": d_info.get("city", d_info["district"]),
        "district": d_info["district"],
        "state": "Tamil Nadu",
        "country": "India",
        "lat": d_info["lat"],
        "lng": d_info["lng"],
        "desc": d_info.get("desc", f"Historic district of {d_info['district']}, Tamil Nadu"),
        "places": adapted_places
    }

# Backward compatibility alias
DISTRICT_LIST: List[str] = sorted(list(TAMIL_NADU_DISTRICTS.keys()))

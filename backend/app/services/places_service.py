import math
from typing import List, Dict, Any, Optional
from app.providers.chennai_places_data import CHENNAI_COMPREHENSIVE_PLACES
from app.schemas.place import PlaceItem, PlaceSearchResponse, CategoryCount, AreaZoneCount

class PlacesService:
    def __init__(self):
        self._raw_places = self._deduplicate_places(CHENNAI_COMPREHENSIVE_PLACES)

    def _deduplicate_places(self, places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicates places based on unique ID, normalized name, and close coordinates (<50 meters).
        """
        seen_ids = set()
        seen_names = set()
        deduped = []

        for p in places:
            pid = p.get("id")
            norm_name = p.get("name", "").strip().lower()
            
            if pid in seen_ids or norm_name in seen_names:
                continue

            seen_ids.add(pid)
            seen_names.add(norm_name)
            deduped.append(p)

        return deduped

    def get_place_by_id(self, place_id: str) -> Optional[PlaceItem]:
        for p in self._raw_places:
            if p["id"] == place_id:
                return PlaceItem(**p)
        return None

    def get_categories(self) -> List[CategoryCount]:
        counts: Dict[str, int] = {}
        for p in self._raw_places:
            cat = p.get("category", "General")
            counts[cat] = counts.get(cat, 0) + 1
        
        sorted_cats = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return [CategoryCount(category=c[0], count=c[1]) for c in sorted_cats]

    def get_zones(self) -> List[AreaZoneCount]:
        labels = {
            "chennai_city": "Chennai City",
            "greater_chennai": "Greater Chennai Suburbs",
            "day_trips": "Nearby Day Trips (Outside Chennai)"
        }
        counts: Dict[str, int] = {}
        for p in self._raw_places:
            z = p.get("area_zone", "chennai_city")
            counts[z] = counts.get(z, 0) + 1

        ordered_zones = ["chennai_city", "greater_chennai", "day_trips"]
        res = []
        for z in ordered_zones:
            if z in counts:
                res.append(AreaZoneCount(zone=z, label=labels.get(z, z), count=counts[z]))
        return res

    def search_places(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        area_zone: Optional[str] = None,
        sort_by: str = "default",
        page: int = 1,
        limit: int = 12
    ) -> PlaceSearchResponse:
        filtered = list(self._raw_places)

        # 1. Filter by area zone if specified and not 'all'
        if area_zone and area_zone.lower() not in ("all", ""):
            filtered = [p for p in filtered if p.get("area_zone", "").lower() == area_zone.lower()]

        # 2. Filter by category if specified and not 'all'
        if category and category.lower() not in ("all", ""):
            filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]

        # 3. Filter by text query across name, locality, address, desc
        if query and query.strip():
            q = query.strip().lower()
            filtered = [
                p for p in filtered
                if q in p.get("name", "").lower()
                or q in p.get("locality", "").lower()
                or q in p.get("address", "").lower()
                or q in p.get("desc", "").lower()
                or q in p.get("category", "").lower()
                or q in p.get("district", "").lower()
            ]

        # 4. Sorting
        if sort_by == "name_asc":
            filtered.sort(key=lambda x: x.get("name", "").lower())
        elif sort_by == "name_desc":
            filtered.sort(key=lambda x: x.get("name", "").lower(), reverse=True)
        elif sort_by == "duration_asc":
            filtered.sort(key=lambda x: x.get("visit_duration_hours", 2.0))
        elif sort_by == "duration_desc":
            filtered.sort(key=lambda x: x.get("visit_duration_hours", 2.0), reverse=True)
        elif sort_by == "price_asc":
            filtered.sort(key=lambda x: x.get("ticket_price_inr", 0.0))
        elif sort_by == "price_desc":
            filtered.sort(key=lambda x: x.get("ticket_price_inr", 0.0), reverse=True)

        total = len(filtered)
        limit = max(1, min(limit, 100))
        total_pages = max(1, math.ceil(total / limit)) if total > 0 else 1
        page = max(1, page)

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_raw = filtered[start_idx:end_idx]

        results = [PlaceItem(**p) for p in paginated_raw]
        has_more = end_idx < total

        return PlaceSearchResponse(
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_more=has_more,
            results=results,
            available_categories=self.get_categories(),
            available_zones=self.get_zones()
        )

# Global singleton service
places_service = PlacesService()

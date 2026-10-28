import math
from typing import List, Dict, Any, Optional
from app.providers.tamil_nadu_complete_data import TAMIL_NADU_ALL_DISTRICTS_DATA
from app.providers.chennai_places_data import CHENNAI_COMPREHENSIVE_PLACES
from app.providers.geo_places_provider import TN_DISTRICT_ALIASES
from app.schemas.place import PlaceItem, PlaceSearchResponse, CategoryCount, AreaZoneCount, DistrictSummary

class PlacesService:
    def __init__(self):
        self._raw_places = self._load_and_deduplicate_all_places()

    def _load_and_deduplicate_all_places(self) -> List[Dict[str, Any]]:
        """
        Loads all verified attractions across all 38 Tamil Nadu districts
        and metropolitan zones, deduplicating by unique ID and normalized name.
        """
        seen_ids = set()
        seen_names = set()
        deduped = []

        # 1. Load Chennai comprehensive places first (preserves chennai_city, greater_chennai, day_trips)
        for p in CHENNAI_COMPREHENSIVE_PLACES:
            pid = p.get("id")
            norm_name = p.get("name", "").strip().lower()
            if pid in seen_ids or (norm_name and norm_name in seen_names):
                continue
            seen_ids.add(pid)
            if norm_name:
                seen_names.add(norm_name)
            deduped.append(dict(p))

        # 2. Load all other districts from 38-district database
        for dist_key, dist_data in TAMIL_NADU_ALL_DISTRICTS_DATA.items():
            for p in dist_data.get("places", []):
                pid = p.get("id")
                norm_name = p.get("name", "").strip().lower()

                if pid in seen_ids or (norm_name and norm_name in seen_names):
                    continue

                seen_ids.add(pid)
                if norm_name:
                    seen_names.add(norm_name)

                # Ensure default values for schema compatibility
                place_record = dict(p)
                place_record.setdefault("district", dist_data.get("district", dist_key.title()))
                place_record.setdefault("city", dist_data.get("city", dist_key.title()))
                place_record.setdefault("state", "Tamil Nadu")
                place_record.setdefault("area_zone", "district_attraction")
                place_record.setdefault("area_label", dist_data.get("district", dist_key.title()))
                place_record.setdefault("source_attribution", "Tamil Nadu Tourism (TTDC)")
                place_record.setdefault("source_confidence", "verified_official")
                place_record.setdefault("last_verified", "2026-10-28")
                place_record.setdefault("status", "active")
                place_record.setdefault("ticket_price_inr", float(p.get("cost", 0.0)))
                place_record.setdefault("visit_duration_hours", float(p.get("duration", 2.0)))
                place_record.setdefault("is_outdoor", bool(p.get("out", p.get("is_outdoor", True))))

                deduped.append(place_record)

        return deduped

    def get_place_by_id(self, place_id: str) -> Optional[PlaceItem]:
        for p in self._raw_places:
            if p["id"] == place_id:
                return PlaceItem(**p)
        return None

    def get_categories(self) -> List[CategoryCount]:
        counts: Dict[str, int] = {}
        for p in self._raw_places:
            cat = p.get("category", "Heritage")
            counts[cat] = counts.get(cat, 0) + 1

        sorted_cats = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return [CategoryCount(category=c[0], count=c[1]) for c in sorted_cats]

    def get_zones(self) -> List[AreaZoneCount]:
        labels = {
            "chennai_city": "Chennai City",
            "greater_chennai": "Greater Chennai Suburbs",
            "day_trips": "Nearby Day Trips (Outside Chennai)",
            "district_attraction": "Tamil Nadu Districts"
        }
        counts: Dict[str, int] = {}
        for p in self._raw_places:
            z = p.get("area_zone", "district_attraction")
            counts[z] = counts.get(z, 0) + 1

        res = []
        for z, count in counts.items():
            res.append(AreaZoneCount(zone=z, label=labels.get(z, z.replace("_", " ").title()), count=count))
        return sorted(res, key=lambda x: -x.count)

    def get_districts(self) -> List[DistrictSummary]:
        summaries = []
        for dist_key, dist_data in sorted(TAMIL_NADU_ALL_DISTRICTS_DATA.items()):
            places = dist_data.get("places", [])
            pop_names = [p.get("name", "") for p in places[:3]]
            summaries.append(DistrictSummary(
                district=dist_data.get("district", dist_key.title()),
                district_key=dist_key,
                city=dist_data.get("city", dist_key.title()),
                lat=dist_data.get("lat", 11.0),
                lng=dist_data.get("lng", 78.0),
                attraction_count=len(places),
                popular_attractions=pop_names
            ))
        return summaries

    def resolve_destination(self, query: str) -> Dict[str, Any]:
        """
        Resolves a user-entered town, alias, or landmark to its administrative district.
        e.g. 'Ooty' -> 'nilgiris', 'Rameswaram' -> 'ramanathapuram', 'Kodaikanal' -> 'dindigul'.
        """
        norm = query.strip().lower()

        # Direct district key match
        if norm in TAMIL_NADU_ALL_DISTRICTS_DATA:
            d = TAMIL_NADU_ALL_DISTRICTS_DATA[norm]
            return {
                "resolved_district_key": norm,
                "district": norm,
                "district_name": d["district"],
                "city": d["city"],
                "lat": d["lat"],
                "lng": d["lng"],
                "attractions_available": len(d["places"]),
                "total_attractions": len(d["places"]),
                "is_tamil_nadu": True
            }

        # Check alias dictionary
        if norm in TN_DISTRICT_ALIASES:
            dk = TN_DISTRICT_ALIASES[norm]
            if dk in TAMIL_NADU_ALL_DISTRICTS_DATA:
                d = TAMIL_NADU_ALL_DISTRICTS_DATA[dk]
                return {
                    "resolved_district_key": dk,
                    "district": dk,
                    "district_name": d["district"],
                    "city": d["city"],
                    "lat": d["lat"],
                    "lng": d["lng"],
                    "attractions_available": len(d["places"]),
                    "total_attractions": len(d["places"]),
                    "is_tamil_nadu": True
                }

        # Check place name matches
        for p in self._raw_places:
            if norm in p["name"].lower():
                d_name = p["district"]
                dk = d_name.lower().replace(" ", "")
                return {
                    "resolved_district_key": dk,
                    "district": dk,
                    "district_name": d_name,
                    "city": p["city"],
                    "lat": p["lat"],
                    "lng": p["lng"],
                    "matched_place": p["name"],
                    "total_attractions": 1,
                    "is_tamil_nadu": True
                }

        return {
            "resolved_district_key": None,
            "district_name": query.title(),
            "city": query.title(),
            "is_tamil_nadu": False
        }

    def search_places(
        self,
        query: Optional[str] = None,
        district: Optional[str] = None,
        category: Optional[str] = None,
        area_zone: Optional[str] = None,
        sort_by: str = "default",
        page: int = 1,
        limit: int = 12
    ) -> PlaceSearchResponse:
        filtered = list(self._raw_places)

        # 1. Filter by district if specified
        if district and district.lower() not in ("all", ""):
            d_norm = district.strip().lower()
            # If alias used (e.g. ooty), resolve to district name
            if d_norm in TN_DISTRICT_ALIASES:
                d_norm = TN_DISTRICT_ALIASES[d_norm]

            filtered = [
                p for p in filtered
                if p.get("district", "").lower() == d_norm
                or d_norm in p.get("district", "").lower()
                or d_norm in p.get("city", "").lower()
            ]

        # 2. Filter by area zone if specified and not 'all'
        if area_zone and area_zone.lower() not in ("all", ""):
            filtered = [p for p in filtered if p.get("area_zone", "").lower() == area_zone.lower()]

        # 3. Filter by category if specified and not 'all'
        if category and category.lower() not in ("all", ""):
            filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]

        # 4. Filter by text query across name, locality, address, desc, category, district
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
                or q in p.get("city", "").lower()
            ]

        # 5. Sorting
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
            available_zones=self.get_zones(),
            available_districts=self.get_districts()
        )

# Global singleton service
places_service = PlacesService()

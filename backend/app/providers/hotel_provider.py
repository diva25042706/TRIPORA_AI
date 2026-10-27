from typing import List, Dict, Any
from app.schemas.agent_schemas import HotelOption

class HotelProvider:
    """Accommodation provider calculating realistic options, distances, and itemized costs."""

    def get_hotels(
        self,
        destination: str,
        nights: int,
        travellers: int,
        preference: str = "Hotel",
        style: str = "Balanced",
        budget: float = 50000.0,
        currency: str = "INR"
    ) -> List[HotelOption]:
        nights = max(1, nights)
        rooms_needed = max(1, (travellers + 1) // 2)

        # Baseline per-night rates per room according to tier
        rates = {
            "Budget": 1800.0,
            "Balanced": 3800.0,
            "Luxury": 11500.0,
            "Boutique": 5200.0,
            "Hostel": 950.0,
            "Resort": 8500.0
        }

        base_rate = rates.get(style, rates.get(preference, 3500.0))

        # Generate realistic candidate properties for the destination
        properties = [
            {
                "id": "hotel_1",
                "name": f"The Heritage Grand {destination.title()}",
                "location": f"Historic Central Promenade, {destination.title()}",
                "rate_mult": 1.15,
                "rating": 4.6,
                "amenities": ["High-Speed Wi-Fi", "Complimentary Breakfast", "Rooftop Restaurant", "Airport Shuttle", "24/7 Concierge"],
                "dist_km": 1.2,
                "desc": f"Refined colonial-era boutique architecture featuring garden courtyards, elegant rooms, and walking access to main cultural attractions.",
                "ranking_rationale": "Top recommendation: optimal balance of central proximity, heritage character, and verified customer reviews."
            },
            {
                "id": "hotel_2",
                "name": f"{destination.title()} Emerald Bay Suites",
                "location": f"Waterfront Vista District, {destination.title()}",
                "rate_mult": 0.85,
                "rating": 4.3,
                "amenities": ["Complimentary Breakfast", "Swimming Pool", "Fitness Center", "Free Parking", "Air Conditioning"],
                "dist_km": 2.8,
                "desc": f"Contemporary hotel offering spacious family suites, scenic views, and leisure amenities suitable for extended stays.",
                "ranking_rationale": "Best value selection: high comfort-to-cost ratio with full leisure amenities and pool access."
            },
            {
                "id": "hotel_3",
                "name": f"Royal Orchid Palace & Spa",
                "location": f"Golden Enclave, {destination.title()}",
                "rate_mult": 2.1,
                "rating": 4.8,
                "amenities": ["Ayurvedic Wellness Spa", "Infinity Pool", "Fine Dining Pavilion", "Butler Service", "Private Balconies"],
                "dist_km": 3.5,
                "desc": f"5-star luxury property with sprawling landscaped lawns, multi-cuisine dining, and signature spa treatments.",
                "ranking_rationale": "Luxury highlight: premium choice for travellers seeking high-end hospitality and pampering."
            },
            {
                "id": "hotel_4",
                "name": f"Backpackers Social Hub & Pods",
                "location": f"Old Quarter Arts Alley, {destination.title()}",
                "rate_mult": 0.35,
                "rating": 4.2,
                "amenities": ["Free Wi-Fi", "Co-working Lounge", "Community Kitchen", "Lockers", "Weekly Walking Tours"],
                "dist_km": 0.8,
                "desc": f"Vibrant social hostel offering air-conditioned private rooms and designer dormitory pods with lively community events.",
                "ranking_rationale": "Budget saver: ultra-economical option located right in the heart of pedestrian alleys."
            }
        ]

        hotel_options: List[HotelOption] = []
        for p in properties:
            per_night_per_room = round(base_rate * p["rate_mult"], 0)
            total_room_cost = round(per_night_per_room * nights * rooms_needed, 0)
            hotel_options.append(HotelOption(
                id=p["id"],
                name=p["name"],
                location=p["location"],
                price_per_night=per_night_per_room,
                total_price=total_room_cost,
                currency=currency,
                rating=p["rating"],
                amenities=p["amenities"],
                distance_to_center_km=p["dist_km"],
                description=p["desc"],
                provider_source="TRIPORA Verified Hotel Knowledge Catalog (Demo Mode)",
                booking_url=f"https://www.google.com/travel/hotels/{destination.lower()}",
                is_verified=True,
                availability_status="Available for direct inquiry / Standard rate",
                ranking_rationale=p["ranking_rationale"]
            ))

        return hotel_options

hotel_provider = HotelProvider()

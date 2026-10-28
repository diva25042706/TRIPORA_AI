import math
from typing import List, Dict, Any, Optional
import httpx
from app.core.config import settings
from app.providers.tamil_nadu_districts import TAMIL_NADU_DISTRICTS

# Curated high-fidelity destination database with verified landmarks, coordinates, and categories
DESTINATION_CATALOG: Dict[str, Dict[str, Any]] = {
    "goa": {
        "city": "Goa",
        "country": "India",
        "lat": 15.2993,
        "lng": 74.1240,
        "places": [
            {"name": "Aguada Fort & Lighthouse", "category": "Culture", "lat": 15.4920, "lng": 73.7735, "is_outdoor": True, "duration": 2.0, "cost": 100, "desc": "17th-century Portuguese fortress overlooking Sinquerim beach with panoramic Arabian sea views."},
            {"name": "Basilica of Bom Jesus", "category": "Culture", "lat": 15.5009, "lng": 73.9116, "is_outdoor": False, "duration": 1.5, "cost": 50, "desc": "UNESCO World Heritage site containing the tomb and mortal remains of St. Francis Xavier."},
            {"name": "Baga & Calangute Beach Coastal Walk", "category": "Nature", "lat": 15.5553, "lng": 73.7517, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Vibrant shoreline walk featuring coastal shacks, artisan stalls, and ocean breezes."},
            {"name": "Dudhsagar Waterfalls Trek", "category": "Adventure", "lat": 15.3144, "lng": 74.3143, "is_outdoor": True, "duration": 4.0, "cost": 800, "desc": "Majestic four-tiered waterfall located on the Mandovi River amidst the Western Ghats."},
            {"name": "Fontainhas Latin Quarter Heritage Walk", "category": "Culture", "lat": 15.4989, "lng": 73.8311, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Picturesque old quarter of Panaji with brightly colored colonial Portuguese houses and bakeries."},
            {"name": "Goa Chitra Museum", "category": "Culture", "lat": 15.2678, "lng": 73.9664, "is_outdoor": False, "duration": 2.0, "cost": 300, "desc": "Ethnographic museum showcasing traditional Goan farming implements and indigenous craftsmanship."},
            {"name": "Mandovi River Sunset Cruise", "category": "Relaxation", "lat": 15.4989, "lng": 73.8278, "is_outdoor": True, "duration": 2.0, "cost": 650, "desc": "Leisurely evening river cruise with traditional Goan folk performances and DJ music."},
            {"name": "Anjuna Flea Market & Sunset Point", "category": "Food", "lat": 15.5782, "lng": 73.7408, "is_outdoor": True, "duration": 2.5, "cost": 200, "desc": "Iconic seaside market offering bohemian handicrafts, seaside cafes, and fresh seafood shacks."},
            {"name": "Sahakari Spice Farm Tour", "category": "Nature", "lat": 15.4050, "lng": 74.0200, "is_outdoor": True, "duration": 2.5, "cost": 500, "desc": "Guided walk through organic vanilla, cardamom, and cinnamon plantations followed by traditional buffet lunch."},
            {"name": "Houses of Goa Museum", "category": "Culture", "lat": 15.5397, "lng": 73.8647, "is_outdoor": False, "duration": 1.5, "cost": 150, "desc": "Architectural museum designed by Gerard da Cunha documenting Goan colonial home designs."}
        ]
    },
    "paris": {
        "city": "Paris",
        "country": "France",
        "lat": 48.8566,
        "lng": 2.3522,
        "places": [
            {"name": "Louvre Museum", "category": "Culture", "lat": 48.8606, "lng": 2.3376, "is_outdoor": False, "duration": 3.5, "cost": 2000, "desc": "World's largest art museum housing the Mona Lisa and Venus de Milo in a historic royal palace."},
            {"name": "Eiffel Tower & Champ de Mars", "category": "Sightseeing", "lat": 48.8584, "lng": 2.2945, "is_outdoor": True, "duration": 2.5, "cost": 2800, "desc": "Iconic iron lattice tower offering panoramic views of Paris from its observation summits."},
            {"name": "Musée d'Orsay", "category": "Culture", "lat": 48.8599, "lng": 2.3265, "is_outdoor": False, "duration": 2.5, "cost": 1600, "desc": "Renowned impressionist and post-impressionist museum located in a Beaux-Arts railway station."},
            {"name": "Montmartre & Sacré-Cœur Basilica", "category": "Sightseeing", "lat": 48.8867, "lng": 2.3431, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Bohemian hilltop district with cobbled alleys, street portraitists, and panoramic basilica terrace."},
            {"name": "Seine River Sightseeing Cruise", "category": "Relaxation", "lat": 48.8583, "lng": 2.2944, "is_outdoor": True, "duration": 1.5, "cost": 1500, "desc": "Scenic audio-guided boat tour passing Notre-Dame, Pont Alexandre III, and historic riverbanks."},
            {"name": "Sainte-Chapelle & Conciergerie", "category": "Culture", "lat": 48.8554, "lng": 2.3450, "is_outdoor": False, "duration": 1.5, "cost": 1200, "desc": "Gothic royal chapel famed for its 1,113 magnificent 13th-century stained-glass panels."},
            {"name": "Jardin du Luxembourg", "category": "Nature", "lat": 48.8462, "lng": 2.3371, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Formal manicured gardens with tree-lined promenades, Medici fountain, and model sailboat basin."},
            {"name": "Le Marais Culinary & Boutique Walk", "category": "Food", "lat": 48.8575, "lng": 2.3622, "is_outdoor": True, "duration": 2.5, "cost": 1000, "desc": "Historic neighborhood boasting artisan boulangeries, falafel eateries, and independent fashion ateliers."}
        ]
    },
    "tokyo": {
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.6762,
        "lng": 139.6503,
        "places": [
            {"name": "Senso-ji Temple & Nakamise Street", "category": "Culture", "lat": 35.7148, "lng": 139.7967, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Tokyo's oldest Buddhist temple founded in 645 AD, approached through traditional snack and souvenir stalls."},
            {"name": "Meiji Jingu Shrine & Yoyogi Forest", "category": "Culture", "lat": 35.6764, "lng": 139.6993, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Serene Shinto shrine enveloped by 170 acres of tranquil sacred evergreen forest in central Shibuya."},
            {"name": "teamLab Planets Digital Art Museum", "category": "Culture", "lat": 35.6517, "lng": 139.7897, "is_outdoor": False, "duration": 2.5, "cost": 2500, "desc": "Immersive body-interactive digital art installations where visitors walk barefoot through water and light."},
            {"name": "Shibuya Crossing & Hachiko Statue", "category": "Sightseeing", "lat": 35.6595, "lng": 139.7005, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "World's busiest pedestrian scramble intersection flanked by giant neon screens and rooftop viewing decks."},
            {"name": "Tsukiji Outer Market Food Exploration", "category": "Food", "lat": 35.6655, "lng": 139.7708, "is_outdoor": True, "duration": 2.0, "cost": 1200, "desc": "Bustling foodie haven of fresh sushi stands, tamagoyaki grills, and wagyu skewers."},
            {"name": "Tokyo National Museum (Ueno)", "category": "Culture", "lat": 35.7188, "lng": 139.7765, "is_outdoor": False, "duration": 2.5, "cost": 800, "desc": "Japan's oldest national museum housing over 110,000 national treasures and samurai artifacts."},
            {"name": "Akihabara Tech & Anime District", "category": "Sightseeing", "lat": 35.6983, "lng": 139.7731, "is_outdoor": False, "duration": 2.5, "cost": 0, "desc": "Electric town renowned for multi-story electronics stores, retro gaming arcades, and manga emporiums."}
        ]
    },
    "jaipur": {
        "city": "Jaipur",
        "country": "India",
        "lat": 26.9124,
        "lng": 75.7873,
        "places": [
            {"name": "Amber Palace & Fort", "category": "Culture", "lat": 26.9855, "lng": 75.8513, "is_outdoor": True, "duration": 3.0, "cost": 500, "desc": "Majestic hilltop fort with ornate marble pavilions, Sheesh Mahal mirror palace, and Maota Lake views."},
            {"name": "Hawa Mahal (Palace of Winds)", "category": "Sightseeing", "lat": 26.9239, "lng": 75.8267, "is_outdoor": True, "duration": 1.5, "cost": 200, "desc": "Pink sandstone facade with 953 honeycomb jharokha windows built in 1799 for royal court ladies."},
            {"name": "City Palace & Museum", "category": "Culture", "lat": 26.9258, "lng": 75.8237, "is_outdoor": False, "duration": 2.5, "cost": 700, "desc": "Sprawling royal residence blending Rajput and Mughal architecture with preserved royal costumes and armory."},
            {"name": "Jantar Mantar Astronomical Observatory", "category": "Culture", "lat": 26.9248, "lng": 75.8246, "is_outdoor": True, "duration": 1.5, "cost": 200, "desc": "UNESCO monument with 19 architectural astronomical instruments including the world's largest stone sundial."},
            {"name": "Nahargarh Fort Sunset Viewpoint", "category": "Sightseeing", "lat": 26.9372, "lng": 75.8155, "is_outdoor": True, "duration": 2.0, "cost": 200, "desc": "Edge-of-Aravalli ridge fortress providing breathtaking bird's-eye sunsets over the entire Pink City."},
            {"name": "Albert Hall State Museum", "category": "Culture", "lat": 26.9116, "lng": 75.8195, "is_outdoor": False, "duration": 2.0, "cost": 300, "desc": "Oldest museum of Rajasthan boasting Indo-Saracenic architecture, rare pottery, and Persian carpets."},
            {"name": "Johari Bazaar & Bapu Bazaar Walk", "category": "Food", "lat": 26.9212, "lng": 75.8279, "is_outdoor": True, "duration": 2.5, "cost": 300, "desc": "Vibrant traditional bazaars famous for Jaipuri quilts, gemstone jewelry, lac bangles, and kachori stalls."}
        ]
    }
}

# Merge all 38 Tamil Nadu districts into curated destination catalog
DESTINATION_CATALOG.update(TAMIL_NADU_DISTRICTS)

# Map common tourist town aliases and spelling variations to district keys
TN_DISTRICT_ALIASES: Dict[str, str] = {
    # Major tourist towns
    "ooty": "nilgiris",
    "udhagamandalam": "nilgiris",
    "coonoor": "nilgiris",
    "kodaikanal": "dindigul",
    "kodai": "dindigul",
    "palani": "dindigul",
    "rameswaram": "ramanathapuram",
    "rameshwaram": "ramanathapuram",
    "dhanushkodi": "ramanathapuram",
    "trichy": "tiruchirappalli",
    "srirangam": "tiruchirappalli",
    "tanjore": "thanjavur",
    "kumbakonam": "thanjavur",
    "mahabalipuram": "chengalpattu",
    "mamallapuram": "chengalpattu",
    "kovalam": "chengalpattu",
    "yelagiri": "tirupathur",
    "hogenakkal": "dharmapuri",
    "kolli hills": "namakkal",
    "chettinad": "sivaganga",
    "karaikudi": "sivaganga",
    "megamalai": "theni",
    "meghamalai": "theni",
    "pichavaram": "cuddalore",
    "chidambaram": "cuddalore",
    "gingee": "viluppuram",
    "velankanni": "nagapattinam",
    "nagore": "nagapattinam",
    "tranquebar": "mayiladuthurai",
    "tharangambadi": "mayiladuthurai",
    "srivilliputhur": "virudhunagar",
    "rajapalayam": "virudhunagar",
    "courtallam": "tenkasi",
    "kutralam": "tenkasi",
    "gangaikonda cholapuram": "ariyalur",
    "yercaud": "salem",
    "mettur": "salem",
    "tiruchendur": "thoothukudi",
    "tuticorin": "thoothukudi",
    "pollachi": "coimbatore",
    "valparai": "coimbatore",
    "bhavani": "erode",
    "tiruthani": "tiruvallur",
    "pulicat": "tiruvallur",
    "mannargudi": "tiruvarur",
    "arcot": "ranipet",
    # Administrative spelling variations
    "kanchipuram": "kancheepuram",
    "kanyakumari": "kanniyakumari",
    "sivagangai": "sivaganga",
    "villupuram": "viluppuram",
    "thiruvannamalai": "tiruvannamalai",
    "thiruchirappalli": "tiruchirappalli",
    "thiruvarur": "tiruvarur",
    "thirunelveli": "tirunelveli",
    "thirupathur": "tirupathur",
    "thiruppur": "tiruppur",
    "thiruvallur": "tiruvallur",
}


for alias, district_key in TN_DISTRICT_ALIASES.items():
    if district_key in TAMIL_NADU_DISTRICTS and alias not in DESTINATION_CATALOG:
        DESTINATION_CATALOG[alias] = TAMIL_NADU_DISTRICTS[district_key]

class GeoPlacesProvider:
    """Provider for geocoding, coordinates, and verified attraction data."""

    def __init__(self):
        self.catalog = DESTINATION_CATALOG

    async def get_destination_info(self, destination_name: str) -> Dict[str, Any]:
        """Look up coordinates and attractions for a destination."""
        norm_key = destination_name.strip().lower()

        # Check aliases first
        if norm_key in TN_DISTRICT_ALIASES and TN_DISTRICT_ALIASES[norm_key] in self.catalog:
            data = self.catalog[TN_DISTRICT_ALIASES[norm_key]]
            return {
                "destination": data["city"],
                "country": data["country"],
                "latitude": data["lat"],
                "longitude": data["lng"],
                "places": data["places"],
                "is_curated": True,
                "source": "TRIPORA Verified Destination Knowledge Base (Tamil Nadu State Catalog)"
            }

        for key, data in self.catalog.items():
            if key in norm_key or norm_key in key:
                source_lbl = "TRIPORA Verified Destination Knowledge Base"
                if "state" in data and data["state"] == "Tamil Nadu":
                    source_lbl = "TRIPORA Verified Destination Knowledge Base (Tamil Nadu 38-District Catalog)"
                return {
                    "destination": data["city"],
                    "country": data["country"],
                    "latitude": data["lat"],
                    "longitude": data["lng"],
                    "places": data["places"],
                    "is_curated": True,
                    "source": source_lbl
                }
        
        # Try live geocoding via OpenStreetMap Nominatim with bounded timeout
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                headers = {"User-Agent": "TriporaAI-TravelPlanner/1.0"}
                resp = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": destination_name, "format": "json", "limit": 1},
                    headers=headers
                )
                if resp.status_code == 200 and resp.json():
                    loc = resp.json()[0]
                    lat = float(loc.get("lat", 0.0))
                    lon = float(loc.get("lon", 0.0))
                    generated_places = self._generate_generic_places(destination_name, lat, lon)
                    return {
                        "destination": loc.get("display_name", destination_name).split(",")[0],
                        "country": loc.get("display_name", "").split(",")[-1].strip(),
                        "latitude": lat,
                        "longitude": lon,
                        "places": generated_places,
                        "is_curated": False,
                        "source": "OpenStreetMap Nominatim Geocoding + Synthetic POI Model"
                    }
        except Exception:
            pass
            
        # Fallback to realistic default coordinates
        def_lat, def_lon = 20.5937, 78.9629
        return {
            "destination": destination_name.title(),
            "country": "International",
            "latitude": def_lat,
            "longitude": def_lon,
            "places": self._generate_generic_places(destination_name, def_lat, def_lon),
            "is_curated": False,
            "source": "TRIPORA Synthetic Destination Model (Demo Mode)"
        }

    def _generate_generic_places(self, dest: str, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Generate structured POIs around given coordinates when destination is outside curated catalog."""
        templates = [
            ("Old Town & Historic Square", "Culture", False, 2.5, 200, 0.005, 0.004, "Historic architectural center with pedestrian squares and landmark monuments."),
            ("Central Cultural Museum", "Culture", False, 2.0, 350, -0.003, 0.006, "Primary municipal museum displaying regional history, archaeology and fine arts."),
            ("City Panoramic Viewpoint & Gardens", "Sightseeing", True, 2.0, 100, 0.012, -0.008, "Elevated scenic viewpoint providing sweeping horizon views across the city."),
            ("Artisans Bazaar & Market Street", "Food", True, 2.5, 250, -0.008, -0.005, "Lively commercial corridor featuring local street food, crafts, and specialty shops."),
            ("Riverside / Coastal Esplanade Walk", "Nature", True, 2.0, 0, 0.009, 0.011, "Paved waterfront promenade with outdoor cafes and scenic walking paths."),
            ("Botanical Gardens & Conservatory", "Nature", True, 2.0, 150, -0.015, 0.002, "Landscaped urban sanctuary featuring exotic flora and peaceful walking trails."),
            ("Heritage Cathedral & Bell Tower", "Culture", False, 1.5, 100, 0.002, -0.004, "Centuries-old stone cathedral known for sacred art and architectural masonry."),
            ("Evening Twilight Food Tour", "Food", True, 2.5, 600, -0.002, 0.003, "Guided culinary exploration through regional street delicacies and iconic bistros.")
        ]
        results = []
        for name, cat, is_out, dur, cost, dlat, dlon, desc in templates:
            results.append({
                "name": f"{dest.title()} {name}",
                "category": cat,
                "lat": round(lat + dlat, 5),
                "lng": round(lon + dlon, 5),
                "is_outdoor": is_out,
                "duration": dur,
                "cost": cost,
                "desc": desc
            })
        return results


def resolve_destination_district(destination_name: str) -> Optional[str]:
    """Resolve a destination name or town alias to a normalized Tamil Nadu district key, or None."""
    norm = destination_name.strip().lower()
    if norm in TN_DISTRICT_ALIASES:
        return TN_DISTRICT_ALIASES[norm]
    if norm in TAMIL_NADU_DISTRICTS:
        return norm
    for dist_key in TAMIL_NADU_DISTRICTS:
        if dist_key in norm or norm in dist_key:
            return dist_key
    return None


def get_places_for_destination(destination_name: str) -> List[Dict[str, Any]]:
    """Retrieve verified places for a destination, checking district aliases and catalog."""
    dist_key = resolve_destination_district(destination_name)
    if dist_key and dist_key in TAMIL_NADU_DISTRICTS:
        return TAMIL_NADU_DISTRICTS[dist_key]["places"]
    norm = destination_name.strip().lower()
    if norm in DESTINATION_CATALOG:
        return DESTINATION_CATALOG[norm]["places"]
    for key, data in DESTINATION_CATALOG.items():
        if key in norm or norm in key:
            return data["places"]
    return []


geo_places_provider = GeoPlacesProvider()

from typing import Dict, Any, Optional, Set, Tuple

# Verified active commercial passenger airports with regular scheduled commercial flights
# Key is normalized lowercase city/region name
VERIFIED_AIRPORTS: Dict[str, Dict[str, Any]] = {
    "chennai": {
        "iata": "MAA",
        "name": "Chennai International Airport",
        "city": "Chennai",
        "country": "India",
        "lat": 12.9941,
        "lng": 80.1709,
        "is_international": True,
        "active_commercial": True
    },
    "madurai": {
        "iata": "IXM",
        "name": "Madurai International Airport",
        "city": "Madurai",
        "country": "India",
        "lat": 9.8345,
        "lng": 78.0934,
        "is_international": True,
        "active_commercial": True
    },
    "coimbatore": {
        "iata": "CJB",
        "name": "Coimbatore International Airport",
        "city": "Coimbatore",
        "country": "India",
        "lat": 11.0299,
        "lng": 77.0434,
        "is_international": True,
        "active_commercial": True
    },
    "tiruchirappalli": {
        "iata": "TRZ",
        "name": "Tiruchirappalli International Airport",
        "city": "Tiruchirappalli",
        "country": "India",
        "lat": 10.7654,
        "lng": 78.7097,
        "is_international": True,
        "active_commercial": True
    },
    "trichy": {
        "iata": "TRZ",
        "name": "Tiruchirappalli International Airport",
        "city": "Tiruchirappalli",
        "country": "India",
        "lat": 10.7654,
        "lng": 78.7097,
        "is_international": True,
        "active_commercial": True
    },
    "thoothukudi": {
        "iata": "TCR",
        "name": "Tuticorin Airport",
        "city": "Thoothukudi",
        "country": "India",
        "lat": 8.7236,
        "lng": 78.0264,
        "is_international": False,
        "active_commercial": True
    },
    "tuticorin": {
        "iata": "TCR",
        "name": "Tuticorin Airport",
        "city": "Thoothukudi",
        "country": "India",
        "lat": 8.7236,
        "lng": 78.0264,
        "is_international": False,
        "active_commercial": True
    },
    "salem": {
        "iata": "SXV",
        "name": "Salem Airport (UDAN Regional)",
        "city": "Salem",
        "country": "India",
        "lat": 11.7833,
        "lng": 78.0647,
        "is_international": False,
        "active_commercial": True
    },
    "bangalore": {
        "iata": "BLR",
        "name": "Kempegowda International Airport",
        "city": "Bengaluru",
        "country": "India",
        "lat": 13.1986,
        "lng": 77.7066,
        "is_international": True,
        "active_commercial": True
    },
    "bengaluru": {
        "iata": "BLR",
        "name": "Kempegowda International Airport",
        "city": "Bengaluru",
        "country": "India",
        "lat": 13.1986,
        "lng": 77.7066,
        "is_international": True,
        "active_commercial": True
    },
    "mumbai": {
        "iata": "BOM",
        "name": "Chhatrapati Shivaji Maharaj International Airport",
        "city": "Mumbai",
        "country": "India",
        "lat": 19.0896,
        "lng": 72.8656,
        "is_international": True,
        "active_commercial": True
    },
    "delhi": {
        "iata": "DEL",
        "name": "Indira Gandhi International Airport",
        "city": "New Delhi",
        "country": "India",
        "lat": 28.5562,
        "lng": 77.1000,
        "is_international": True,
        "active_commercial": True
    },
    "hyderabad": {
        "iata": "HYD",
        "name": "Rajiv Gandhi International Airport",
        "city": "Hyderabad",
        "country": "India",
        "lat": 17.2403,
        "lng": 78.4294,
        "is_international": True,
        "active_commercial": True
    },
    "kolkata": {
        "iata": "CCU",
        "name": "Netaji Subhash Chandra Bose International Airport",
        "city": "Kolkata",
        "country": "India",
        "lat": 22.6547,
        "lng": 88.4467,
        "is_international": True,
        "active_commercial": True
    },
    "goa": {
        "iata": "GOI",
        "name": "Dabolim / Manohar International Airport (MOPA)",
        "city": "Goa",
        "country": "India",
        "lat": 15.3808,
        "lng": 73.8314,
        "is_international": True,
        "active_commercial": True
    },
    "kochi": {
        "iata": "COK",
        "name": "Cochin International Airport",
        "city": "Kochi",
        "country": "India",
        "lat": 10.1518,
        "lng": 76.3930,
        "is_international": True,
        "active_commercial": True
    },
    "jaipur": {
        "iata": "JAI",
        "name": "Jaipur International Airport",
        "city": "Jaipur",
        "country": "India",
        "lat": 26.8242,
        "lng": 75.8122,
        "is_international": True,
        "active_commercial": True
    },
    "pune": {
        "iata": "PNQ",
        "name": "Pune International Airport",
        "city": "Pune",
        "country": "India",
        "lat": 18.5822,
        "lng": 73.9197,
        "is_international": True,
        "active_commercial": True
    },
    "ahmedabad": {
        "iata": "AMD",
        "name": "Sardar Vallabhbhai Patel International Airport",
        "city": "Ahmedabad",
        "country": "India",
        "lat": 23.0734,
        "lng": 72.6347,
        "is_international": True,
        "active_commercial": True
    },
    "london": {
        "iata": "LHR",
        "name": "London Heathrow Airport",
        "city": "London",
        "country": "United Kingdom",
        "lat": 51.4700,
        "lng": -0.4543,
        "is_international": True,
        "active_commercial": True
    },
    "paris": {
        "iata": "CDG",
        "name": "Paris Charles de Gaulle Airport",
        "city": "Paris",
        "country": "France",
        "lat": 49.0097,
        "lng": 2.5479,
        "is_international": True,
        "active_commercial": True
    },
    "tokyo": {
        "iata": "HND",
        "name": "Tokyo Haneda / Narita International Airport",
        "city": "Tokyo",
        "country": "Japan",
        "lat": 35.5494,
        "lng": 139.7798,
        "is_international": True,
        "active_commercial": True
    },
    "dubai": {
        "iata": "DXB",
        "name": "Dubai International Airport",
        "city": "Dubai",
        "country": "United Arab Emirates",
        "lat": 25.2532,
        "lng": 55.3657,
        "is_international": True,
        "active_commercial": True
    },
    "singapore": {
        "iata": "SIN",
        "name": "Singapore Changi Airport",
        "city": "Singapore",
        "country": "Singapore",
        "lat": 1.3644,
        "lng": 103.9915,
        "is_international": True,
        "active_commercial": True
    },
    "new york": {
        "iata": "JFK",
        "name": "John F. Kennedy International Airport",
        "city": "New York",
        "country": "United States",
        "lat": 40.6413,
        "lng": -73.7781,
        "is_international": True,
        "active_commercial": True
    }
}

# Verified Railway Stations for key destinations
VERIFIED_STATIONS: Dict[str, Dict[str, Any]] = {
    "chennai": {
        "code": "MAS / MS",
        "name": "Chennai Central (MAS) & Chennai Egmore (MS)",
        "hub_type": "Major Terminal"
    },
    "tiruvannamalai": {
        "code": "TNM",
        "name": "Tiruvannamalai Railway Station (TNM)",
        "hub_type": "Regional Junction (Southern Railway)"
    },
    "madurai": {
        "code": "MDU",
        "name": "Madurai Junction (MDU)",
        "hub_type": "Divisional Superfast Terminal"
    },
    "coimbatore": {
        "code": "CBE",
        "name": "Coimbatore Junction (CBE)",
        "hub_type": "Major Terminal"
    },
    "tiruchirappalli": {
        "code": "TPJ",
        "name": "Tiruchirappalli Junction (TPJ)",
        "hub_type": "Divisional Superfast Terminal"
    },
    "trichy": {
        "code": "TPJ",
        "name": "Tiruchirappalli Junction (TPJ)",
        "hub_type": "Divisional Superfast Terminal"
    },
    "thanjavur": {
        "code": "TJ",
        "name": "Thanjavur Junction (TJ)",
        "hub_type": "Mainline Station"
    },
    "kanyakumari": {
        "code": "CAPE",
        "name": "Kanyakumari Terminus (CAPE)",
        "hub_type": "Terminus Station"
    },
    "salem": {
        "code": "SA",
        "name": "Salem Junction (SA)",
        "hub_type": "Divisional Superfast Terminal"
    },
    "nilgiris": {
        "code": "UAM",
        "name": "Udagamandalam (Ooty) Railway Station / MTP (Mettupalayam)",
        "hub_type": "Mountain Heritage Railway"
    },
    "ooty": {
        "code": "UAM",
        "name": "Udagamandalam (Ooty) Railway Station / MTP",
        "hub_type": "Mountain Heritage Railway"
    },
    "dindigul": {
        "code": "DG",
        "name": "Dindigul Junction (DG)",
        "hub_type": "Mainline Junction"
    },
    "kodaikanal": {
        "code": "KQN",
        "name": "Kodaikanal Road (KQN) [Overland road transfer up to hills]",
        "hub_type": "Railhead with Bus Link"
    },
    "ramanathapuram": {
        "code": "RMM",
        "name": "Rameswaram Railway Station (RMM)",
        "hub_type": "Island Terminus"
    },
    "rameswaram": {
        "code": "RMM",
        "name": "Rameswaram Railway Station (RMM)",
        "hub_type": "Island Terminus"
    },
    "tenkasi": {
        "code": "TSI",
        "name": "Tenkasi Junction (TSI)",
        "hub_type": "Branch Line Junction"
    },
    "tirunelveli": {
        "code": "TEN",
        "name": "Tirunelveli Junction (TEN)",
        "hub_type": "Divisional Station"
    },
    "mumbai": {
        "code": "CSMT / BCT",
        "name": "Chhatrapati Shivaji Maharaj Terminus (CSMT)",
        "hub_type": "Major Terminal"
    },
    "delhi": {
        "code": "NDLS / DLI",
        "name": "New Delhi Railway Station (NDLS)",
        "hub_type": "National Hub"
    },
    "bangalore": {
        "code": "SBC / YPR",
        "name": "KSR Bengaluru City (SBC) & Yesvantpur (YPR)",
        "hub_type": "Major Terminal"
    },
    "bengaluru": {
        "code": "SBC / YPR",
        "name": "KSR Bengaluru City (SBC)",
        "hub_type": "Major Terminal"
    },
    "goa": {
        "code": "MAO",
        "name": "Madgaon Junction (MAO)",
        "hub_type": "Konkan Railway Terminal"
    },
    "jaipur": {
        "code": "JP",
        "name": "Jaipur Junction (JP)",
        "hub_type": "Major Terminal"
    }
}

# Major known intercity passenger flight corridors (direct scheduled pairs)
# Set of frozensets of lowercase city names
DIRECT_FLIGHT_PAIRS: Set[frozenset] = {
    frozenset(["chennai", "madurai"]),
    frozenset(["chennai", "coimbatore"]),
    frozenset(["chennai", "tiruchirappalli"]),
    frozenset(["chennai", "trichy"]),
    frozenset(["chennai", "thoothukudi"]),
    frozenset(["chennai", "tuticorin"]),
    frozenset(["chennai", "salem"]),
    frozenset(["chennai", "bangalore"]),
    frozenset(["chennai", "bengaluru"]),
    frozenset(["chennai", "mumbai"]),
    frozenset(["chennai", "delhi"]),
    frozenset(["chennai", "hyderabad"]),
    frozenset(["chennai", "kolkata"]),
    frozenset(["chennai", "goa"]),
    frozenset(["chennai", "kochi"]),
    frozenset(["chennai", "pune"]),
    frozenset(["chennai", "ahmedabad"]),
    frozenset(["chennai", "jaipur"]),
    frozenset(["chennai", "dubai"]),
    frozenset(["chennai", "singapore"]),
    frozenset(["mumbai", "delhi"]),
    frozenset(["mumbai", "goa"]),
    frozenset(["mumbai", "bangalore"]),
    frozenset(["delhi", "jaipur"]),
    frozenset(["delhi", "goa"]),
    frozenset(["bangalore", "goa"]),
    frozenset(["bangalore", "madurai"]),
    frozenset(["bangalore", "coimbatore"]),
}

# Known intercontinental pairs (direct or standard 1-stop scheduled flights)
INTERNATIONAL_HUBS: Set[str] = {"london", "paris", "tokyo", "dubai", "singapore", "new york"}

def is_overland_contiguous(orig: str, dest: str) -> bool:
    """Determine whether two locations are on contiguous land reachable by road or rail."""
    o = orig.strip().lower()
    d = dest.strip().lower()
    
    # If one is in an overseas/intercontinental zone and the other is in India, overland is impossible
    is_o_intl = o in INTERNATIONAL_HUBS
    is_d_intl = d in INTERNATIONAL_HUBS

    if is_o_intl != is_d_intl:
        return False
    if is_o_intl and is_d_intl:
        # e.g., London to Paris is overland via Eurostar/Tunnel, but London to Tokyo is not
        if (o == "london" and d == "paris") or (o == "paris" and d == "london"):
            return True
        return False
        
    return True

def get_verified_airport(city_name: str) -> Optional[Dict[str, Any]]:
    """Look up verified active commercial airport for a city or region."""
    norm = city_name.strip().lower()
    for key, data in VERIFIED_AIRPORTS.items():
        if key == norm or key in norm or norm in key:
            return data
    return None

def get_verified_station(city_name: str) -> Optional[Dict[str, Any]]:
    """Look up verified railway station for a city or region."""
    norm = city_name.strip().lower()
    for key, data in VERIFIED_STATIONS.items():
        if key == norm or key in norm or norm in key:
            return data
    return None

from typing import Dict, Any, Optional, Set, Tuple

# ==============================================================================
# 1. VERIFIED COMMERCIAL PASSENGER AIRPORTS (Certified Active Passenger Hubs)
# ==============================================================================
# Only locations with regular, scheduled commercial passenger flights appear here.
# Key is normalized lowercase city/region name or district alias.
VERIFIED_AIRPORTS: Dict[str, Dict[str, Any]] = {
    # Tamil Nadu Commercial Airports
    "chennai": {
        "iata": "MAA",
        "name": "Chennai International Airport",
        "city": "Chennai",
        "state": "Tamil Nadu",
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
        "state": "Tamil Nadu",
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
        "state": "Tamil Nadu",
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
        "state": "Tamil Nadu",
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
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.7654,
        "lng": 78.7097,
        "is_international": True,
        "active_commercial": True
    },
    "thoothukudi": {
        "iata": "TCR",
        "name": "Tuticorin Domestic Airport",
        "city": "Thoothukudi",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.7236,
        "lng": 78.0264,
        "is_international": False,
        "active_commercial": True
    },
    "tuticorin": {
        "iata": "TCR",
        "name": "Tuticorin Domestic Airport",
        "city": "Thoothukudi",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.7236,
        "lng": 78.0264,
        "is_international": False,
        "active_commercial": True
    },
    "salem": {
        "iata": "SXV",
        "name": "Salem Airport (UDAN Regional Scheduled)",
        "city": "Salem",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.7833,
        "lng": 78.0647,
        "is_international": False,
        "active_commercial": True
    },

    # Indian Metro & Tier-1 Hubs
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
        "iata": "GOI / GOX",
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

    # International Gateways
    "london": {
        "iata": "LHR / LGW",
        "name": "London Heathrow Airport (LHR)",
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
        "iata": "HND / NRT",
        "name": "Tokyo Haneda & Narita International Airport",
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
        "iata": "JFK / EWR",
        "name": "John F. Kennedy International Airport",
        "city": "New York",
        "country": "United States",
        "lat": 40.6413,
        "lng": -73.7781,
        "is_international": True,
        "active_commercial": True
    }
}

# ==============================================================================
# 2. VERIFIED RAILWAY STATIONS (ALL 38 TAMIL NADU DISTRICTS + NATIONAL HUBS)
# ==============================================================================
VERIFIED_STATIONS: Dict[str, Dict[str, Any]] = {
    # 1. Ariyalur
    "ariyalur": {
        "code": "ALU",
        "name": "Ariyalur Railway Station (ALU)",
        "hub_type": "Chord Line Mainline (Southern Railway)"
    },
    # 2. Chengalpattu
    "chengalpattu": {
        "code": "CGL",
        "name": "Chengalpattu Junction (CGL)",
        "hub_type": "Major Railway Junction (Southern Railway)"
    },
    "mahabalipuram": {
        "code": "CGL",
        "name": "Chengalpattu Junction (CGL) [28 km Road Link to Shore Temple]",
        "hub_type": "Railhead with Direct Highway Link"
    },
    # 3. Chennai
    "chennai": {
        "code": "MAS / MS",
        "name": "Chennai Central (MAS) & Chennai Egmore (MS)",
        "hub_type": "Premier Intercity Superfast Terminal"
    },
    # 4. Coimbatore
    "coimbatore": {
        "code": "CBE",
        "name": "Coimbatore Junction (CBE)",
        "hub_type": "Premier Divisional Superfast Terminal"
    },
    # 5. Cuddalore
    "cuddalore": {
        "code": "CUPJ / COT",
        "name": "Cuddalore Port Junction (CUPJ)",
        "hub_type": "Mainline Coastal Junction"
    },
    # 6. Dharmapuri
    "dharmapuri": {
        "code": "DPJ",
        "name": "Dharmapuri Railway Station (DPJ)",
        "hub_type": "Bengaluru-Salem Line Station"
    },
    # 7. Dindigul
    "dindigul": {
        "code": "DG",
        "name": "Dindigul Junction (DG)",
        "hub_type": "Divisional Superfast Junction"
    },
    "kodaikanal": {
        "code": "KQN",
        "name": "Kodaikanal Road (KQN) [Scenic Hill Ghat Road Transfer]",
        "hub_type": "Hill Station Railhead"
    },
    "kodai": {
        "code": "KQN",
        "name": "Kodaikanal Road (KQN)",
        "hub_type": "Hill Station Railhead"
    },
    # 8. Erode
    "erode": {
        "code": "ED",
        "name": "Erode Junction (ED)",
        "hub_type": "Major Quadruple-Line Junction with Diesel Loco Shed"
    },
    # 9. Kallakurichi
    "kallakurichi": {
        "code": "CHSM / VM",
        "name": "Chinnasalem Railway Station (CHSM)",
        "hub_type": "Salem-Vriddhachalam Branch Line"
    },
    # 10. Kanchipuram
    "kanchipuram": {
        "code": "CJ",
        "name": "Kanchipuram Railway Station (CJ)",
        "hub_type": "Arakkonam-Chengalpattu Branch Line"
    },
    # 11. Kanyakumari
    "kanyakumari": {
        "code": "CAPE / NCJ",
        "name": "Kanyakumari Terminus (CAPE) & Nagercoil Junction (NCJ)",
        "hub_type": "Southernmost National Railway Terminus"
    },
    # 12. Karur
    "karur": {
        "code": "KRR",
        "name": "Karur Junction (KRR)",
        "hub_type": "Major Industrial Junction"
    },
    # 13. Krishnagiri
    "krishnagiri": {
        "code": "HSRA / DPJ",
        "name": "Hosur Railway Station (HSRA) & Dharmapuri (DPJ)",
        "hub_type": "Bengaluru Sub-Corridor Railhead"
    },
    # 14. Madurai
    "madurai": {
        "code": "MDU",
        "name": "Madurai Junction (MDU)",
        "hub_type": "Premier Divisional Superfast Terminal"
    },
    # 15. Mayiladuthurai
    "mayiladuthurai": {
        "code": "MV",
        "name": "Mayiladuthurai Junction (MV)",
        "hub_type": "Kaveri Delta Mainline Junction"
    },
    "tranquebar": {
        "code": "MV",
        "name": "Mayiladuthurai Junction (MV) [Danish Fort Link]",
        "hub_type": "Railhead with Coastal Road Transfer"
    },
    # 16. Nagapattinam
    "nagapattinam": {
        "code": "NGT / VLNK",
        "name": "Nagapattinam Junction (NGT) & Velankanni (VLNK)",
        "hub_type": "Coastal Pilgrimage Terminal"
    },
    "velankanni": {
        "code": "VLNK",
        "name": "Velankanni Railway Station (VLNK)",
        "hub_type": "Basilica Dedicated Pilgrimage Station"
    },
    # 17. Namakkal
    "namakkal": {
        "code": "NMKL",
        "name": "Namakkal Railway Station (NMKL)",
        "hub_type": "Salem-Karur Broad Gauge Line"
    },
    "kolli hills": {
        "code": "NMKL",
        "name": "Namakkal Railway Station (NMKL) [Ghat Road to Agaya Gangai]",
        "hub_type": "Railhead with 70 Hairpin Ghat Link"
    },
    # 18. Nilgiris
    "nilgiris": {
        "code": "UAM / MTP",
        "name": "Udagamandalam (Ooty UAM) & Mettupalayam (MTP)",
        "hub_type": "UNESCO World Heritage Mountain Railway"
    },
    "ooty": {
        "code": "UAM / MTP",
        "name": "Udagamandalam (Ooty UAM) & Mettupalayam (MTP)",
        "hub_type": "UNESCO World Heritage Mountain Railway"
    },
    # 19. Perambalur
    "perambalur": {
        "code": "ALU",
        "name": "Ariyalur Railhead (ALU) [30 km Highway Transfer to Perambalur]",
        "hub_type": "Mainline Railhead Link"
    },
    # 20. Pudukkottai
    "pudukkottai": {
        "code": "PDKT",
        "name": "Pudukkottai Railway Station (PDKT)",
        "hub_type": "Trichy-Karaikkudi Mainline"
    },
    # 21. Ramanathapuram
    "ramanathapuram": {
        "code": "RMD / RMM",
        "name": "Ramanathapuram (RMD) & Rameswaram Island (RMM)",
        "hub_type": "Sea Bridge Island Line"
    },
    "rameswaram": {
        "code": "RMM",
        "name": "Rameswaram Railway Station (RMM)",
        "hub_type": "Pamban Sea Bridge Island Terminus"
    },
    # 22. Ranipet
    "ranipet": {
        "code": "WJR / KPD",
        "name": "Walajah Road Junction (WJR) & Katpadi (KPD)",
        "hub_type": "Chennai-Bengaluru Mainline Hub"
    },
    # 23. Salem
    "salem": {
        "code": "SA",
        "name": "Salem Junction (SA)",
        "hub_type": "Divisional Superfast Junction"
    },
    "yercaud": {
        "code": "SA",
        "name": "Salem Junction (SA) [32 km Ghat Road to Yercaud]",
        "hub_type": "Hill Station Railhead"
    },
    # 24. Sivagangai
    "sivagangai": {
        "code": "SVGA / KKDI",
        "name": "Sivaganga (SVGA) & Karaikkudi Junction (KKDI)",
        "hub_type": "Chettinad Heritage Rail Hub"
    },
    "chettinad": {
        "code": "KKDI / SVGA",
        "name": "Karaikkudi Junction (KKDI) & Kanadukathan",
        "hub_type": "Chettinad Heritage Junction"
    },
    # 25. Tenkasi
    "tenkasi": {
        "code": "TSI",
        "name": "Tenkasi Junction (TSI)",
        "hub_type": "Kollam-Sengottai-Madurai Line"
    },
    "courtallam": {
        "code": "TSI",
        "name": "Tenkasi Junction (TSI) [6 km Link to Courtallam Waterfalls]",
        "hub_type": "Waterfalls Gateway Junction"
    },
    # 26. Thanjavur
    "thanjavur": {
        "code": "TJ",
        "name": "Thanjavur Junction (TJ)",
        "hub_type": "Great Living Chola Mainline Station"
    },
    # 27. Theni
    "theni": {
        "code": "TENI",
        "name": "Theni Railway Station (TENI)",
        "hub_type": "Madurai-Bodinaickanur Broad Gauge Line"
    },
    "megamalai": {
        "code": "TENI",
        "name": "Theni Railway Station (TENI) [Mountain Road to Megamalai]",
        "hub_type": "Cloud Mountain Railhead"
    },
    # 28. Thoothukudi
    "thoothukudi": {
        "code": "TN / MEJ",
        "name": "Tuticorin Terminus (TN) & Vanchi Maniyachchi (MEJ)",
        "hub_type": "Port City Railway Terminus"
    },
    # 29. Tiruchirappalli
    "tiruchirappalli": {
        "code": "TPJ",
        "name": "Tiruchirappalli Junction (TPJ)",
        "hub_type": "Premier Central Tamil Nadu Superfast Terminal"
    },
    "trichy": {
        "code": "TPJ",
        "name": "Tiruchirappalli Junction (TPJ)",
        "hub_type": "Premier Central Tamil Nadu Superfast Terminal"
    },
    # 30. Tirunelveli
    "tirunelveli": {
        "code": "TEN",
        "name": "Tirunelveli Junction (TEN)",
        "hub_type": "Divisional Superfast Junction"
    },
    # 31. Tirupathur
    "tirupathur": {
        "code": "TPT / JTJ",
        "name": "Tirupathur (TPT) & Jolarpettai Junction (JTJ)",
        "hub_type": "Major Intercity Quad-Track Junction"
    },
    "yelagiri": {
        "code": "JTJ",
        "name": "Jolarpettai Junction (JTJ) [21 km Ghat Road to Yelagiri]",
        "hub_type": "Yelagiri Hills Gateway Railhead"
    },
    # 32. Tiruppur
    "tiruppur": {
        "code": "TUP",
        "name": "Tiruppur Railway Station (TUP)",
        "hub_type": "Mainline Industrial Superfast Station"
    },
    # 33. Tiruvallur
    "tiruvallur": {
        "code": "TRL",
        "name": "Tiruvallur Railway Station (TRL)",
        "hub_type": "Chennai Suburban & Mainline Hub"
    },
    # 34. Tiruvannamalai
    "tiruvannamalai": {
        "code": "TNM",
        "name": "Tiruvannamalai Railway Station (TNM)",
        "hub_type": "Villupuram-Katpadi Chord Line (Southern Railway)"
    },
    # 35. Tiruvarur
    "tiruvarur": {
        "code": "TVR",
        "name": "Tiruvarur Junction (TVR)",
        "hub_type": "Kaveri Delta Railway Junction"
    },
    # 36. Vellore
    "vellore": {
        "code": "KPD / VLR",
        "name": "Katpadi Junction (KPD) & Vellore Cantonment (VLR)",
        "hub_type": "Major Intercity Quad-Track Superfast Junction"
    },
    # 37. Viluppuram
    "viluppuram": {
        "code": "VM",
        "name": "Villupuram Junction (VM)",
        "hub_type": "Major Quadruple-Line Southern Railway Junction"
    },
    "villupuram": {
        "code": "VM",
        "name": "Villupuram Junction (VM)",
        "hub_type": "Major Quadruple-Line Southern Railway Junction"
    },
    "gingee": {
        "code": "VM",
        "name": "Villupuram Junction (VM) [28 km Highway Link to Gingee Fort]",
        "hub_type": "Fortress Gateway Railhead"
    },
    # 38. Virudhunagar
    "virudhunagar": {
        "code": "VPT",
        "name": "Virudhunagar Junction (VPT)",
        "hub_type": "Mainline Southern Railway Junction"
    },
    "srivilliputhur": {
        "code": "SVPR",
        "name": "Srivilliputtur Railway Station (SVPR)",
        "hub_type": "Andal Temple Pilgrimage Station"
    },

    # National Hubs
    "mumbai": {
        "code": "CSMT / BCT",
        "name": "Chhatrapati Shivaji Maharaj Terminus (CSMT)",
        "hub_type": "Premier National Terminal"
    },
    "delhi": {
        "code": "NDLS / NZM",
        "name": "New Delhi Railway Station (NDLS)",
        "hub_type": "Premier National Hub"
    },
    "bangalore": {
        "code": "SBC / YPR",
        "name": "KSR Bengaluru City (SBC) & Yesvantpur (YPR)",
        "hub_type": "Major Superfast Terminal"
    },
    "bengaluru": {
        "code": "SBC / YPR",
        "name": "KSR Bengaluru City (SBC)",
        "hub_type": "Major Superfast Terminal"
    },
    "hyderabad": {
        "code": "SC / HYB",
        "name": "Secunderabad Junction (SC) & Hyderabad (HYB)",
        "hub_type": "South Central Railway Hub"
    },
    "kolkata": {
        "code": "HWH / SDAH",
        "name": "Howrah Junction (HWH) & Sealdah (SDAH)",
        "hub_type": "Eastern Railway Mega-Hub"
    },
    "goa": {
        "code": "MAO / THVM",
        "name": "Madgaon Junction (MAO) & Thivim (THVM)",
        "hub_type": "Konkan Railway Terminal"
    },
    "kochi": {
        "code": "ERS / ERN",
        "name": "Ernakulam Junction (ERS) & Town (ERN)",
        "hub_type": "Southern Railway Major Terminal"
    },
    "jaipur": {
        "code": "JP",
        "name": "Jaipur Junction (JP)",
        "hub_type": "North Western Railway Hub"
    },
    "pune": {
        "code": "PUNE",
        "name": "Pune Junction (PUNE)",
        "hub_type": "Central Railway Superfast Hub"
    },
    "ahmedabad": {
        "code": "ADI",
        "name": "Ahmedabad Junction (ADI)",
        "hub_type": "Western Railway Major Terminal"
    }
}

# ==============================================================================
# 3. VERIFIED BUS TERMINALS (ALL 38 TAMIL NADU DISTRICTS + NATIONAL HUBS)
# ==============================================================================
VERIFIED_BUS_TERMINALS: Dict[str, str] = {
    "chennai": "Chennai Kilambakkam (KCBT) & Koyambedu (CMBT)",
    "tiruvannamalai": "Tiruvannamalai Central Bus Stand (NH 48 / SH 9 Corridor)",
    "madurai": "Madurai Integrated Mattuthavani Bus Terminal (MIBT)",
    "coimbatore": "Coimbatore Gandhipuram & Singanallur Central Bus Stand",
    "tiruchirappalli": "Trichy Central Bus Stand & Chathiram Terminal",
    "trichy": "Trichy Central Bus Stand & Chathiram Terminal",
    "thanjavur": "Thanjavur New Central Bus Stand (Near Medical College)",
    "kanyakumari": "Kanyakumari Express Bus Terminus & Nagercoil Christopher Stand",
    "salem": "Salem Central New Bus Stand (MGR Terminal)",
    "nilgiris": "Ooty ATC Municipal Central Bus Terminal",
    "ooty": "Ooty ATC Municipal Central Bus Terminal",
    "dindigul": "Dindigul Central Bus Stand",
    "kodaikanal": "Kodaikanal Municipal Hill Bus Stand",
    "ramanathapuram": "Ramanathapuram Central Bus Stand",
    "rameswaram": "Rameswaram Temple & Town Express Bus Stand",
    "tenkasi": "Tenkasi Central Bus Stand & Courtallam Terminal",
    "tirunelveli": "Tirunelveli New Bus Stand (Vaeinthaankulam)",
    "erode": "Erode Central Bus Stand",
    "tiruppur": "Tiruppur New Bus Stand (Pushpa Theatre)",
    "kanchipuram": "Kanchipuram Central Bus Stand",
    "chengalpattu": "Chengalpattu New Bus Stand",
    "mahabalipuram": "Mahabalipuram ECR Coastal Bus Stand",
    "vellore": "Vellore New Central Bus Stand (Chelliamman Koil)",
    "ranipet": "Ranipet & Walajah Bus Stand",
    "tirupathur": "Tirupathur Central Bus Stand",
    "yelagiri": "Yelagiri Athanavur Hill Bus Terminal",
    "dharmapuri": "Dharmapuri Central Bus Stand",
    "krishnagiri": "Krishnagiri Central Bus Stand",
    "namakkal": "Namakkal Central Bus Stand",
    "karur": "Karur Central Bus Stand",
    "pudukkottai": "Pudukkottai Central Bus Stand",
    "sivagangai": "Sivagangai & Karaikkudi New Bus Stand",
    "chettinad": "Karaikkudi New Bus Stand & Kanadukathan Stop",
    "theni": "Theni Central Bus Stand",
    "thoothukudi": "Thoothukudi New Bus Stand",
    "cuddalore": "Cuddalore Central Bus Stand",
    "villupuram": "Villupuram Central Bus Stand",
    "viluppuram": "Villupuram Central Bus Stand",
    "gingee": "Gingee Fort Bus Stand",
    "kallakurichi": "Kallakurichi Central Bus Stand",
    "nagapattinam": "Nagapattinam Central Bus Stand",
    "velankanni": "Velankanni Basilica Express Bus Terminal",
    "mayiladuthurai": "Mayiladuthurai Central Bus Stand",
    "tiruvarur": "Tiruvarur Central Bus Stand",
    "ariyalur": "Ariyalur Central Bus Stand",
    "perambalur": "Perambalur New Bus Stand",
    "tiruvallur": "Tiruvallur Central Bus Stand",
    "virudhunagar": "Virudhunagar Central Bus Stand",
    "srivilliputhur": "Srivilliputhur Town Bus Stand",
    "bangalore": "Kempegowda Bus Station (Majestic SBC) & Shantinagar",
    "bengaluru": "Kempegowda Bus Station (Majestic SBC)",
    "mumbai": "Mumbai Central MSRTC Bus Station",
    "delhi": "ISBT Kashmere Gate & Anand Vihar",
    "goa": "Panaji Kadamba Central Bus Stand & Madgaon KTC",
    "kochi": "Kochi KSRTC Central Bus Stand & Vyttila Mobility Hub",
    "jaipur": "Sindhi Camp Central Bus Stand"
}

# ==============================================================================
# 4. DIRECT COMMERCIAL PASSENGER FLIGHT CORRIDORS
# ==============================================================================
DIRECT_FLIGHT_PAIRS: Set[frozenset] = {
    # Tamil Nadu Commercial Hub Connections
    frozenset(["chennai", "madurai"]),
    frozenset(["chennai", "coimbatore"]),
    frozenset(["chennai", "tiruchirappalli"]),
    frozenset(["chennai", "trichy"]),
    frozenset(["chennai", "thoothukudi"]),
    frozenset(["chennai", "tuticorin"]),
    frozenset(["chennai", "salem"]),
    # South Indian & National Connections
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
    frozenset(["bangalore", "madurai"]),
    frozenset(["bangalore", "coimbatore"]),
    frozenset(["bangalore", "tiruchirappalli"]),
    frozenset(["bangalore", "trichy"]),
    frozenset(["bangalore", "thoothukudi"]),
    frozenset(["bangalore", "tuticorin"]),
    frozenset(["bangalore", "goa"]),
    frozenset(["bangalore", "mumbai"]),
    frozenset(["bangalore", "delhi"]),
    frozenset(["mumbai", "madurai"]),
    frozenset(["mumbai", "coimbatore"]),
    frozenset(["mumbai", "delhi"]),
    frozenset(["mumbai", "goa"]),
    frozenset(["delhi", "coimbatore"]),
    frozenset(["delhi", "jaipur"]),
    frozenset(["delhi", "goa"]),
    # International Direct Gateways
    frozenset(["chennai", "dubai"]),
    frozenset(["chennai", "singapore"]),
    frozenset(["chennai", "london"]),
    frozenset(["madurai", "dubai"]),
    frozenset(["madurai", "singapore"]),
    frozenset(["tiruchirappalli", "singapore"]),
    frozenset(["trichy", "singapore"]),
    frozenset(["tiruchirappalli", "dubai"]),
    frozenset(["trichy", "dubai"]),
    frozenset(["coimbatore", "singapore"]),
    frozenset(["mumbai", "london"]),
    frozenset(["delhi", "london"]),
    frozenset(["delhi", "paris"]),
    frozenset(["delhi", "tokyo"]),
    frozenset(["delhi", "new york"]),
    frozenset(["mumbai", "new york"])
}

INTERNATIONAL_HUBS: Set[str] = {"london", "paris", "tokyo", "dubai", "singapore", "new york"}

def is_overland_contiguous(orig: str, dest: str) -> bool:
    """Determine whether two locations are on contiguous land reachable by road or rail."""
    o = orig.strip().lower()
    d = dest.strip().lower()
    
    is_o_intl = o in INTERNATIONAL_HUBS
    is_d_intl = d in INTERNATIONAL_HUBS

    if is_o_intl != is_d_intl:
        return False
    if is_o_intl and is_d_intl:
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

def get_verified_bus_terminal(city_name: str) -> Optional[str]:
    """Look up verified central bus terminal for a city or district."""
    norm = city_name.strip().lower()
    for key, term in VERIFIED_BUS_TERMINALS.items():
        if key == norm or key in norm or norm in key:
            return term
    return None

# ==============================================================================
# 5. TAMIL NADU 6 CERTIFIED AIRPORTS REPOSITORY (Separated Metadata Schema)
# ==============================================================================
# Explicitly stores airport coordinates, district, airport code, operational status,
# and verified scheduled passenger service separately as mandated by routing rules.
TAMIL_NADU_COMMERCIAL_AIRPORTS: Dict[str, Dict[str, Any]] = {
    "MAA": {
        "airport_code": "MAA",
        "airport_name": "Chennai International Airport",
        "district": "Chennai",
        "coordinates": (12.9941, 80.1709),
        "lat": 12.9941,
        "lng": 80.1709,
        "operational_status": "Operational International Hub",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["IndiGo", "Air India", "Air India Express", "SpiceJet"],
        "booking_portal": "https://www.airportchennai.com"
    },
    "CJB": {
        "airport_code": "CJB",
        "airport_name": "Coimbatore International Airport",
        "district": "Coimbatore",
        "coordinates": (11.0299, 77.0434),
        "lat": 11.0299,
        "lng": 77.0434,
        "operational_status": "Operational International",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["IndiGo", "Air India", "Air India Express"],
        "booking_portal": "https://www.aai.aero/en/airports/coimbatore"
    },
    "IXM": {
        "airport_code": "IXM",
        "airport_name": "Madurai Airport",
        "district": "Madurai",
        "coordinates": (9.8345, 78.0934),
        "lat": 9.8345,
        "lng": 78.0934,
        "operational_status": "Operational Customs & Domestic",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["IndiGo", "Air India", "SpiceJet"],
        "booking_portal": "https://www.aai.aero/en/airports/madurai"
    },
    "TRZ": {
        "airport_code": "TRZ",
        "airport_name": "Tiruchirappalli International Airport",
        "district": "Tiruchirappalli",
        "coordinates": (10.7654, 78.7097),
        "lat": 10.7654,
        "lng": 78.7097,
        "operational_status": "Operational International",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["IndiGo", "Air India Express"],
        "booking_portal": "https://www.aai.aero/en/airports/tiruchirappalli"
    },
    "SXV": {
        "airport_code": "SXV",
        "airport_name": "Salem Airport",
        "district": "Salem",
        "coordinates": (11.7833, 78.0647),
        "lat": 11.7833,
        "lng": 78.0647,
        "operational_status": "Operational (UDAN RCS Scheduled)",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["Alliance Air", "IndiGo"],
        "booking_portal": "https://www.allianceair.in"
    },
    "TCR": {
        "airport_code": "TCR",
        "airport_name": "Thoothukudi Domestic Airport",
        "district": "Thoothukudi",
        "coordinates": (8.7236, 78.0264),
        "lat": 8.7236,
        "lng": 78.0264,
        "operational_status": "Operational Domestic Passenger",
        "has_scheduled_passenger_service": True,
        "primary_airlines": ["IndiGo"],
        "booking_portal": "https://www.aai.aero/en/airports/tuticorin"
    }
}

def get_tamil_nadu_commercial_airport(query: str) -> Optional[Dict[str, Any]]:
    """Return verified commercial airport data if query matches one of the 6 Tamil Nadu commercial airports."""
    q = query.strip().lower()
    for code, data in TAMIL_NADU_COMMERCIAL_AIRPORTS.items():
        if q == code.lower() or q == data["district"].lower() or data["district"].lower() in q or q in data["district"].lower():
            return data
    if "tuticorin" in q:
        return TAMIL_NADU_COMMERCIAL_AIRPORTS["TCR"]
    if "trichy" in q:
        return TAMIL_NADU_COMMERCIAL_AIRPORTS["TRZ"]
    return None

# ==============================================================================
# 6. VERIFIED TRAIN SERVICES (Indian Railways / Southern Railway Schedule Registry)
# ==============================================================================
# Real verified train numbers, timings, station pairings, and official IRCTC booking link.
VERIFIED_TRAIN_SERVICES: Dict[Tuple[str, str], List[Dict[str, Any]]] = {
    ("chennai", "tiruvannamalai"): [
        {
            "train_number": "16115 / 06033",
            "train_name": "Chennai Egmore - Tiruvannamalai Express / MEMU",
            "origin_station": "Chennai Egmore (MS) / Tambaram (TBM)",
            "dest_station": "Tiruvannamalai Railway Station (TNM)",
            "departure_time": "18:00",
            "arrival_time": "22:30",
            "duration_hours": 4.5,
            "fare_low": 115.0,
            "fare_high": 450.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "IRCTC Reservation Open (2S / CC / SL Berths)",
            "route_notes": "Southern Railway broad gauge route via Chengalpattu & Villupuram connecting directly to Tiruvannamalai (TNM)."
        }
    ],
    ("chennai", "coimbatore"): [
        {
            "train_number": "20643",
            "train_name": "Coimbatore Vande Bharat Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Coimbatore Junction (CBE)",
            "departure_time": "14:25",
            "arrival_time": "20:15",
            "duration_hours": 5.83,
            "fare_low": 1365.0,
            "fare_high": 2490.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Vande Bharat Express (AC Chair Car & Executive Car)",
            "route_notes": "Fastest rail corridor via Katpadi, Jolarpettai, Salem, and Erode to Coimbatore."
        },
        {
            "train_number": "12675",
            "train_name": "Kovai Superfast Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Coimbatore Junction (CBE)",
            "departure_time": "06:10",
            "arrival_time": "14:05",
            "duration_hours": 7.92,
            "fare_low": 195.0,
            "fare_high": 700.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Superfast (2S / AC Chair Car)",
            "route_notes": "Daytime premier intercity express connecting Chennai Central to Coimbatore Junction."
        },
        {
            "train_number": "12671",
            "train_name": "Nilgiri Superfast Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Coimbatore Junction (CBE)",
            "departure_time": "21:05",
            "arrival_time": "05:15",
            "duration_hours": 8.16,
            "fare_low": 335.0,
            "fare_high": 1270.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Overnight Sleeper & AC Berths",
            "route_notes": "Overnight superfast service connecting Chennai Central with Coimbatore."
        }
    ],
    ("chennai", "madurai"): [
        {
            "train_number": "20635",
            "train_name": "Madurai Tejas Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Madurai Junction (MDU)",
            "departure_time": "06:00",
            "arrival_time": "12:15",
            "duration_hours": 6.25,
            "fare_low": 1375.0,
            "fare_high": 2475.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Tejas Express (AC Chair Car & Executive Class)",
            "route_notes": "Fastest rail link between Chennai Egmore and Madurai via Tiruchirappalli."
        },
        {
            "train_number": "12635",
            "train_name": "Vaigai Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Madurai Junction (MDU)",
            "departure_time": "13:50",
            "arrival_time": "21:30",
            "duration_hours": 7.66,
            "fare_low": 180.0,
            "fare_high": 650.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Daytime Superfast (2S / AC Chair Car)",
            "route_notes": "Mainline express connecting Chennai Egmore to Madurai Junction."
        },
        {
            "train_number": "12637",
            "train_name": "Pandian Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Madurai Junction (MDU)",
            "departure_time": "21:40",
            "arrival_time": "05:35",
            "duration_hours": 7.91,
            "fare_low": 310.0,
            "fare_high": 1185.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Overnight Sleeper / 3A / 2A / 1A",
            "route_notes": "Premier overnight superfast connecting the state capital and Temple City."
        }
    ],
    ("chennai", "tiruchirappalli"): [
        {
            "train_number": "20605",
            "train_name": "Tiruchirappalli Vande Bharat Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tiruchirappalli Junction (TPJ)",
            "departure_time": "05:45",
            "arrival_time": "09:45",
            "duration_hours": 4.0,
            "fare_low": 1020.0,
            "fare_high": 1870.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Vande Bharat Superfast (AC Chair & Executive)",
            "route_notes": "Direct semi-high-speed transit connecting Chennai Egmore and Tiruchirappalli Junction in 4 hrs."
        },
        {
            "train_number": "12605",
            "train_name": "Pallavan Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tiruchirappalli Junction (TPJ)",
            "departure_time": "15:45",
            "arrival_time": "20:45",
            "duration_hours": 5.0,
            "fare_low": 145.0,
            "fare_high": 525.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Superfast (2S / AC Chair Car)",
            "route_notes": "Popular afternoon intercity service via Chengalpattu, Villupuram, and Ariyalur."
        },
        {
            "train_number": "12635",
            "train_name": "Vaigai Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tiruchirappalli Junction (TPJ)",
            "departure_time": "13:50",
            "arrival_time": "18:50",
            "duration_hours": 5.0,
            "fare_low": 145.0,
            "fare_high": 525.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Afternoon Superfast",
            "route_notes": "Mainline express connecting Chennai Egmore and Tiruchirappalli."
        }
    ],
    ("chennai", "trichy"): [
        {
            "train_number": "20605",
            "train_name": "Tiruchirappalli Vande Bharat Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tiruchirappalli Junction (TPJ)",
            "departure_time": "05:45",
            "arrival_time": "09:45",
            "duration_hours": 4.0,
            "fare_low": 1020.0,
            "fare_high": 1870.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Vande Bharat Superfast (AC Chair & Executive)",
            "route_notes": "Direct semi-high-speed transit connecting Chennai Egmore and Tiruchirappalli Junction in 4 hrs."
        },
        {
            "train_number": "12605",
            "train_name": "Pallavan Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tiruchirappalli Junction (TPJ)",
            "departure_time": "15:45",
            "arrival_time": "20:45",
            "duration_hours": 5.0,
            "fare_low": 145.0,
            "fare_high": 525.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Superfast (2S / AC Chair Car)",
            "route_notes": "Popular afternoon intercity service via Chengalpattu, Villupuram, and Ariyalur."
        }
    ],
    ("chennai", "salem"): [
        {
            "train_number": "20643",
            "train_name": "Chennai - Coimbatore Vande Bharat Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Salem Junction (SA)",
            "departure_time": "14:25",
            "arrival_time": "18:48",
            "duration_hours": 4.38,
            "fare_low": 1065.0,
            "fare_high": 1950.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "High-Speed AC Chair Car on IRCTC",
            "route_notes": "Semi-high speed service stopping directly at Salem Junction."
        },
        {
            "train_number": "12675",
            "train_name": "Kovai Superfast Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Salem Junction (SA)",
            "departure_time": "06:10",
            "arrival_time": "11:20",
            "duration_hours": 5.16,
            "fare_low": 155.0,
            "fare_high": 555.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Morning Superfast (2S / AC Chair)",
            "route_notes": "Daily morning superfast linking Chennai Central to Salem Junction."
        },
        {
            "train_number": "22649",
            "train_name": "Yercaud Superfast Express",
            "origin_station": "Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)",
            "dest_station": "Salem Junction (SA)",
            "departure_time": "23:00",
            "arrival_time": "05:10",
            "duration_hours": 6.16,
            "fare_low": 255.0,
            "fare_high": 975.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Overnight Sleeper & AC Berths",
            "route_notes": "Dedicated overnight superfast express connecting Chennai to Salem."
        }
    ],
    ("chennai", "thoothukudi"): [
        {
            "train_number": "12693",
            "train_name": "Pearl City Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tuticorin Terminus (TN)",
            "departure_time": "19:30",
            "arrival_time": "06:30",
            "duration_hours": 11.0,
            "fare_low": 395.0,
            "fare_high": 1495.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Superfast Sleeper & AC (Pearl City Corridor)",
            "route_notes": "Prestigious overnight connection between Chennai Egmore and Tuticorin port terminus."
        },
        {
            "train_number": "19568",
            "train_name": "Vivek Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tuticorin Terminus (TN)",
            "departure_time": "08:00",
            "arrival_time": "19:15",
            "duration_hours": 11.25,
            "fare_low": 390.0,
            "fare_high": 1420.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daytime Long-Distance Express",
            "route_notes": "Daytime service between Chennai Egmore and Thoothukudi."
        }
    ],
    ("chennai", "tuticorin"): [
        {
            "train_number": "12693",
            "train_name": "Pearl City Superfast Express",
            "origin_station": "Chennai Egmore (MS)",
            "dest_station": "Tuticorin Terminus (TN)",
            "departure_time": "19:30",
            "arrival_time": "06:30",
            "duration_hours": 11.0,
            "fare_low": 395.0,
            "fare_high": 1495.0,
            "booking_url": "https://www.irctc.co.in/nget/",
            "availability_status": "Daily Superfast Sleeper & AC (Pearl City Corridor)",
            "route_notes": "Prestigious overnight connection between Chennai Egmore and Tuticorin port terminus."
        }
    ]
}

def get_verified_train_services(orig: str, dest: str) -> Optional[List[Dict[str, Any]]]:
    """Retrieve verified train schedule records for route."""
    o = orig.strip().lower()
    d = dest.strip().lower()
    if (o, d) in VERIFIED_TRAIN_SERVICES:
        return VERIFIED_TRAIN_SERVICES[(o, d)]
    # Check partial match
    for (k_o, k_d), trains in VERIFIED_TRAIN_SERVICES.items():
        if (k_o in o or o in k_o) and (k_d in d or d in k_d):
            return trains
    return None

# ==============================================================================
# 7. VERIFIED PASSENGER AIRLINE FLIGHT SERVICES
# ==============================================================================
# Real verified commercial scheduled flights with airline operators, flight numbers,
# and official airline booking portals.
VERIFIED_FLIGHT_SERVICES: Dict[Tuple[str, str], Dict[str, Any]] = {
    ("chennai", "coimbatore"): {
        "flight_operator": "IndiGo / Air India Express",
        "flight_number": "6E 6825 / 6E 238",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Coimbatore International Airport (CJB)",
        "departure_time": "07:15 / 18:30 Scheduled Daily",
        "arrival_time": "08:20 / 19:35",
        "flight_duration_hours": 1.08,
        "total_duration_hours": 3.1,
        "fare_low": 3200.0,
        "fare_high": 5800.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Daily Flights Confirmed (Book on Airline Portal)"
    },
    ("chennai", "madurai"): {
        "flight_operator": "IndiGo / Air India",
        "flight_number": "6E 7183 / 6E 7259",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Madurai Airport (IXM)",
        "departure_time": "08:40 / 17:15 Scheduled Daily",
        "arrival_time": "09:55 / 18:30",
        "flight_duration_hours": 1.25,
        "total_duration_hours": 3.25,
        "fare_low": 3100.0,
        "fare_high": 5400.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Daily Flights Confirmed (Book on Airline Portal)"
    },
    ("chennai", "tiruchirappalli"): {
        "flight_operator": "IndiGo",
        "flight_number": "6E 7214 / 6E 7984",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Tiruchirappalli International Airport (TRZ)",
        "departure_time": "11:20 / 19:40 Scheduled Daily",
        "arrival_time": "12:20 / 20:40",
        "flight_duration_hours": 1.0,
        "total_duration_hours": 3.0,
        "fare_low": 2900.0,
        "fare_high": 4900.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Daily Commercial Service (Book on Airline Portal)"
    },
    ("chennai", "trichy"): {
        "flight_operator": "IndiGo",
        "flight_number": "6E 7214 / 6E 7984",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Tiruchirappalli International Airport (TRZ)",
        "departure_time": "11:20 / 19:40 Scheduled Daily",
        "arrival_time": "12:20 / 20:40",
        "flight_duration_hours": 1.0,
        "total_duration_hours": 3.0,
        "fare_low": 2900.0,
        "fare_high": 4900.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Daily Commercial Service (Book on Airline Portal)"
    },
    ("chennai", "salem"): {
        "flight_operator": "Alliance Air (UDAN Regional Scheduled)",
        "flight_number": "9I 507 / 9I 508",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Salem Airport (SXV)",
        "departure_time": "07:45 Scheduled Regional",
        "arrival_time": "08:40",
        "flight_duration_hours": 0.92,
        "total_duration_hours": 2.9,
        "fare_low": 2400.0,
        "fare_high": 4200.0,
        "booking_url": "https://www.allianceair.in",
        "availability_status": "Regional UDAN Scheduled Service (Verify active seasonal slot on Alliance Air)"
    },
    ("chennai", "thoothukudi"): {
        "flight_operator": "IndiGo Domestic",
        "flight_number": "6E 7958 / 6E 7961",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Thoothukudi Airport (TCR)",
        "departure_time": "06:15 / 13:40 Scheduled Daily",
        "arrival_time": "07:40 / 15:05",
        "flight_duration_hours": 1.42,
        "total_duration_hours": 3.4,
        "fare_low": 3600.0,
        "fare_high": 6400.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Domestic Passenger Service (Book on IndiGo Portal)"
    },
    ("chennai", "tuticorin"): {
        "flight_operator": "IndiGo Domestic",
        "flight_number": "6E 7958 / 6E 7961",
        "origin_airport": "Chennai International Airport (MAA)",
        "dest_airport": "Thoothukudi Airport (TCR)",
        "departure_time": "06:15 / 13:40 Scheduled Daily",
        "arrival_time": "07:40 / 15:05",
        "flight_duration_hours": 1.42,
        "total_duration_hours": 3.4,
        "fare_low": 3600.0,
        "fare_high": 6400.0,
        "booking_url": "https://www.goindigo.in",
        "availability_status": "Scheduled Domestic Passenger Service (Book on IndiGo Portal)"
    }
}

def get_verified_flight_services(orig: str, dest: str) -> Optional[Dict[str, Any]]:
    """Retrieve verified flight service records for route."""
    o = orig.strip().lower()
    d = dest.strip().lower()
    if (o, d) in VERIFIED_FLIGHT_SERVICES:
        return VERIFIED_FLIGHT_SERVICES[(o, d)]
    # Check partial match
    for (k_o, k_d), flight in VERIFIED_FLIGHT_SERVICES.items():
        if (k_o in o or o in k_o) and (k_d in d or d in k_d):
            return flight
    return None


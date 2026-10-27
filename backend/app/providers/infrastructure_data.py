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

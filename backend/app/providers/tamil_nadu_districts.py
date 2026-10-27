from typing import Dict, Any
from app.providers.chennai_places_data import CHENNAI_COMPREHENSIVE_PLACES

_FORMATTED_CHENNAI_PLACES = [
    {
        "name": p["name"],
        "category": p["category"],
        "lat": p["lat"],
        "lng": p["lng"],
        "is_outdoor": p["is_outdoor"],
        "duration": p["visit_duration_hours"],
        "cost": p["ticket_price_inr"],
        "desc": p["desc"],
        "area_zone": p.get("area_zone", "chennai_city"),
        "locality": p.get("locality", "Chennai"),
        "image_url": p.get("image_url"),
        "address": p.get("address")
    }
    for p in CHENNAI_COMPREHENSIVE_PLACES
]

TAMIL_NADU_DISTRICTS: Dict[str, Dict[str, Any]] = {
    # 1. Chennai (All 54 verified city, suburban & day-trip places)
    "chennai": {
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 13.0827,
        "lng": 80.2707,
        "places": _FORMATTED_CHENNAI_PLACES
    },

    # 2. Coimbatore
    "coimbatore": {
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.0168,
        "lng": 76.9558,
        "places": [
            {"name": "Isha Yoga Centre & Adiyogi Statue", "category": "Culture", "lat": 10.9726, "lng": 76.7404, "is_outdoor": True, "duration": 3.0, "cost": 0, "desc": "112-foot bust of Adiyogi Shiva and tranquil Dhyanalinga consecrated space in Velliangiri foothills."},
            {"name": "Marudhamalai Murugan Temple", "category": "Culture", "lat": 11.0458, "lng": 76.8524, "is_outdoor": False, "duration": 2.0, "cost": 50, "desc": "Hilltop temple dedicated to Lord Murugan surrounded by medicinal herbs."},
            {"name": "Gass Forest Museum", "category": "Nature", "lat": 11.0185, "lng": 76.9458, "is_outdoor": False, "duration": 1.5, "cost": 50, "desc": "Historic natural history museum established in 1902 showcasing preserved wildlife and forestry."},
            {"name": "Siruvani Waterfalls & Dam", "category": "Nature", "lat": 10.9634, "lng": 76.6853, "is_outdoor": True, "duration": 3.0, "cost": 100, "desc": "Famed for mineral-rich sweet water nestled in the Western Ghats."}
        ]
    },
    # 3. Madurai
    "madurai": {
        "city": "Madurai",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 9.9252,
        "lng": 78.1198,
        "places": [
            {"name": "Meenakshi Amman Temple", "category": "Culture", "lat": 9.9195, "lng": 78.1193, "is_outdoor": False, "duration": 2.5, "cost": 50, "desc": "Magnificent historic Dravidian temple complex with 14 gopurams and Hall of Thousand Pillars."},
            {"name": "Thirumalai Nayakkar Palace", "category": "Culture", "lat": 9.9152, "lng": 78.1235, "is_outdoor": False, "duration": 2.0, "cost": 100, "desc": "17th-century Indo-Saracenic palace famous for giant stone pillars and evening light-and-sound show."},
            {"name": "Gandhi Memorial Museum (Tamukkam Palace)", "category": "Culture", "lat": 9.9328, "lng": 78.1396, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Historic palace museum preserving Mahatma Gandhi's blood-stained garment and freedom artifacts."},
            {"name": "Vandiyur Mariamman Teppakulam Tank", "category": "Sightseeing", "lat": 9.9103, "lng": 78.1517, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Enormous temple pond built in 1645 with a central granite pavilion mandapam."}
        ]
    },
    # 4. Tiruchirappalli (Trichy)
    "tiruchirappalli": {
        "city": "Tiruchirappalli",
        "district": "Tiruchirappalli",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.7905,
        "lng": 78.7047,
        "places": [
            {"name": "Sri Ranganathaswamy Temple (Srirangam)", "category": "Culture", "lat": 10.8624, "lng": 78.6901, "is_outdoor": False, "duration": 3.0, "cost": 100, "desc": "Largest functioning Hindu temple complex in the world spanning 156 acres across 7 concentric enclosures."},
            {"name": "Rockfort Ucchi Pillayar Temple", "category": "Culture", "lat": 10.8286, "lng": 78.6967, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Ancient 3.8-billion-year-old rock fortress with 437 stone steps leading to panoramic hilltop shrine."},
            {"name": "Jambukeswarar Temple (Thiruvanaikaval)", "category": "Culture", "lat": 10.8527, "lng": 78.7058, "is_outdoor": False, "duration": 1.5, "cost": 50, "desc": "Pancha Bhoota Stalam representing Water element with perennial spring underneath the lingam."},
            {"name": "Kallanai Grand Anicut Dam", "category": "Sightseeing", "lat": 10.8354, "lng": 78.8228, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "World's oldest functional water-diversion dam built by Chola King Karikalan across Kaveri River."}
        ]
    },
    # 5. Thanjavur (Tanjore)
    "thanjavur": {
        "city": "Thanjavur",
        "district": "Thanjavur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.7870,
        "lng": 79.1378,
        "places": [
            {"name": "Brihadisvara Temple (Big Temple)", "category": "Culture", "lat": 10.7828, "lng": 79.1318, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "UNESCO Great Living Chola Temple built by Raja Raja Chola I with an 80-tonne monolithic cupola."},
            {"name": "Thanjavur Maratha Palace & Art Gallery", "category": "Culture", "lat": 10.7915, "lng": 79.1362, "is_outdoor": False, "duration": 2.0, "cost": 150, "desc": "Royal residence housing ancient Chola bronzes, Bell Tower, and Arsenal Tower."},
            {"name": "Saraswathi Mahal Library", "category": "Culture", "lat": 10.7920, "lng": 79.1360, "is_outdoor": False, "duration": 1.5, "cost": 50, "desc": "One of Asia's oldest medieval libraries preserving rare palm-leaf manuscripts and treaties."}
        ]
    },
    # 6. Kanyakumari
    "kanyakumari": {
        "city": "Kanyakumari",
        "district": "Kanyakumari",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.0883,
        "lng": 77.5385,
        "places": [
            {"name": "Vivekananda Rock Memorial & Ferry", "category": "Culture", "lat": 8.0781, "lng": 77.5552, "is_outdoor": True, "duration": 2.5, "cost": 150, "desc": "Iconic memorial on two offshore rock islands where Swami Vivekananda meditated in 1892."},
            {"name": "Thiruvalluvar Statue (133-foot Monolith)", "category": "Sightseeing", "lat": 8.0778, "lng": 77.5558, "is_outdoor": True, "duration": 1.5, "cost": 50, "desc": "Towering stone sculpture commemorating the ancient Tamil poet and philosopher."},
            {"name": "Triveni Sangam & Sunset Beach Point", "category": "Nature", "lat": 8.0792, "lng": 77.5492, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Southernmost tip of mainland India where the Arabian Sea, Indian Ocean, and Bay of Bengal converge."},
            {"name": "Padmanabhapuram Palace", "category": "Culture", "lat": 8.2508, "lng": 77.3275, "is_outdoor": False, "duration": 2.5, "cost": 100, "desc": "Magnificent wooden palace of Travancore kings featuring intricate rosewood and teak craftsmanship."}
        ]
    },
    # 7. Nilgiris (Ooty)
    "nilgiris": {
        "city": "Ooty (Nilgiris)",
        "district": "Nilgiris",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.4102,
        "lng": 76.6950,
        "places": [
            {"name": "Government Botanical Gardens Ooty", "category": "Nature", "lat": 11.4168, "lng": 76.7118, "is_outdoor": True, "duration": 2.5, "cost": 100, "desc": "Terraced 55-acre garden established in 1848 with exotic fern house, fossil tree trunk, and Italian gardens."},
            {"name": "Doddabetta Peak Viewpoint", "category": "Sightseeing", "lat": 11.4011, "lng": 76.7358, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Highest mountain in the Nilgiri Hills (2,637 m) offering panoramic telescope room views."},
            {"name": "Nilgiri Mountain Railway Toy Train", "category": "Adventure", "lat": 11.4075, "lng": 76.7032, "is_outdoor": True, "duration": 3.0, "cost": 300, "desc": "UNESCO heritage rack-and-pinion steam railway chugging through mist-covered tea slopes and tunnels."},
            {"name": "Pykara Lake & Waterfalls", "category": "Nature", "lat": 11.4880, "lng": 76.5960, "is_outdoor": True, "duration": 2.5, "cost": 150, "desc": "Sacred Toda river lake offering speed-boating and cascading waterfalls surrounded by pine forests."}
        ]
    },
    # 8. Dindigul (Kodaikanal)
    "dindigul": {
        "city": "Kodaikanal (Dindigul)",
        "district": "Dindigul",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.2381,
        "lng": 77.4892,
        "places": [
            {"name": "Kodaikanal Lake & Boating Club", "category": "Nature", "lat": 10.2345, "lng": 77.4900, "is_outdoor": True, "duration": 2.5, "cost": 200, "desc": "Star-shaped artificial lake built in 1863 flanked by lush gardens and pedal-boat rides."},
            {"name": "Coaker's Walk & Green Valley View", "category": "Sightseeing", "lat": 10.2312, "lng": 77.4962, "is_outdoor": True, "duration": 1.5, "cost": 50, "desc": "Pedestrian paved cliff walk presenting mesmerizing cloud-covered valleys of Vaigai river."},
            {"name": "Pillar Rocks & Pine Forest Walk", "category": "Nature", "lat": 10.2185, "lng": 77.4660, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Three gigantic vertical granite boulders standing 122 meters high amidst mist."},
            {"name": "Dindigul Rock Fort (Historical Citadel)", "category": "Culture", "lat": 10.3630, "lng": 77.9690, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "17th-century fortress built by Nayak rulers on a monolithic steep rock outcrop."}
        ]
    },
    # 9. Ramanathapuram (Rameswaram)
    "ramanathapuram": {
        "city": "Rameswaram (Ramanathapuram)",
        "district": "Ramanathapuram",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 9.2876,
        "lng": 79.3129,
        "places": [
            {"name": "Ramanathaswamy Temple & 22 Theerthams", "category": "Culture", "lat": 9.2881, "lng": 79.3174, "is_outdoor": False, "duration": 3.0, "cost": 100, "desc": "Char Dham jyotirlinga shrine boasting the longest temple corridor in India with 1,212 carved pillars."},
            {"name": "Dhanushkodi Ghost Town & Sangam Point", "category": "Nature", "lat": 9.1764, "lng": 79.4184, "is_outdoor": True, "duration": 3.0, "cost": 250, "desc": "Submerged city ruins on narrow sand spit where Bay of Bengal meets the Indian Ocean facing Sri Lanka."},
            {"name": "Pamban Sea Bridge Viewpoint", "category": "Sightseeing", "lat": 9.2789, "lng": 79.1963, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Engineering marvel railway sea bridge with lifting Scherzer span over the Palk Strait."},
            {"name": "Dr. APJ Abdul Kalam National Memorial", "category": "Culture", "lat": 9.2880, "lng": 79.2840, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Memorial showcasing the life, rocket models, and national awards of India's Missile Man."}
        ]
    },
    # 10. Tirunelveli
    "tirunelveli": {
        "city": "Tirunelveli",
        "district": "Tirunelveli",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.7139,
        "lng": 77.7567,
        "places": [
            {"name": "Nellaiappar Temple & Musical Pillars", "category": "Culture", "lat": 8.7289, "lng": 77.6897, "is_outdoor": False, "duration": 2.5, "cost": 50, "desc": "Twin temple complex of Shiva and Kanthimathi Ambal famous for acoustic musical stone pillars."},
            {"name": "Manimuthar Waterfalls & Dam Garden", "category": "Nature", "lat": 8.5830, "lng": 77.4170, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "Cascading mountain waterfall with natural swimming pond in the Western Ghats."},
            {"name": "Iruttu Kadai Halwa & Market Exploration", "category": "Food", "lat": 8.7285, "lng": 77.6905, "is_outdoor": True, "duration": 1.5, "cost": 150, "desc": "Iconic shop serving hot wheat halwa prepared using Thamirabarani river water."},
            {"name": "District Science Centre & Planetarium", "category": "Culture", "lat": 8.7100, "lng": 77.7400, "is_outdoor": False, "duration": 2.0, "cost": 50, "desc": "Interactive science galleries and astronomical show on the banks of Thamirabarani River."}
        ]
    },
    # 11. Tenkasi
    "tenkasi": {
        "city": "Tenkasi",
        "district": "Tenkasi",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.9594,
        "lng": 77.3142,
        "places": [
            {"name": "Courtallam Main Waterfalls", "category": "Nature", "lat": 8.9317, "lng": 77.2725, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "The 'Spa of South India' featuring therapeutic herbal waters tumbling over Chittar River rocks."},
            {"name": "Kasi Viswanathar Temple Tenkasi", "category": "Culture", "lat": 8.9602, "lng": 77.3150, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Historic 180-foot gopuram built by King Parakkirama Pandian in the 15th century."},
            {"name": "Five Falls (Aintharuvi)", "category": "Nature", "lat": 8.9350, "lng": 77.2450, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Picturesque cascade where the river splits into five distinct natural streams."},
            {"name": "Gundar Dam & Eco Park", "category": "Nature", "lat": 9.0200, "lng": 77.2800, "is_outdoor": True, "duration": 2.0, "cost": 30, "desc": "Serene reservoir surrounded by thick rainforest canopies and trekking paths."}
        ]
    },
    # 12. Salem
    "salem": {
        "city": "Salem",
        "district": "Salem",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.6643,
        "lng": 78.1460,
        "places": [
            {"name": "Yercaud Hill Station & Emerald Lake", "category": "Nature", "lat": 11.7753, "lng": 78.2093, "is_outdoor": True, "duration": 3.0, "cost": 100, "desc": "Jewel of the Shevaroy Hills offering boating on Emerald Lake, Pagoda Point, and spice gardens."},
            {"name": "Mettur Dam & Stanley Reservoir Park", "category": "Sightseeing", "lat": 11.7947, "lng": 77.8016, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "One of the largest masonry dams in India spanning the Kaveri with expansive landscaped gardens."},
            {"name": "1008 Shiva Lingam Temple", "category": "Culture", "lat": 11.6140, "lng": 78.1880, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Spiritual shrine atop Ariyanoor hill featuring 1008 individual Shiva lingams."}
        ]
    },
    # 13. Erode
    "erode": {
        "city": "Erode",
        "district": "Erode",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.3410,
        "lng": 77.7172,
        "places": [
            {"name": "Bhavani Sangameswarar Temple (Kooduthurai)", "category": "Culture", "lat": 11.4428, "lng": 77.6833, "is_outdoor": False, "duration": 2.0, "cost": 0, "desc": "Sacred confluence of Kaveri, Bhavani, and the invisible Amutha rivers."},
            {"name": "Vellode Birds Sanctuary", "category": "Nature", "lat": 11.2580, "lng": 77.6530, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "77-hectare sanctuary hosting migratory pelicans, teals, and cormorants."},
            {"name": "Thindal Murugan Temple", "category": "Culture", "lat": 11.3190, "lng": 77.6740, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Elevated temple complex on Thindal hill dedicated to Lord Velayudaswami."}
        ]
    },
    # 14. Tiruppur
    "tiruppur": {
        "city": "Tiruppur",
        "district": "Tiruppur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.1085,
        "lng": 77.3411,
        "places": [
            {"name": "Thirumoorthy Dam & Amanalingeswarar Temple", "category": "Nature", "lat": 10.4570, "lng": 77.1630, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "Scenic reservoir with Panjalinga waterfalls in the Anamalai hills."},
            {"name": "Avinashilingeswarar Temple (Avinashi)", "category": "Culture", "lat": 11.1925, "lng": 77.2683, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Ancient Karunaiyathaal temple praised by Sundarar with magnificent carved pillars."},
            {"name": "Tiruppur Kumaran Memorial", "category": "Culture", "lat": 11.1070, "lng": 77.3450, "is_outdoor": False, "duration": 1.0, "cost": 0, "desc": "Tribute to the young freedom martyr who held the national flag high during colonial protests."}
        ]
    },
    # 15. Kanchipuram
    "kanchipuram": {
        "city": "Kanchipuram",
        "district": "Kanchipuram",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.8342,
        "lng": 79.7036,
        "places": [
            {"name": "Ekambareswarar Temple (Earth Element)", "category": "Culture", "lat": 12.8465, "lng": 79.6998, "is_outdoor": False, "duration": 2.0, "cost": 50, "desc": "Pancha Bhoota Stalam representing Earth with a 3,500-year-old mango tree yielding 4 flavors."},
            {"name": "Kailasanathar Temple", "category": "Culture", "lat": 12.8423, "lng": 79.6897, "is_outdoor": True, "duration": 2.0, "cost": 25, "desc": "Oldest sandstone temple in Kanchipuram built by Pallava King Rajasimha in 700 AD."},
            {"name": "Kanchi Silk Weavers Cooperative Society", "category": "Food", "lat": 12.8330, "lng": 79.7050, "is_outdoor": False, "duration": 2.0, "cost": 0, "desc": "Witness live handloom weaving of mulberry silk and pure gold zari borders."}
        ]
    },
    # 16. Chengalpattu (Mahabalipuram)
    "chengalpattu": {
        "city": "Mahabalipuram (Chengalpattu)",
        "district": "Chengalpattu",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.6208,
        "lng": 80.1944,
        "places": [
            {"name": "Shore Temple & Bay of Bengal Promenade", "category": "Culture", "lat": 12.6163, "lng": 80.1983, "is_outdoor": True, "duration": 2.0, "cost": 250, "desc": "8th-century granite sea-facing monument, recognized as a UNESCO World Heritage Site."},
            {"name": "Arjuna's Penance & Krishna's Butterball", "category": "Culture", "lat": 12.6179, "lng": 80.1932, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "World's largest open-air rock relief carving and a balancing 250-tonne boulder on a smooth slope."},
            {"name": "Pancha Rathas (Five Chariots)", "category": "Culture", "lat": 12.6094, "lng": 80.1915, "is_outdoor": True, "duration": 1.5, "cost": 250, "desc": "Five monolithic rock-cut shrines named after Pandavas carved out of single pink diorite boulders."},
            {"name": "Madras Crocodile Bank Trust", "category": "Nature", "lat": 12.7538, "lng": 80.2415, "is_outdoor": True, "duration": 2.0, "cost": 150, "desc": "Reptile zoo and herpetology research station housing muggers, gharials, and venomous snakes."}
        ]
    },
    # 17. Tiruvannamalai
    "tiruvannamalai": {
        "city": "Tiruvannamalai",
        "district": "Tiruvannamalai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.2253,
        "lng": 79.0747,
        "places": [
            {"name": "Arunachaleswarar Temple (Fire Element)", "category": "Culture", "lat": 12.2307, "lng": 79.0677, "is_outdoor": False, "duration": 2.5, "cost": 50, "desc": "Pancha Bhoota Stalam of Agni (Fire) located at the foot of Arunachala hill with 66-meter Rajagopuram."},
            {"name": "Girivalam Path of Sacred Arunachala Hill", "category": "Nature", "lat": 12.2350, "lng": 79.0550, "is_outdoor": True, "duration": 3.5, "cost": 0, "desc": "14-km sacred circumambulation circuit around the volcanic holy mountain."},
            {"name": "Sri Ramana Maharshi Ashram", "category": "Culture", "lat": 12.2205, "lng": 79.0577, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Tranquil meditation hall and samadhi shrine surrounded by peacocks and green foliage."},
            {"name": "Sathanur Dam & Crocodile Sanctuary", "category": "Sightseeing", "lat": 12.1850, "lng": 78.8530, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Major dam on Thenpennai River with formal gardens, hanging bridge, and crocodile farm."}
        ]
    },
    # 18. Vellore
    "vellore": {
        "city": "Vellore",
        "district": "Vellore",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.9165,
        "lng": 79.1325,
        "places": [
            {"name": "Vellore Fort & Jalakanteswarar Temple", "category": "Culture", "lat": 12.9228, "lng": 79.1325, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "16th-century granite fort surrounded by a deep moat, site of the 1806 Vellore Mutiny."},
            {"name": "Sripuram Golden Temple (Malaikodi)", "category": "Culture", "lat": 12.8710, "lng": 79.0883, "is_outdoor": False, "duration": 2.5, "cost": 100, "desc": "Spiritual park featuring Sri Lakshmi Narayani temple covered in 1,500 kg of pure gold foil."},
            {"name": "Amirthi Zoological Park", "category": "Nature", "lat": 12.7230, "lng": 79.0820, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Wildlife sanctuary and seasonal waterfall tucked away in the Javadi Hills."}
        ]
    },
    # 19. Ranipet
    "ranipet": {
        "city": "Ranipet",
        "district": "Ranipet",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.9272,
        "lng": 79.3330,
        "places": [
            {"name": "Delhi Gate & Arcot Fort Ruins", "category": "Culture", "lat": 12.9050, "lng": 79.3350, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Historic defensive red-stone portal commemorating the 1751 Siege of Arcot by Robert Clive."},
            {"name": "Mahendravadi Rock-cut Cave Temple", "category": "Culture", "lat": 13.0450, "lng": 79.5800, "is_outdoor": True, "duration": 1.5, "cost": 25, "desc": "7th-century Pallava cave sanctuary carved into monolithic stone dedicated to Murari."},
            {"name": "Palar River Promenade & Park", "category": "Nature", "lat": 12.9300, "lng": 79.3300, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Riverfront green corridor in the historic leather and artisan trade town."}
        ]
    },
    # 20. Tirupathur
    "tirupathur": {
        "city": "Yelagiri (Tirupathur)",
        "district": "Tirupathur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.5833,
        "lng": 78.6333,
        "places": [
            {"name": "Yelagiri Hills & Punganoor Lake", "category": "Nature", "lat": 12.5800, "lng": 78.6400, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "Cluster of 14 tribal hamlets 1,110m high with boating, orchidarium, and rose gardens."},
            {"name": "Jalagamparai Waterfalls", "category": "Adventure", "lat": 12.5500, "lng": 78.6800, "is_outdoor": True, "duration": 3.0, "cost": 0, "desc": "Attaru river cascade falling through thick foliage, reached via scenic forest trek."},
            {"name": "Vainu Bappu Observatory (Kavalur)", "category": "Culture", "lat": 12.5760, "lng": 78.8270, "is_outdoor": False, "duration": 2.0, "cost": 50, "desc": "Asian continent's premier optical astronomical telescope facility in the Javadi Hills."}
        ]
    },
    # 21. Dharmapuri
    "dharmapuri": {
        "city": "Dharmapuri (Hogenakkal)",
        "district": "Dharmapuri",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.1211,
        "lng": 78.1582,
        "places": [
            {"name": "Hogenakkal Falls ('Niagara of India')", "category": "Adventure", "lat": 12.1186, "lng": 77.7770, "is_outdoor": True, "duration": 3.5, "cost": 350, "desc": "Spectacular river waterfalls on the Kaveri offering round bamboo coracle boat rides and herbal baths."},
            {"name": "Theerthamalai Sacred Shiva Temple", "category": "Culture", "lat": 12.0830, "lng": 78.5830, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Hill temple with five holy waterfalls flowing non-stop from the mountainside."},
            {"name": "Adiyamankottai Fort & Chenraya Perumal", "category": "Culture", "lat": 12.0850, "lng": 78.1400, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Historic fortress built by Sangam era ruler King Adiyaman."}
        ]
    },
    # 22. Krishnagiri
    "krishnagiri": {
        "city": "Krishnagiri",
        "district": "Krishnagiri",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 12.5186,
        "lng": 78.2137,
        "places": [
            {"name": "Krishnagiri Dam & Reservoir Gardens", "category": "Nature", "lat": 12.4700, "lng": 78.1800, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Thenpennai river reservoir flanked by rolling granite hills and flower parks."},
            {"name": "Sayed Basha Hill Fort", "category": "Adventure", "lat": 12.5200, "lng": 78.2100, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Steep rock fortress of Hyder Ali offering sweeping views over Krishnagiri district."},
            {"name": "Rayakottai Medieval Military Fort", "category": "Culture", "lat": 12.5180, "lng": 78.0380, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Strategic ramparts and watchtowers dating back to the Anglo-Mysore wars."}
        ]
    },
    # 23. Namakkal
    "namakkal": {
        "city": "Namakkal (Kolli Hills)",
        "district": "Namakkal",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.2189,
        "lng": 78.1674,
        "places": [
            {"name": "Kolli Hills (70 Hairpin Bends)", "category": "Adventure", "lat": 11.2500, "lng": 78.3400, "is_outdoor": True, "duration": 4.0, "cost": 0, "desc": "Untamed mountain range with 70 continuous hairpin bends, pepper estates, and medicinal herbs."},
            {"name": "Agaya Gangai Waterfalls", "category": "Nature", "lat": 11.2800, "lng": 78.3500, "is_outdoor": True, "duration": 3.0, "cost": 50, "desc": "300-foot spectacular waterfall in Kolli Hills accessed via steep 1,000-step descent."},
            {"name": "Namakkal Anjaneyar & Rock Fort", "category": "Culture", "lat": 11.2205, "lng": 78.1650, "is_outdoor": False, "duration": 2.0, "cost": 0, "desc": "Monolithic 18-foot Hanuman statue standing uncovered in open air facing Narasimha fort."}
        ]
    },
    # 24. Karur
    "karur": {
        "city": "Karur",
        "district": "Karur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.9601,
        "lng": 78.0766,
        "places": [
            {"name": "Sri Pasupatheeswarar Temple", "category": "Culture", "lat": 10.9610, "lng": 78.0770, "is_outdoor": False, "duration": 2.0, "cost": 0, "desc": "1st-century Chola temple dedicated to Lord Shiva with self-manifested Swayambhu lingam."},
            {"name": "Mayanur Barrage & Kaveri Eco Park", "category": "Nature", "lat": 10.9400, "lng": 78.2300, "is_outdoor": True, "duration": 2.0, "cost": 30, "desc": "Riverfront barrage with boating, children's park, and landscaped lawns."},
            {"name": "Pugazhimalai Balasubramaniaswamy Temple", "category": "Culture", "lat": 11.0500, "lng": 78.0100, "is_outdoor": True, "duration": 1.5, "cost": 0, "desc": "Hill temple overlooking the lush coconut groves and Amaravathi river basin."}
        ]
    },
    # 25. Pudukkottai
    "pudukkottai": {
        "city": "Pudukkottai",
        "district": "Pudukkottai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.3797,
        "lng": 78.8208,
        "places": [
            {"name": "Sittannavasal Cave Paintings & Jaina Beds", "category": "Culture", "lat": 10.4578, "lng": 78.7289, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "2nd-century BC rock-cut Jaina monument famous for natural vegetable dye fresco murals."},
            {"name": "Thirumayam Fort & Rock-cut Shrines", "category": "Culture", "lat": 10.2450, "lng": 78.7550, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "40-acre 17th-century bastion built by Sethupathi of Ramnad with rock-cut temples."},
            {"name": "Pudukkottai Government Archaeological Museum", "category": "Culture", "lat": 10.3800, "lng": 78.8200, "is_outdoor": False, "duration": 1.5, "cost": 25, "desc": "Second largest state museum with rare sculptures, zoological specimens, and Chola bronzes."}
        ]
    },
    # 26. Sivagangai
    "sivagangai": {
        "city": "Chettinad (Sivagangai)",
        "district": "Sivagangai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 9.8433,
        "lng": 78.4809,
        "places": [
            {"name": "Chettinad Heritage Mansions (Kanadukathan)", "category": "Culture", "lat": 10.1500, "lng": 78.7800, "is_outdoor": False, "duration": 3.0, "cost": 150, "desc": "Opulent palatial merchant mansions built with Burmese teak, Italian marble, and Athangudi tiles."},
            {"name": "Athangudi Handmade Tile Workshops", "category": "Food", "lat": 10.1600, "lng": 78.7500, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Witness generation-old artisans hand-casting vibrant glass-glazed geometric tiles."},
            {"name": "Vettangudi Bird Sanctuary", "category": "Nature", "lat": 9.9800, "lng": 78.4900, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Breeding habitat for Asian openbill storks, painted storks, and grey herons."},
            {"name": "Chettinad Culinary Tasting (Authentic Kitchens)", "category": "Food", "lat": 10.1520, "lng": 78.7820, "is_outdoor": True, "duration": 1.5, "cost": 500, "desc": "Authentic multi-course banana leaf feast with black rice kavuni arisi and aromatic masalas."}
        ]
    },
    # 27. Virudhunagar
    "virudhunagar": {
        "city": "Virudhunagar (Srivilliputhur)",
        "district": "Virudhunagar",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 9.5680,
        "lng": 77.9624,
        "places": [
            {"name": "Srivilliputhur Andal Temple (Tamil Nadu State Emblem)", "category": "Culture", "lat": 9.5100, "lng": 77.6300, "is_outdoor": False, "duration": 2.5, "cost": 0, "desc": "192-foot monumental gopuram depicted on the official emblem of the Government of Tamil Nadu."},
            {"name": "Kamarajar Memorial House", "category": "Culture", "lat": 9.5850, "lng": 77.9550, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Humble ancestral residence of kingmaker and former Chief Minister K. Kamaraj."},
            {"name": "Grizzled Squirrel Wildlife Sanctuary", "category": "Nature", "lat": 9.5200, "lng": 77.4500, "is_outdoor": True, "duration": 3.0, "cost": 100, "desc": "Western Ghats sanctuary protecting the endangered giant flying squirrel and lion-tailed macaques."}
        ]
    },
    # 28. Theni
    "theni": {
        "city": "Theni (Megamalai & Suruli)",
        "district": "Theni",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.0104,
        "lng": 77.4768,
        "places": [
            {"name": "Suruli Falls & Rock-cut Caves", "category": "Nature", "lat": 9.6640, "lng": 77.2940, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "Two-stage cascading falls fed by Meghamalai range with 18 sacred rock-cut cave hermitages."},
            {"name": "Meghamalai 'Highwavys' Tea Plantations", "category": "Nature", "lat": 9.7000, "lng": 77.3800, "is_outdoor": True, "duration": 4.0, "cost": 100, "desc": "Mist-clad cardamom and tea estate mountains overlooking the Cumbum valley."},
            {"name": "Kumbakkarai Waterfalls", "category": "Nature", "lat": 10.1700, "lng": 77.5300, "is_outdoor": True, "duration": 2.0, "cost": 30, "desc": "Pambar river waterfalls cascading through unique rock formations at the foot of Kodaikanal hills."}
        ]
    },
    # 29. Thoothukudi (Tuticorin)
    "thoothukudi": {
        "city": "Thoothukudi (Tuticorin)",
        "district": "Thoothukudi",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 8.7642,
        "lng": 78.1348,
        "places": [
            {"name": "Our Lady of Snows Basilica", "category": "Culture", "lat": 8.8078, "lng": 78.1578, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "16th-century Portuguese shrine on the Coromandel coast celebrating the miracle of Mother Mary."},
            {"name": "Hare Island & Pearl City Beach Walk", "category": "Nature", "lat": 8.7800, "lng": 78.1900, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Shoreline peninsula famous for natural sea breeze, lighthouse, and pearl fishery legacy."},
            {"name": "Kulasekharapatnam Mutharamman Temple", "category": "Culture", "lat": 8.3800, "lng": 78.0500, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Coastal Shakti shrine renowned worldwide for its 10-day Dasara masquerade carnival."}
        ]
    },
    # 30. Cuddalore
    "cuddalore": {
        "city": "Cuddalore (Pichavaram & Chidambaram)",
        "district": "Cuddalore",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.7480,
        "lng": 79.7714,
        "places": [
            {"name": "Pichavaram Mangrove Forest Boat Safari", "category": "Nature", "lat": 11.4300, "lng": 79.7800, "is_outdoor": True, "duration": 3.0, "cost": 300, "desc": "World's second largest mangrove ecosystem with 4,400 interconnected water canals."},
            {"name": "Chidambaram Nataraja Temple (Sky Element)", "category": "Culture", "lat": 11.3992, "lng": 79.6934, "is_outdoor": False, "duration": 2.5, "cost": 50, "desc": "Pancha Bhoota Stalam representing Akasha (Space/Sky) with the golden-roofed cosmic dance hall."},
            {"name": "Silver Beach & Devanampattinam Point", "category": "Nature", "lat": 11.7300, "lng": 79.7800, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Second longest beach in Tamil Nadu offering water sports, quiet dunes, and sunrise views."}
        ]
    },
    # 31. Villupuram
    "villupuram": {
        "city": "Villupuram (Gingee)",
        "district": "Villupuram",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.9401,
        "lng": 79.4861,
        "places": [
            {"name": "Gingee Fort ('Troy of the East')", "category": "Culture", "lat": 12.2514, "lng": 79.4181, "is_outdoor": True, "duration": 3.5, "cost": 50, "desc": "Impregnable citadel spanning three hillocks with 8-story Kalyana Mahal and 60-foot deep moats."},
            {"name": "Mailam Murugan Hill Temple", "category": "Culture", "lat": 12.1280, "lng": 79.6200, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Centuries-old pilgrimage hill temple dedicated to Lord Subramanya."},
            {"name": "Melmalayanur Angalamman Temple", "category": "Culture", "lat": 12.3500, "lng": 79.3800, "is_outdoor": True, "duration": 2.0, "cost": 0, "desc": "Famous ancient mother goddess shrine on the banks of Seshathirtham."}
        ]
    },
    # 32. Kallakurichi
    "kallakurichi": {
        "city": "Kallakurichi (Kalvarayan Hills)",
        "district": "Kallakurichi",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.7383,
        "lng": 78.9639,
        "places": [
            {"name": "Kalvarayan Hills & Gomukhi Dam", "category": "Nature", "lat": 11.7800, "lng": 78.8500, "is_outdoor": True, "duration": 3.0, "cost": 30, "desc": "Peaceful Eastern Ghats hill range offering scenic viewpoints and reservoir boat rides."},
            {"name": "Periyar Waterfalls & Megam Falls", "category": "Nature", "lat": 11.8200, "lng": 78.8000, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Cascading hill streams surrounded by evergreen forests and indigenous tribal hamlets."}
        ]
    },
    # 33. Nagapattinam
    "nagapattinam": {
        "city": "Nagapattinam (Velankanni)",
        "district": "Nagapattinam",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.7672,
        "lng": 79.8449,
        "places": [
            {"name": "Basilica of Our Lady of Good Health (Velankanni)", "category": "Culture", "lat": 10.6800, "lng": 79.8500, "is_outdoor": False, "duration": 2.5, "cost": 0, "desc": "Famous 'Lourdes of the East' coastal basilica drawing millions of pilgrims worldwide."},
            {"name": "Nagore Dargah Shrine (Hazrat Syed Shahul)", "category": "Culture", "lat": 10.8200, "lng": 79.8450, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "500-year-old Islamic Sufi shrine with 5 towering minarets celebrating interfaith harmony."},
            {"name": "Point Calimere Wildlife & Bird Sanctuary", "category": "Nature", "lat": 10.3000, "lng": 79.8600, "is_outdoor": True, "duration": 3.0, "cost": 100, "desc": "Coastal wetland and salt swamp hosting greater flamingos, blackbucks, and dolphins."}
        ]
    },
    # 34. Mayiladuthurai
    "mayiladuthurai": {
        "city": "Mayiladuthurai (Tranquebar)",
        "district": "Mayiladuthurai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.1075,
        "lng": 79.6522,
        "places": [
            {"name": "Fort Dansborg (Danish Fort Tranquebar)", "category": "Culture", "lat": 11.0333, "lng": 79.8500, "is_outdoor": True, "duration": 2.5, "cost": 50, "desc": "1620 Scandinavian coastal fortress and maritime museum with high defensive cannons."},
            {"name": "Mayuranathaswamy Temple", "category": "Culture", "lat": 11.1000, "lng": 79.6500, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Vast Shiva temple where Goddess Parvati worshipped in the form of a peacock (Mayura)."},
            {"name": "Poompuhar Ancient Port & Maritime Museum", "category": "Culture", "lat": 11.1400, "lng": 79.8500, "is_outdoor": True, "duration": 2.0, "cost": 50, "desc": "Legendary submerged capital of early Cholas described in the Tamil epic Silappadikaram."}
        ]
    },
    # 35. Tiruvarur
    "tiruvarur": {
        "city": "Tiruvarur",
        "district": "Tiruvarur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 10.7725,
        "lng": 79.6365,
        "places": [
            {"name": "Thyagaraja Temple & Aazhi Ther (Asia's Largest Chariot)", "category": "Culture", "lat": 10.7740, "lng": 79.6340, "is_outdoor": False, "duration": 2.5, "cost": 50, "desc": "Vast temple spanning 20 acres with 33-acre Kamalalayam temple pond and 300-tonne festival chariot."},
            {"name": "Muthupet Mangrove Eco Lagoon", "category": "Nature", "lat": 10.4000, "lng": 79.5100, "is_outdoor": True, "duration": 2.5, "cost": 150, "desc": "Scenic mangrove forest on the Palk Strait with wooden watchtower walks."},
            {"name": "Birthplace of Carnatic Music Trinity Memorial", "category": "Culture", "lat": 10.7700, "lng": 79.6380, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Memorial commemorating Tyagaraja, Muthuswami Dikshitar, and Syama Sastri."}
        ]
    },
    # 36. Ariyalur
    "ariyalur": {
        "city": "Ariyalur (Gangaikonda Cholapuram)",
        "district": "Ariyalur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.1401,
        "lng": 79.0786,
        "places": [
            {"name": "Gangaikonda Cholapuram Temple (UNESCO)", "category": "Culture", "lat": 11.2058, "lng": 79.4520, "is_outdoor": True, "duration": 2.5, "cost": 0, "desc": "Architectural masterpiece built by Rajendra Chola I after victorious military expedition to River Ganga."},
            {"name": "Ariyalur Fossil Museum & Badlands", "category": "Culture", "lat": 11.1350, "lng": 79.0800, "is_outdoor": False, "duration": 1.5, "cost": 50, "desc": "Paleontological site exhibiting 65-million-year-old dinosaur eggs, ammonites, and marine fossils."},
            {"name": "Karaivetti Bird Sanctuary", "category": "Nature", "lat": 10.9700, "lng": 79.0400, "is_outdoor": True, "duration": 2.5, "cost": 30, "desc": "One of the largest freshwater bird sanctuaries in South India hosting bar-headed geese."}
        ]
    },
    # 37. Perambalur
    "perambalur": {
        "city": "Perambalur",
        "district": "Perambalur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 11.2342,
        "lng": 78.8820,
        "places": [
            {"name": "Ranjankudi Fortress (Nawab of Carnatic)", "category": "Culture", "lat": 11.3120, "lng": 78.9630, "is_outdoor": True, "duration": 2.0, "cost": 25, "desc": "17th-century rock fortress with stone ramparts and underground prison tunnels."},
            {"name": "Chettikulam Ekambareswarar Temple", "category": "Culture", "lat": 11.1600, "lng": 78.7800, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Hilltop shrine dedicated to Lord Murugan and Lord Shiva built by Chola kings."},
            {"name": "Siruvachur Madhurakali Amman Temple", "category": "Culture", "lat": 11.2200, "lng": 78.8600, "is_outdoor": False, "duration": 1.5, "cost": 0, "desc": "Renowned historic mother goddess shrine visited by thousands on Mondays and Fridays."}
        ]
    },
    # 38. Tiruvallur
    "tiruvallur": {
        "city": "Tiruvallur",
        "district": "Tiruvallur",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 13.1432,
        "lng": 79.9083,
        "places": [
            {"name": "Sri Veeraraghava Swamy Temple", "category": "Culture", "lat": 13.1444, "lng": 79.9075, "is_outdoor": False, "duration": 2.0, "cost": 0, "desc": "108 Divya Desam shrine dedicated to Lord Vishnu in reclining Bhujanga Sayana posture."},
            {"name": "Pulicat Lake & Bird Sanctuary", "category": "Nature", "lat": 13.4167, "lng": 80.3167, "is_outdoor": True, "duration": 3.0, "cost": 100, "desc": "India's second largest brackish-water lagoon hosting flamingos, pelicans, and Dutch colonial cemeteries."},
            {"name": "Poondi Reservoir & Satyamoorthy Sagar Park", "category": "Nature", "lat": 13.1800, "lng": 79.8600, "is_outdoor": True, "duration": 2.0, "cost": 30, "desc": "Major freshwater reservoir supplying Chennai with botanical gardens and fossil museum."}
        ]
    }
}

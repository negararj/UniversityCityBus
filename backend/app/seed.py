"""Run with `python -m app.seed` to (re)create tables and load real stops.

Source: the official University City of Sharjah transportation page
(https://universitycity.gov.ae/en/transportation/), via the Google My Maps
layer linked from that page. Coordinates are (lat, lng); the raw KML export
lists them as (lng, lat), already flipped here.

This is a dev-only convenience script: it wipes and reloads the whole table
every run. That's fine for SQLite while we're iterating, but isn't how
you'd evolve a schema against a real database with real data in it — that's
what a migration tool (e.g. Alembic) is for. We'll introduce that when we
move to Postgres.
"""

from .database import Base, SessionLocal, engine
from .models import Stop

STOPS = [
    # King Faisal Route — pickup points feeding the King Faisal line
    {"name": "Next to the Sharjah Cooperative Society", "lat": 25.334213, "lng": 55.371695, "route": "King Faisal"},
    {"name": "In front of the Car Service Station", "lat": 25.330038, "lng": 55.371131, "route": "King Faisal"},
    {"name": "In front of Adnoc Station", "lat": 25.329886, "lng": 55.371740, "route": "King Faisal"},
    {"name": "In front of Alhalabi Factory", "lat": 25.315974, "lng": 55.381562, "route": "King Faisal"},
    {"name": "Gref Mandi Restaurant", "lat": 25.318364, "lng": 55.383899, "route": "King Faisal"},
    {"name": "In front of Al-Shamia Sweets", "lat": 25.320120, "lng": 55.385486, "route": "King Faisal"},
    {"name": "In front of Al-Majaz Park", "lat": 25.323251, "lng": 55.388436, "route": "King Faisal"},
    {"name": "In front of Al-Kalhah Restaurant", "lat": 25.331072, "lng": 55.391177, "route": "King Faisal"},
    {"name": "In front of KFC", "lat": 25.337870, "lng": 55.386547, "route": "King Faisal"},
    {"name": "In front of King Faisal Mosque", "lat": 25.348818, "lng": 55.387018, "route": "King Faisal"},
    {"name": "In front of Al-Mashreq Bank", "lat": 25.345531, "lng": 55.392187, "route": "King Faisal"},
    {"name": "In front of Mega Mall", "lat": 25.344392, "lng": 55.397030, "route": "King Faisal"},
    {"name": "Opposite Sindbad Bakery", "lat": 25.349823, "lng": 55.399712, "route": "King Faisal"},
    {"name": "In front of Jesco Supermarket", "lat": 25.355489, "lng": 55.405981, "route": "King Faisal"},
    {"name": "Al-Sahabah Mosque", "lat": 25.345328, "lng": 55.421860, "route": "King Faisal"},
    {"name": "Hamriyah Area next to the Mosque", "lat": 25.479658, "lng": 55.523497, "route": "King Faisal"},
    {"name": "Al-Taawun Roundabout", "lat": 25.309367, "lng": 55.371469, "route": "King Faisal"},
    {"name": "In front of Afamia Al-Sham Supermarket", "lat": 25.315807, "lng": 55.376340, "route": "King Faisal"},
    {"name": "In front of Al-Etihad Insurance", "lat": 25.326494, "lng": 55.370965, "route": "King Faisal"},
    {"name": "Old Expo", "lat": 25.320163, "lng": 55.380448, "route": "King Faisal"},
    {"name": "In front of Alpha Al Seha Pharmacy", "lat": 25.306059, "lng": 55.366006, "route": "King Faisal"},

    # Al Heerah Route
    {"name": "Rona Square", "lat": 25.393283, "lng": 55.426617, "route": "Al Heerah"},
    {"name": "In front of Al-Hira Police", "lat": 25.386643, "lng": 55.414513, "route": "Al Heerah"},
    {"name": "In front of Al-Fisht Park", "lat": 25.383798, "lng": 55.408108, "route": "Al Heerah"},
    {"name": "In front of Al-Madinah Supermarket", "lat": 25.376006, "lng": 55.403069, "route": "Al Heerah"},
    {"name": "In front of Al-Anjad Police", "lat": 25.373751, "lng": 55.406842, "route": "Al Heerah"},
    {"name": "Nasiriyah Station", "lat": 25.371106, "lng": 55.411283, "route": "Al Heerah"},
    {"name": "In front of Shahoof Al-Fareej Restaurant", "lat": 25.367969, "lng": 55.415370, "route": "Al Heerah"},
    {"name": "Before the traffic light", "lat": 25.365264, "lng": 55.418751, "route": "Al Heerah"},
    {"name": "After the traffic light", "lat": 25.361449, "lng": 55.422426, "route": "Al Heerah"},
    {"name": "In front of HH the Ruler's office", "lat": 25.358018, "lng": 55.425689, "route": "Al Heerah"},
    {"name": "Opposite to Sharjah TV", "lat": 25.352998, "lng": 55.425725, "route": "Al Heerah"},

    # Returning Points — drop-off points at each university inside University City
    {"name": "UOS - M3", "lat": 25.283234, "lng": 55.474651, "route": "Returning Points"},
    {"name": "UOS - W3", "lat": 25.291245, "lng": 55.480560, "route": "Returning Points"},
    {"name": "UOS - Fine Arts", "lat": 25.296264, "lng": 55.482804, "route": "Returning Points"},
    {"name": "UOS - Medical College", "lat": 25.301524, "lng": 55.486406, "route": "Returning Points"},
    {"name": "AUS - Bus Station", "lat": 25.307864, "lng": 55.490790, "route": "Returning Points"},
    {"name": "HCT Building A", "lat": 25.293722, "lng": 55.478897, "route": "Returning Points"},
    {"name": "HCT Building B", "lat": 25.284496, "lng": 55.470478, "route": "Returning Points"},
    {"name": "Al Qasimia - Men's", "lat": 25.299347, "lng": 55.465844, "route": "Returning Points"},
    {"name": "Qasimia - Women's", "lat": 25.293714, "lng": 55.466454, "route": "Returning Points"},

    # Central Region
    {"name": "Suhaila Nursery Parking Area", "lat": 25.347652, "lng": 55.966544, "route": "Central Region"},
    {"name": "Opposite of Dubai Islamic Bank", "lat": 25.279015, "lng": 55.880019, "route": "Central Region"},
    {"name": "Bridge 12 Al Dhaid Road", "lat": 25.277050, "lng": 55.818119, "route": "Central Region"},
    {"name": "Bridge 11 Al Dhaid Road", "lat": 25.276869, "lng": 55.791815, "route": "Central Region"},
    {"name": "Bridge 10 Al Dhaid Road", "lat": 25.275275, "lng": 55.736515, "route": "Central Region"},
    {"name": "Bridge 8 Al Dhaid Road", "lat": 25.294096, "lng": 55.614867, "route": "Central Region"},
    {"name": "Bridge 6 Al Dhaid Road", "lat": 25.306813, "lng": 55.583885, "route": "Central Region"},
    {"name": "Bridge 5 Al Dhaid Road", "lat": 25.315535, "lng": 55.543696, "route": "Central Region"},
    {"name": "Al Maleeha Ladies Club", "lat": 25.132803, "lng": 55.889317, "route": "Central Region"},
    {"name": "Hadera Ladies Park", "lat": 25.170072, "lng": 55.957817, "route": "Central Region"},
    {"name": "Shabiyat Akhaidher Mosque", "lat": 25.086960, "lng": 55.954159, "route": "Central Region"},
    {"name": "Shabiyat Bel Ejeed Mosque", "lat": 25.169985, "lng": 55.880573, "route": "Central Region"},
    {"name": "Shaabiyat Saif Awadh Mosque", "lat": 25.169526, "lng": 55.876676, "route": "Central Region"},
    {"name": "Al Thameed Ladies Club", "lat": 25.010628, "lng": 55.876544, "route": "Central Region"},
    {"name": "Al-Bahais Roundabout", "lat": 25.017318, "lng": 55.843416, "route": "Central Region"},
    {"name": "AlFaya Roundabout", "lat": 25.040110, "lng": 55.808880, "route": "Central Region"},
    {"name": "Mahafiz - AlFaya Roundabout", "lat": 25.050414, "lng": 55.805034, "route": "Central Region"},
    {"name": "Al-Madam Ladies Club", "lat": 24.970546, "lng": 55.775807, "route": "Central Region"},
    {"name": "Nazwa Roundabout", "lat": 25.063555, "lng": 55.709765, "route": "Central Region"},
    {"name": "Al Dhaid Ladies Club", "lat": 25.296114, "lng": 55.875511, "route": "Central Region"},
    {"name": "Al Hisn Ladies Park", "lat": 25.296682, "lng": 55.878896, "route": "Central Region"},
    {"name": "Al-Mina Supermarket", "lat": 25.290150, "lng": 55.881899, "route": "Central Region"},
    {"name": "Al-Taiba Park", "lat": 25.271839, "lng": 55.875504, "route": "Central Region"},

    # Eastern Region
    {"name": "Abu Ayoub Al-Ansari School", "lat": 25.063569, "lng": 56.348218, "route": "Eastern Region"},
    {"name": "Opposite of Khorfakkan Ladies Club", "lat": 25.342425, "lng": 56.344034, "route": "Eastern Region"},
    {"name": "Next to Dibba Al-Hisn Club", "lat": 25.609848, "lng": 56.267418, "route": "Eastern Region"},
    {"name": "Wadi El Helou Ladies Club", "lat": 24.948937, "lng": 56.208011, "route": "Eastern Region"},
    {"name": "Parking area of Social Services Kalba Branch", "lat": 25.021724, "lng": 56.349182, "route": "Eastern Region"},
    {"name": "Sidra Park Kalba", "lat": 25.053183, "lng": 56.354639, "route": "Eastern Region"},
    {"name": "Amr Ibn Al-Aas Street", "lat": 25.067592, "lng": 56.355604, "route": "Eastern Region"},
    {"name": "Next to Kalba English School", "lat": 25.076164, "lng": 56.356215, "route": "Eastern Region"},
    {"name": "Kalba Public Beach Park", "lat": 25.084227, "lng": 56.358515, "route": "Eastern Region"},
    {"name": "Opposite of Al-Adl Mosque", "lat": 25.096529, "lng": 56.358456, "route": "Eastern Region"},
    {"name": "Al-Lulayyah Park", "lat": 25.394633, "lng": 56.355093, "route": "Eastern Region"},
    {"name": "Zubara Park", "lat": 25.403983, "lng": 56.356664, "route": "Eastern Region"},
    {"name": "Atika School", "lat": 25.398482, "lng": 56.335947, "route": "Eastern Region"},
    {"name": "Al-Metalaa Park", "lat": 25.371577, "lng": 56.347899, "route": "Eastern Region"},
    {"name": "Al-Dar Medical Center", "lat": 25.357497, "lng": 56.349402, "route": "Eastern Region"},
    {"name": "Dubai Islamic Bank", "lat": 25.354629, "lng": 56.351077, "route": "Eastern Region"},
    {"name": "Omar Ibn Alkhattab Mosque", "lat": 25.343796, "lng": 56.348335, "route": "Eastern Region"},
    {"name": "Next to Awf Bin Harith School", "lat": 25.339109, "lng": 56.348495, "route": "Eastern Region"},
    {"name": "Next to Etisalat Building", "lat": 25.335711, "lng": 56.348171, "route": "Eastern Region"},
    {"name": "Khorfakkan Comprehensive Police Station", "lat": 25.328947, "lng": 56.345327, "route": "Eastern Region"},
    {"name": "In front of Al Khoros Park", "lat": 25.369889, "lng": 56.000278, "route": "Eastern Region"},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(Stop).delete()
        db.add_all(Stop(**s) for s in STOPS)
        db.commit()
        print(f"Seeded {len(STOPS)} stops.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

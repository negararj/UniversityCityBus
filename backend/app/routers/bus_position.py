import statistics

from fastapi import APIRouter

from .. import live_sessions, schemas

router = APIRouter()


@router.get("/bus-position/{route}", response_model=schemas.BusPositionOut)
def get_bus_position(route: str):
    sessions = live_sessions.get_live_sessions(route)

    if not sessions:
        return schemas.BusPositionOut(route=route, status="unknown", lat=None, lng=None, rider_count=0)

    latitudes = [session.lat for session in sessions]
    longitudes = [session.lng for session in sessions]

    median_lat = statistics.median(latitudes)
    median_lng = statistics.median(longitudes)

    return schemas.BusPositionOut(route=route, status="estimated", lat=median_lat, lng=median_lng, rider_count=len(sessions))

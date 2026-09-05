"""In-memory store of riders currently checked in to a bus route.

Lives only in this process's memory — fine while there's a single backend
process. If we ever run multiple backend instances behind a load balancer,
this would need to move to something shared, like Redis.
"""

import time
from dataclasses import dataclass, field

STALE_AFTER_SECONDS = 60


@dataclass
class Session:
    route: str
    lat: float
    lng: float
    last_ping: float = field(default_factory=time.time)


_sessions: dict[str, Session] = {}


def add_session(session_id: str, route: str, lat: float, lng: float) -> None:
    _sessions[session_id] = Session(route=route, lat=lat, lng=lng)


def update_ping(session_id: str, lat: float, lng: float) -> None:
    session = _sessions.get(session_id)
    if session is None:
        return
    session.lat = lat
    session.lng = lng
    session.last_ping = time.time()


def remove_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def get_live_sessions(route: str) -> list[Session]:
    now = time.time()
    return [
        s
        for s in _sessions.values()
        if s.route == route and now - s.last_ping <= STALE_AFTER_SECONDS
    ]

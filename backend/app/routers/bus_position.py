from fastapi import APIRouter

from .. import live_sessions, schemas

router = APIRouter()

# TODO(you): implement this endpoint.
#
# It should:
#   - be a GET endpoint at "/bus-position/{route}" (full path once combined
#     with the "/api" prefix in main.py: GET /api/bus-position/{route})
#   - declare `response_model=schemas.BusPositionOut`
#   - take `route: str` as a path parameter (FastAPI fills it in from the
#     URL automatically — no Depends() needed for this one)
#   - call `live_sessions.get_live_sessions(route)` to get the list of
#     currently-live Session objects for that route (each has .lat, .lng)
#   - if the list is empty, return:
#       schemas.BusPositionOut(route=route, status="unknown", lat=None,
#                               lng=None, rider_count=0)
#   - otherwise, compute the median lat and median lng across the live
#     sessions (see Python's `statistics.median` — takes a list of numbers)
#     and return:
#       schemas.BusPositionOut(route=route, status="estimated",
#                               lat=<median lat>, lng=<median lng>,
#                               rider_count=<how many sessions>)
#
# Why median instead of average: one rider with a bad/wildly wrong GPS
# reading shouldn't drag the whole estimate off with it the way it would
# with a mean.

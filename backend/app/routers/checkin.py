"""WebSocket endpoint riders connect to for the duration of their ride.

Protocol (JSON messages over the socket):
  client -> server  {"type": "checkin", "route": "King Faisal", "lat": .., "lng": ..}
  server -> client  {"type": "checked_in", "sessionId": "..."}
  client -> server  {"type": "ping", "lat": .., "lng": ..}   (repeat periodically)
  client -> server  {"type": "checkout"}                      (or just close the socket)

If the socket just drops (app closed, network lost, phone locked hard enough
to kill the connection) the `finally` block still cleans the session up —
we don't rely on the client sending "checkout" cleanly.
"""

import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .. import live_sessions

router = APIRouter()


@router.websocket("/ws/checkin")
async def checkin(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())

    try:
        while True:
            message = await websocket.receive_json()
            msg_type = message.get("type")

            if msg_type == "checkin":
                live_sessions.add_session(
                    session_id, message["route"], message["lat"], message["lng"]
                )
                await websocket.send_json(
                    {"type": "checked_in", "sessionId": session_id}
                )

            elif msg_type == "ping":
                live_sessions.update_ping(session_id, message["lat"], message["lng"])

            elif msg_type == "checkout":
                break

    except WebSocketDisconnect:
        pass
    finally:
        live_sessions.remove_session(session_id)

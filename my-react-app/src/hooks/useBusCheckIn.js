import { useCallback, useRef, useState } from 'react'

const WS_URL = 'ws://localhost:8000/ws/checkin'

// Owns the WebSocket connection for the duration of a ride: opens it,
// sends the initial checkin, then keeps sending pings as the browser's
// geolocation watch reports new positions, until checkOut() (or the
// component unmounting) tears it all down.
//
// wsRef/watchIdRef are refs, not state, because they're plumbing the
// effect needs to reach across renders/callbacks — putting them in state
// would trigger pointless re-renders every time a ping goes out.
export function useBusCheckIn() {
  const [checkedIn, setCheckedIn] = useState(false)
  const [error, setError] = useState(null)
  const wsRef = useRef(null)
  const watchIdRef = useRef(null)

  const checkIn = useCallback((route) => {
    setError(null)

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const ws = new WebSocket(WS_URL)
        wsRef.current = ws

        ws.onopen = () => {
          ws.send(
            JSON.stringify({
              type: 'checkin',
              route,
              lat: pos.coords.latitude,
              lng: pos.coords.longitude,
            })
          )
        }

        ws.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (data.type === 'checked_in') {
            setCheckedIn(true)
            watchIdRef.current = navigator.geolocation.watchPosition(
              (p) => {
                if (ws.readyState === WebSocket.OPEN) {
                  ws.send(
                    JSON.stringify({
                      type: 'ping',
                      lat: p.coords.latitude,
                      lng: p.coords.longitude,
                    })
                  )
                }
              },
              (err) => console.error('watchPosition error', err)
            )
          }
        }

        ws.onerror = () => {
          setError('Connection to the server failed.')
        }

        ws.onclose = () => {
          setCheckedIn(false)
        }
      },
      () => {
        setError('Location access is needed to check in.')
      }
    )
  }, [])

  const checkOut = useCallback(() => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current)
      watchIdRef.current = null
    }
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'checkout' }))
      wsRef.current.close()
      wsRef.current = null
    }
    setCheckedIn(false)
  }, [])

  return { checkedIn, error, checkIn, checkOut }
}

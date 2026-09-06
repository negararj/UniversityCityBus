import { useEffect, useState } from 'react'
import Card from '../components/Card.jsx'
import { useBusCheckIn } from '../hooks/useBusCheckIn.js'

// The routes riders can actually check into (excludes "Returning Points",
// which are drop-off markers, not a route someone boards).
const ROUTES = ['King Faisal', 'Al Heerah', 'Central Region', 'Eastern Region']

function Home() {
  // TODO(you): a `selectedRoute` state, defaulting to ROUTES[0].
  // Render a <select> (or a row of buttons, your call) letting the user
  // pick one of ROUTES, wired to this state.

  // TODO(you): pull { checkedIn, error, checkIn, checkOut } out of
  // useBusCheckIn(). Render a button that calls checkIn(selectedRoute)
  // when not checked in, or checkOut() when checked in — label it
  // accordingly ("Check In" / "Check Out"). Show `error` if it's set.
  // While checked in, disable the route picker (you can't switch routes
  // mid-ride without checking out first).

  // TODO(you): state for the live bus position: `busPosition` (start
  // null) holding whatever GET /api/bus-position/{route} last returned
  // ({ route, status, lat, lng, rider_count }).
  //
  // TODO(you): a useEffect that polls that endpoint every few seconds
  // (setInterval) for `selectedRoute`, storing the result in
  // `busPosition`. Things to think about:
  //   - this should run regardless of whether the user has checked in —
  //     you want to see the estimate even before boarding
  //   - it needs to re-fetch immediately when `selectedRoute` changes,
  //     not wait for the next interval tick
  //   - clear the interval in the effect's cleanup function, and encode
  //     `selectedRoute` in the effect's dependency array so it restarts
  //     cleanly when the route changes (fetch/setInterval calls made
  //     against a stale route are a common bug here — think through why)
  //   - route name has a space in it ("King Faisal") — needs
  //     encodeURIComponent() when building the URL

  return (
    <div className="screen">
      <h1>Live Bus Tracker</h1>
      <p className="screen-subtitle">
        Pick your route, check in once you're on the bus, and see the
        estimated position from everyone currently checked in.
      </p>

      {/*
        TODO(you): render, roughly:
          - the route picker
          - the check-in/check-out button (+ error message if any)
          - a <Card> showing busPosition: if status is "unknown", say so
            ("No riders currently checked in on this route"); if
            "estimated", show the lat/lng and rider_count
            ("~3 riders reporting")
      */}
    </div>
  )
}

export default Home

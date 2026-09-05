import { useEffect, useState } from 'react'
import Card from '../components/Card.jsx'

function haversineDistanceMeters(lat1, lng1, lat2, lng2) {
  const lat1Rad = lat1 * Math.PI / 180
  const lng1Rad = lng1 * Math.PI / 180
  const lat2Rad = lat2 * Math.PI / 180
  const lng2Rad = lng2 * Math.PI / 180

  const dLat = lat2Rad - lat1Rad
  const dLng = lng2Rad - lng1Rad

  const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1Rad) * Math.cos(lat2Rad) * Math.sin(dLng / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  const R = 6371000 // Earth's radius in meters
  const distance = R * c

  return distance
}

function NearestStop() {
  const [position, setPosition] = useState(null)
  const [status, setStatus] = useState('loading')
  const [stops, setStops] = useState([])
  const [stopsStatus, setStopsStatus] = useState('loading')

  useEffect(() => {
    fetch('http://localhost:8000/api/stops')
      .then((res) => res.json())
      .then((data) => {
        setStops(data)
        setStopsStatus('ready')
      })
      .catch((err) => {
        console.error(err)
        setStopsStatus('error')
      })

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        })
        setStatus('ready')
      },
      (err) => {
        console.error(err)
        setStatus('error')
      }
    )
  }, [])

  const combinedStatus =
    status === 'error' || stopsStatus === 'error'
      ? 'error'
      : status === 'ready' && stopsStatus === 'ready'
        ? 'ready'
        : 'loading'

  const sortedStops = position
    ? stops.map((stop) => ({
        ...stop,
        distanceM: haversineDistanceMeters(position.lat, position.lng, stop.lat, stop.lng),
      })).sort((a, b) => a.distanceM - b.distanceM)
    : []

  return (
    <div className="screen">
      <h1>Nearest Stop</h1>
      <p className="screen-subtitle">
        Stops near your current location, closest first.
      </p>

      {combinedStatus === 'loading' && <p>Finding your location and nearby stops...</p>}
      {combinedStatus === 'error' && (
        <p>
          Couldn't load stops — check your location permission and that the
          backend is running.
        </p>
      )}
      {combinedStatus === 'ready' && (
        <div className="stop-list">
          {sortedStops.map((stop) => {
            const distanceM = stop.distanceM
            const formattedDistance =
              distanceM < 1000
                ? `${Math.round(distanceM)} m`
                : `${(distanceM / 1000).toFixed(1)} km`

            return (
              <Card key={stop.id}>
                <h3>{stop.name}</h3>
                <p>{formattedDistance}</p>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default NearestStop

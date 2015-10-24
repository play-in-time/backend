# inTime Backend

## API Documentation:

Base URL: `api.playinti.me`

### GET `/tracks_for_duration`
##### Parameters:
  **`playlist__id`**: The id of the Spotify playlist superset to draw from.
  **`duration`**: The time (in seconds) of the desired playback interval
##### Response:
  A JSON-formatted string containing a list of Spotify track ids `{track1, track2, ..., trackN}`


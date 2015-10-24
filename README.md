# inTime Backend

## API Documentation:

Base URL: `api.playinti.me`

### GET: `/tracks_for_duration`
##### Parameters:
  **`playlist_id`**: The id of the Spotify playlist superset to draw from.
  **`duration`**: The time (in seconds) of the desired playback interval
##### Response:
  A JSON-formatted string containing a list of Spotify tracks according to Spotify's formatting

### GET: `/just_play`
##### Parameters:
  **`duration`**: The time (in seconds) of the desired playback interval
##### Response:
  A JSON-formatting string containing a list of Spotify tracks

### POST: `/update_tracklist`
Expects that the client has determined already whether or not it is necessary to actually update the tracklist given a new interval endpoint. That is, if the new endpoint falls before or at the end of the currently playing song, the client should not send a request and rather just play out the song to its end.
##### Parameters:
  **`playlist_id`**: The id of the Spotify playlist to draw from
  **`played`**: A list of songs already played
  **`duration`**: Interval length in seconds - i.e. `new_time - end_of_current_song`.
##### Response:
  A JSON-formatted string containing a list of Spotify tracks to play after the current song

### GET: `/playlists`
##### Parameters:
  none
##### Response:
  JSON-formatted string of a list of playlists. Each element has `playlist_name` and `playlist_id`.

## Contributors:

**Backend**: Chris Hinstorff, Arun Drelich, Sam Slate, Josh White

**Frontend and UI**: Tony Nguyen, Deanna Baris, Vincent Tran

**Design**: Lexie Kirsch, Tess Cotter


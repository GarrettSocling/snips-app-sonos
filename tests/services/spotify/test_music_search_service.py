import pytest
import mock

from snipssonos.services.spotify.music_search_service import SpotifyMusicSearchService, SpotifyAPISearchQueryBuilder
from tests.services.spotify.raw_responses import *


# Testing Spotify Music Service
def test_correct_parsing_of_tracks_for_correct_response():
    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    tracks = music_search_service._parse_track_results(TRACKS)

    assert len(tracks) == 20
    assert tracks[0].uri == "spotify:track:3f9HJzevC4sMYGDwj7yQwd"


def test_correct_parsing_of_tracks_with_empty_response():
    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    tracks = music_search_service._parse_track_results(EMPTY_TRACKS)

    assert len(tracks) == 0


def test_correct_parsing_of_playlists_for_correct_response():
    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    playlists = music_search_service._parse_playlist_results(PLAYLISTS)

    assert len(playlists) == 20
    assert playlists[0].name == "Peaceful Piano"
    assert playlists[0].uri == "spotify:user:spotify:playlist:37i9dQZF1DX4sWSpwq3LiO"


def test_correct_parsing_of_artists_for_correct_response():
    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    artists = music_search_service._parse_artists_results(ARTISTS)

    assert len(artists) == 1
    assert artists[0].name == "Tornado Wallace"
    assert artists[0].uri == "spotify:artist:6GNWPphcJ5CtIwCJVV1lLT"


def test_correct_parsing_of_albums_for_correct_response():
    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    artists = music_search_service._parse_album_results(ALBUMS)

    assert len(artists) == 2
    assert artists[0].name == "KIDS SEE GHOSTS"
    assert artists[0].uri == "spotify:album:6pwuKxMUkNg673KETsXPUV"


@mock.patch.object(SpotifyMusicSearchService, 'search_album')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_album_when_search_album_in_playlist_returns_no_results(mock_spotify_client, mock_search_album):
    mock_spotify_client.execute_query.return_value = EMPTY_ALBUMS
    album_name = "Ash"

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_album_in_playlist(album_name, "Summer")

    mock_search_album.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_album')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_album_when_search_album_for_artist_returns_no_results(mock_spotify_client, mock_search_album):
    mock_spotify_client.execute_query.return_value = EMPTY_ALBUMS
    album_name = "Ash"

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_album_for_artist(album_name, "Ibeyi")

    mock_search_album.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_album')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_album_when_search_album_for_artist_and_for_playlist_returns_no_results(mock_spotify_client,
                                                                                                   mock_search_album):
    mock_spotify_client.execute_query.return_value = EMPTY_ALBUMS
    album_name = "Ash"

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_album_for_artist_and_for_playlist(album_name, "Ibeyi", "Summer")

    mock_search_album.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_artist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_artist("Deathless", "Ibeyi")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_album(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_album("Deathless", "Ash")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_playlist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_playlist("Deathless", "Vibing")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_album_and_for_artist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_album_and_for_artist("Deathless", "Ash", "Ibeyi")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_album_and_for_playlist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_album_and_for_playlist("Deathless", "Ash", "Vibing")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_artist_and_for_playlist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_artist_and_for_playlist("Deathless", "Ibeyi", "Vibing")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_track')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_artist_and_for_playlist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_TRACKS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_track_for_album_and_for_artist_and_for_playlist("Deathless", "Ash", "Ibeyi", "Vibing")

    mock_search_track.assert_called()


@mock.patch.object(SpotifyMusicSearchService, 'search_artist')
@mock.patch('snipssonos.services.spotify.music_search_service.SpotifyClient')
def test_fallback_to_search_track_for_artist_and_for_playlist(mock_spotify_client, mock_search_track):
    mock_spotify_client.execute_query.return_value = EMPTY_ARTISTS

    music_search_service = SpotifyMusicSearchService("client_id", "client_secret", "refresh_token")
    music_search_service.client = mock_spotify_client
    music_search_service.search_artist_for_playlist("Ibeyi", "Summer")

    mock_search_track.assert_called()

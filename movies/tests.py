from unittest.mock import patch

import requests
from rest_framework import status
from rest_framework.test import APITestCase


class MovieAPITests(APITestCase):

    def setUp(self):
        response = self.client.post(
            "/register/",
            {
                "username": "movieuser",
                "password": "TestPassword123"
            },
            format="json"
        )

        self.access_token = response.data["access_token"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    @patch("movies.views.MovieAPIService.get_movies")
    def test_get_movies(self, mock_get_movies):
        mock_get_movies.return_value = [
            {
                "id": 84,
                "title": "Raiders of the Lost Ark",
                "posterURL": "https://example.com/poster.jpg",
                "imdbId": "tt0082971"
            }
        ]

        response = self.client.get("/movies/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data[0]["title"],
            "Raiders of the Lost Ark"
        )

        mock_get_movies.assert_called_once()

    def test_get_movies_without_authentication(self):
        self.client.credentials()

        response = self.client.get("/movies/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    @patch("movies.views.MovieAPIService.get_movies")
    def test_movie_api_timeout(self, mock_get_movies):
        mock_get_movies.side_effect = requests.exceptions.Timeout

        response = self.client.get("/movies/")

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

        self.assertEqual(
            response.data["error"],
            "Movie API request timed out."
        )

    @patch("movies.views.MovieAPIService.get_movies")
    def test_movie_api_request_exception(self, mock_get_movies):
        mock_get_movies.side_effect = requests.exceptions.RequestException

        response = self.client.get("/movies/")

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

        self.assertEqual(
            response.data["error"],
            "Unable to fetch movies from movie API."
        )
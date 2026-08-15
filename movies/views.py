import requests

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.movie_api import MovieAPIService


class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = MovieAPIService()

        try:
            movies = service.get_movies()

            return Response(
                movies,
                status=status.HTTP_200_OK
            )

        except requests.exceptions.Timeout:
            return Response(
                {
                    "error": "Movie API request timed out."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except requests.exceptions.RequestException:
            return Response(
                {
                    "error": "Unable to fetch movies from movie API."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
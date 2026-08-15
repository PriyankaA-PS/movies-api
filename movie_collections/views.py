from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.migrations import serializer
from django.db.models import Model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CollectionSerializers, CollectionMovieListSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from collections import Counter
from .models import Collection, CollectionMovie

#
# class CollectionCreateView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = CollectionSerializers(data = request.data, context= {"request": request})
#
#
#         if serializer.is_valid():
#             collection = serializer.save()
#
#             return Response(
#                 {
#                     "collection_uuid" : str(collection.uuid)
#                 }, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class CollectionListView(APIView):
#         permission_classes = [IsAuthenticated]
#
#         def get(self, request):
#             collections = Collection.objects.filter(user = request.user)
#
#
#             genre_counter = Counter()
#
#             for collection in collections:
#                 for movie in collection.movies.all():
#                     genres = movie.genre.split(",")
#
#                     for genre in genres:
#                         genre = genre.strip()
#
#                         if genre:
#                             genre_counter[genre] += 1
#             favourite_genres = [genre for genre, count in genre_counter.max_common(3)]
#             serializer = CollectionMovieListSerializer(collections, many=True)
#
#             return Response({
#                 "is_success" : True,
#                 "data": {
#                     "collections": serializer.data,
#                     "favourite_genres": ",".join(favourite_genres)
#                 }
#             }, status=status.HTTP_200_OK)
#

class CollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        collections = Collection.objects.filter(user=request.user)

        genre_count = Counter()

        for collection in collections:
            for movie in collection.movies.all():
                for genre in movie.genres.split(","):
                    genre = genre.strip()

                    if genre:
                        genre_count[genre] += 1
        favourite_genres = [genre for genre, count in genre_count.most_common(3)]


        serializer = CollectionMovieListSerializer(collections, many= True)

        return Response({
            "is_success": True,
            "data":{
                "collections" : serializer.data,
                "favourite_genres" : ",".join(favourite_genres)
            }
        })


    def post(self, request):
        serializer = CollectionSerializers(data=request.data, context={"request":request})

        if serializer.is_valid():
            collection = serializer.save()

            return Response({
                "collection_uuid": str(collection.uuid)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, collection_uuid):
        try:
            collection = Collection.objects.get(uuid=collection_uuid, user=request.user)
        except Collection.DoesNotExist:
            return Response({
                "error": "Collection not Found"
            }, status=status.HTTP_404_NOT_FOUND)


        serializers = CollectionSerializers(collection)

        return Response(serializers.data, status=status.HTTP_200_OK)
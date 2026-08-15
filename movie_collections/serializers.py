
from rest_framework import serializers
from .models import Collection, CollectionMovie


class CollectionMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = CollectionMovie
        fields = [
            "title",
            "description",
            "uuid",
            "genres"
        ]

class CollectionSerializers(serializers.ModelSerializer):
    movies = CollectionMovieSerializers(many=True)

    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "movies"
        ]

    def create(self, validated_data):
        movies_data = validated_data.pop("movies")

        collection = Collection.objects.create(user = self.context["request"].user, **validated_data)

        for movie_data in movies_data:
            CollectionMovie.objects.create(collection = collection, **movie_data)

        return collection

class CollectionMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "title",
            "uuid",
            "description"
        ]
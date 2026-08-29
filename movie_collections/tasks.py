import time
from collections import Counter

from celery import shared_task

from .models import Collection, CollectionActivityLog


@shared_task
def generate_collection_report(collection_id):
    """
    Deliberately slow "report generation" job, so triggering it from an API
    view makes the point of using Celery obvious: the HTTP response comes
    back immediately while this keeps running in the worker process.

    Runs entirely outside the request/response cycle — no `request`,
    no `response`, nothing DRF-specific. A task only gets what you pass it
    (here: a plain collection_id, not the Collection instance itself,
    since instances don't serialize onto the broker cleanly).
    """
    collection = Collection.objects.get(pk=collection_id)

    time.sleep(5)  # stand-in for something actually slow: PDF export,
                    # calling a third-party API, crunching a lot of rows...

    genre_counts = Counter()
    for movie in collection.movies.all():
        for genre in movie.genres.split(","):
            genre = genre.strip()
            if genre:
                genre_counts[genre] += 1

    top_genres = ", ".join(genre for genre, _ in genre_counts.most_common(3))

    CollectionActivityLog.objects.create(
        collection=collection,
        action=f"Report generated: {collection.movies.count()} movies, "
               f"top genres: {top_genres or 'none'}",
    )

    # Whatever is returned here is what AsyncResult(task_id).result gives
    # back to the API once the task finishes.
    return {
        "collection_id": collection_id,
        "movie_count": collection.movies.count(),
        "top_genres": top_genres,
    }

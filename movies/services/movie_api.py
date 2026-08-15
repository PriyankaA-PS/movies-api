import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class MovieAPIService:
        def __init__(self):
            self.url = "https://api.sampleapis.com/movies/action-adventure"

            retry_stratergy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist= [500,502,503,504],
                allowed_methods=["GET"]
            )

            adapter = HTTPAdapter(max_retries=retry_stratergy)

            self.session = requests.session()
            self.session.mount("https://", adapter)

        def get_movies(self):
            response = self.session.get(self.url, timeout=5)

            response.raise_for_status()

            return response.json()








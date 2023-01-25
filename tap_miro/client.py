"""REST client handling, including MiroStream base class."""

from typing import Callable, Generator, Any
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
import time

API_URL = 'https://api.miro.com'


class MiroStream(RESTStream):
    """Miro stream class."""
    @property
    def url_base(self) -> str:
        return self.config.get('api_url', API_URL)

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        access_token = self.config.get('access_token')
        return BearerTokenAuthenticator(self, access_token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {'Accept': 'application/json'}

        if "user_agent" in self.config:
            headers['User-Agent'] = self.config.get('user_agent')

        return headers

    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        def _backoff_from_headers(retriable_api_error) -> int:
            headers: dict = retriable_api_error.response.headers

            if 'X-RateLimit-Reset' in headers:
                retry_at = headers.get('X-RateLimit-Reset')
                return retry_at - int(time.time())

            return 0

        return self.backoff_runtime(value=_backoff_from_headers)

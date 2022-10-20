"""REST client handling, including MiroStream base class."""

from pathlib import Path
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import JSONPathPaginator, BaseAPIPaginator

SCHEMAS_DIR = Path(__file__).parent / Path('./schemas')

class MiroStream(RESTStream):
    """Miro stream class."""
    query = {}

    def records_cursor_key(self) -> str:
        """Record key that will be used to find team next to this id in the sorted list."""
        return None

    @property
    def url_base(self) -> str:
        return self.config.get('api_url')

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        access_token = self.config.get('access_token')
        return BearerTokenAuthenticator.create_for_stream(self, access_token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {'Accept': 'application/json'}

        if "user_agent" in self.config:
            headers['User-Agent'] = self.config.get('user_agent')
            
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a fresh paginator for this API endpoint."""
        jsonpath = f'$.data[-1:].{self.records_cursor_key}'
        return JSONPathPaginator(jsonpath)

    def get_url_params(self, context, next_page_token) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        pagination = {}

        if self.records_cursor_key:
            pagination['cursor'] = next_page_token
            limit = self.query.get('limit')

            if limit:
                pagination['limit'] = str(limit)

        query = self.query

        return {**pagination, **query}

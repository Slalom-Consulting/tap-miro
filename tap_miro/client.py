"""REST client handling, including MiroStream base class."""


from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import JSONPathPaginator, BaseAPIPaginator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class MiroStream(RESTStream):
    """Miro stream class."""
    url_base = "https://api.miro.com/v2"
    cursor_field = None
    query = {}

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("access_token")
        )


    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {
            "Accept": "application/json"
        }

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
            
        return headers


    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a fresh paginator for this API endpoint.
        Returns:
            A paginator instance.
        """
        jsonpath = f'$.data[-1:].{self.cursor_field}'
        return JSONPathPaginator(jsonpath)


    def get_url_params(self, context, next_page_token) -> dict:
        """Return a dictionary of values to be used in URL parameterization.
        If paging is supported, developers may override with specific paging logic.
        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.
        Returns:
            Dictionary of URL query parameters to use in the request.
        """
        default_limit = 100
        limit = self.query.get('limit')
        params = self.query

        if limit > default_limit:
            params['limit'] = default_limit

        if self.cursor_field is not None:
            params['cursor'] = next_page_token
            if limit is None:
                params['limit'] = default_limit

        return params

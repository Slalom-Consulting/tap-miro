"""REST client handling, including MiroStream base class."""

import time
from typing import Generator
from urllib.parse import parse_qsl

from memoization import cached
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import JSONPathPaginator
from singer_sdk.streams import RESTStream

API_URL = "https://api.miro.com"


class MiroStream(RESTStream):
    """Miro stream class."""

    next_page_token_jsonpath = ""

    @property
    def url_base(self) -> str:
        return self.config.get("api_url", API_URL)

    @property
    @cached  # type: ignore[override]
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        access_token = self.config["access_token"]
        return BearerTokenAuthenticator(self, access_token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {"Accept": "application/json"}

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config["user_agent"]

        return headers

    def backoff_wait_generator(self) -> Generator[float, None, None]:
        def _backoff_from_headers(retriable_api_error) -> int:
            headers: dict = retriable_api_error.response.headers

            if "X-RateLimit-Reset" in headers:
                retry_at = int(headers["X-RateLimit-Reset"])
                return retry_at - int(time.time())

            return 0

        return self.backoff_runtime(value=_backoff_from_headers)

    def get_new_paginator(self) -> JSONPathPaginator:
        return JSONPathPaginator(self.next_page_token_jsonpath)

    def _get_strem_config(self) -> dict:
        """Get parameters set in config."""
        config: dict = {}

        stream_configs = self.config.get("stream_config", [])
        if not stream_configs:
            return config

        config_list = [
            conf for conf in stream_configs if conf.get("stream") == self.name
        ] or [None]
        config_dict = config_list[-1] or {}
        stream_config = {k: v for k, v in config_dict.items() if k != "stream"}
        return stream_config

    def _get_stream_params(self) -> dict:
        stream_params = self._get_strem_config().get("parameters", "")
        return {qry[0]: qry[1] for qry in parse_qsl(stream_params.lstrip("?"))}

    def get_url_params(self, context, next_page_token) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        params = self._get_stream_params()
        params["limit"] = self.config["limit"]

        if next_page_token:
            params["cursor"] = next_page_token

        return params

"""Miro tap class."""

from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th

from tap_miro.streams import (
    #MiroStream,
    OrganizationMembersStream,
)

STREAM_TYPES = [
    OrganizationMembersStream
]

class TapMiro(Tap):
    """Miro tap class."""
    name = 'tap-miro'

    config_jsonschema = th.PropertiesList(
        th.Property(
            'access_token',
            th.StringType,
            required=True,
            description='Access token.'
        ),
        th.Property(
            'organization_id',
            th.StringType,
            required=True,
            description='The ID of an Organization.'
        ),
        th.Property(
            'limit',
            th.IntegerType,
            default=100,
            description='The response limit for paginated API streams. (Range: 0-100)'
        ),
        th.Property(
            "user_agent",
            th.StringType,
            description='The User agent to present to the API.'
        ),
        th.Property(
            'api_url',
            th.StringType,
            description='Override the url for the API service.'
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == '__main__':
    TapMiro.cli()

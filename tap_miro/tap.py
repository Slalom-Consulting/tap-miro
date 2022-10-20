"""Miro tap class."""

from typing import List
from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

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
            description='Access token'
        ),
        th.Property(
            'org_id',
            th.StringType,
            required=True,
            description='Organization id'
        ),
        th.Property(
            'api_url',
            th.StringType,
            default='https://api.miro.com',
            description='The url for the API service'
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

if __name__ == '__main__':
    TapMiro.cli()

"""Miro tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_miro.streams import (
    OrgMembersStream,
)

STREAM_TYPES = [
    OrgMembersStream
]


class TapMiro(Tap):
    """Miro tap class."""
    name = "tap-miro"

    config_jsonschema = th.PropertiesList(
#        th.Property(
#            "client_id",
#            th.StringType,
#            required=False,
#            description="The token to authenticate against the API service"
#        ),
#        th.Property(
#            "client_secret",
#            th.ArrayType(th.StringType),
#            required=False,
#            description="Project IDs to replicate"
#        ),
#        th.Property(
#            "auth_code",
#            th.DateTimeType,
#            required=False,
#            description="The earliest record date to sync"
#        ),
#        th.Property(
#            "redirect_uri",
#            th.StringType,
#            required=False,
#            description="The url for the API service"
#        ),
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="The url for the API service"
        ),
        th.Property(
            "org_id",
            th.StringType,
            required=True,
            description="The url for the API service"
        ),
#        th.Property(
#            "team_id",
#            th.StringType,
#            required=True,
#            description="The url for the API service"
#        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapMiro.cli()

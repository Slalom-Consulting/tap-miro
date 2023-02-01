"""Miro tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_miro.streams import OrganizationMembersStream

STREAM_TYPES = [OrganizationMembersStream]


class TapMiro(Tap):
    """Miro tap class."""

    name = "tap-miro"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="Access token for API.",
        ),
        th.Property(
            "organization_id",
            th.StringType,
            required=True,
            description="The ID of an Organization.",
        ),
        th.Property(
            "limit",
            th.IntegerType,
            default=100,
            description="The response limit for paginated API streams. (Range: 0-100)",
        ),
        th.Property(
            "user_agent",
            th.StringType,
            description="The User agent to present to the API.",
        ),
        th.Property(
            "api_url",
            th.StringType,
            description="Override the url for the API service.",
        ),
        th.Property(
            "stream_config",
            th.ArrayType(
                th.PropertiesList(
                    th.Property(
                        "stream",
                        th.StringType,
                        required=True,
                        description="Name of stream to apply a custom configuration.",
                    ),
                    th.Property(
                        "primary_keys",
                        th.ArrayType(th.StringType),
                        description="Override the default list of primary keys.",
                    ),
                    th.Property(
                        "replication_key",
                        th.StringType,
                        description="Override the default replication key.",
                    ),
                    th.Property(
                        "schema_discovery",
                        th.BooleanType,
                        description="Override the default schema and use discovery mode.",
                    ),
                    th.Property(
                        "schema",
                        th.StringType,
                        description="Override the default schema with a custom JSONSchema string.",
                    ),
                    th.Property(
                        "parameters",
                        th.StringType,
                        description="URL formatted parameters string to be used for stream.",
                    ),
                ),
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapMiro.cli()

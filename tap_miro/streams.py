"""Stream type classes for tap-miro."""

from pathlib import Path

from tap_miro.client import MiroStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class OrganizationMembersStream(MiroStream):
    """Organization Members stream."""

    name = "organization_members"
    path = "/v2/orgs/{organization_id}/members"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR.joinpath("org_members.json")
    records_jsonpath = "$.data[*]"
    next_page_token_jsonpath = "$.data[-1:].id"

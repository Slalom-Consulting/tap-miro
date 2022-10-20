"""Stream type classes for tap-miro."""

from pathlib import Path
from tap_miro.client import MiroStream

SCHEMAS_DIR = Path(__file__).parent / Path('./schemas')

class OrganizationMembersStream(MiroStream):
    """Define custom stream."""
    name = 'organization members'
    path = '/v2/orgs/{org_id}/members'
    primary_keys = ['id']
    replication_key = None
    schema_filepath = SCHEMAS_DIR / 'org_members.json'
    records_jsonpath = '$.data[*]'
    records_cursor_key = 'id'
    query = {
        'active': True,
        'license': 'full',
        'limit': 100,
        'role': 'organization_internal_user',
    }

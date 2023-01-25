"""Stream type classes for tap-miro."""

from pathlib import Path
from tap_miro.client import MiroStream
from singer_sdk.pagination import JSONPathPaginator

SCHEMAS_DIR = Path(__file__).parent / Path('./schemas')


class OrganizationMembersStream(MiroStream):
    """Define custom stream."""
    name = 'organization members'
    path = '/v2/orgs/{organization_id}/members'
    primary_keys = ['id']
    replication_key = None
    schema_filepath = SCHEMAS_DIR / 'org_members.json'
    records_jsonpath = '$.data[*]'
    next_page_token_jsonpath = '$.data[-1:].id'

    # TODO: make query a tap config
    query = {
        'active': True,
        'license': 'full',
        'role': 'organization_internal_user',
    }

    def get_new_paginator(self) -> JSONPathPaginator:
        return JSONPathPaginator(self.next_page_token_jsonpath)

    def get_url_params(self, context, next_page_token) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {
            'limit': self.query.get('limit') or self.config.get('limit')
        }

        if next_page_token:
            params['cursor'] = next_page_token

        if params:
            return {**params, **self.query}

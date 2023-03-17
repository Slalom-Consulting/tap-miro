"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_miro.tap import TapMiro
from tap_miro.tests.mock_api import mock_api

SAMPLE_CONFIG = {
    "access_token": "SampleToken",
    "organization_id": "SampleOrganizationId",
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapMiro, config=SAMPLE_CONFIG)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test, SAMPLE_CONFIG)
            continue

        test()


# TODO: Create additional tests as appropriate for your tap.

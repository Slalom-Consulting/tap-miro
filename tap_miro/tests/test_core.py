"""Tests standard tap features using the built-in SDK tests library."""

from requests_mock.exceptions import NoMockAddress
from singer_sdk.testing import get_standard_tap_tests

from tap_miro.tap import TapMiro
from tap_miro.tests.mock_api import mock_api, mock_param_api

SAMPLE_CONFIG = {
    "access_token": "SampleToken",
    "organization_id": "SampleOrganizationId",
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapMiro, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test, config)
            continue

        test()


# Run parameter test
def test_standard_tap_param_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG.copy()
    config["stream_config"] = {
        "organization_members": {"parameters": "active=true&license=full"}
    }

    tests = get_standard_tap_tests(TapMiro, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_param_api(test, config)

            config["stream_config"]["organization_members"][
                "parameters"
            ] = "active=true&license=free"

            try:
                mock_param_api(test, config)
            except NoMockAddress:
                pass
            except Exception:
                assert False

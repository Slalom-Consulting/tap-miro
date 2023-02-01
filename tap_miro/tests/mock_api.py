"""Mock API."""

import json

import requests_mock

API_URL = "https://api.miro.com"

mock_responses_path = "tap_miro/tests/mock_responses"

mock_config = {
    "organization_members": {
        "type": "stream",
        "endpoint": "/v2/orgs/{organization_id}/members",
        "file": "organization_members.json",
    }
}


def mock_api(func, SAMPLE_CONFIG):
    """Mock API."""

    def wrapper():
        with requests_mock.Mocker() as m:
            for k, v in mock_config.items():
                path = f"{mock_responses_path}/{v['file']}"

                if v["type"] == "stream":
                    endpoint = v["endpoint"]
                    for k, v in SAMPLE_CONFIG.items():
                        var = f"{{{k}}}"
                        if var in endpoint:
                            endpoint = endpoint.replace(var, v)

                    url = f"{API_URL}{endpoint}"

                    with open(path, "r") as f:
                        response = json.load(f)

                    m.get(url, json=response)

            func()

    wrapper()

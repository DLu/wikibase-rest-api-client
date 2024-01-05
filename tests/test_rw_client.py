import os

import pytest

from wikibase_rest_api_client import AuthenticatedClient
from wikibase_rest_api_client.api.labels import delete_item_label, replace_item_label
from wikibase_rest_api_client.api.properties import get_property
from wikibase_rest_api_client.models import LabelReplaceRequest
from wikibase_rest_api_client.types import Response

from .utils import assert_item_label

TEST_ITEM = "Q233445"
TEST_STRING_PROP = "P95180"
PROPS = [TEST_STRING_PROP]


@pytest.fixture
def client():
    token = os.environ.get("WIKIDATA_TEST_TOKEN")

    if token:
        return AuthenticatedClient(
            base_url="https://test.wikidata.org/w/rest.php/wikibase/v0/",
            token=token,
            headers={"User-Agent": "wikibase-rest-api-client/1.0.0"},
        )
    else:
        raise Exception(
            "No wikidata test token found so cannot do write tests")


# just confirm the item we are going to test with still exists
def test_get_test_props(client):
    for prop in PROPS:
        with client as client:
            response = get_property.sync_detailed(prop, client=client)
            assert type(response) == Response
            assert response.status_code == 200


def test_delete_item_label(client):
    with client as client:
        # set the label
        response = replace_item_label.sync_detailed(
            TEST_ITEM, "en", LabelReplaceRequest("Test label"), client=client)
        assert response.status_code == 200

        assert_item_label(client, TEST_ITEM, "en", "Test label")

        # delete the label
        response = delete_item_label.sync_detailed(
            TEST_ITEM, "en", client=client)

        # Check the response
        assert type(response) == Response
        assert response.status_code == 200
        assert response.content == b'"Label deleted"'

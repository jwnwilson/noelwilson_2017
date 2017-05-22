import pytest

from app import TornadoApp
application = TornadoApp()


@pytest.fixture
def app():
    return application


@pytest.mark.gen_test
def test_home_status(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200

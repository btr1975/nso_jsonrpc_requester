import pytest
import requests_mock
import json


@pytest.fixture
def trans_data():
    return {'jsonrpc': '2.0', 'result': {'th': 1}, 'id': 21052}


@pytest.fixture
def comet_data():
    return {'jsonrpc': '2.0', 'result': {'th': 1, 'handle': 42}, 'id': 21052}


@pytest.fixture
def system_data():
    return {'jsonrpc': '2.0', 'result': '4.7.3.1', 'id': 45890}


@pytest.fixture
def abort_data():
    return {'jsonrpc': '2.0', 'result': {}, 'id': 52081}


@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def request_data_login_get_trans(requests_mock_fixture, trans_data):
    return requests_mock_fixture.post('http://example.com:8080/jsonrpc', json=trans_data)


@pytest.fixture
def request_data_login_get_comet(requests_mock_fixture, comet_data):
    return requests_mock_fixture.post('http://example.com:8080/jsonrpc', json=comet_data)


@pytest.fixture
def request_data_login_get_trans_https(requests_mock_fixture, trans_data):
    return requests_mock_fixture.post('https://example.com:8080/jsonrpc', json=trans_data)


@pytest.fixture
def request_data_get_system(requests_mock_fixture, system_data):
    return requests_mock_fixture.post('http://example.com:8080/jsonrpc', json=system_data)


@pytest.fixture
def request_data_abort(requests_mock_fixture, abort_data):
    return requests_mock_fixture.post('http://example.com:8080/jsonrpc', json=abort_data)

import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from nso_jsonrpc_requester.common import NsoJsonRpcCommon


def test_common_trans(request_data_login_get_trans, monkeypatch, trans_data):
    def mock_new_trans(*args, **kwargs):
        return '15'

    monkeypatch.setattr(NsoJsonRpcCommon, 'new_trans', mock_new_trans)

    test_obj = NsoJsonRpcCommon('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.login()
    test_obj.new_trans()
    response = test_obj.get_trans()
    test_obj.logout()
    assert response == trans_data


def test_common_system(request_data_get_system, system_data):
    test_obj = NsoJsonRpcCommon('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.login()
    response = test_obj.get_system_setting('version')
    test_obj.logout()
    assert response == system_data


def test_abort(request_data_abort, abort_data):
    test_obj = NsoJsonRpcCommon('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.login()
    response = test_obj.abort(1)
    test_obj.logout()
    assert response == abort_data


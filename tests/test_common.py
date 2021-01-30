import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from nso_jsonrpc_requester.common import NsoJsonRpcCommon


def test_common_init_bad_data():
    test_obj = NsoJsonRpcCommon(protocol='http')
    with pytest.raises(TypeError):
        NsoJsonRpcCommon(protocol='ssh')

    with pytest.raises(TypeError):
        test_obj.login('test')

    with pytest.raises(TypeError):
        test_obj.new_trans(mode=False)

    with pytest.raises(ValueError):
        test_obj.new_trans(mode='test')

    with pytest.raises(ValueError):
        test_obj.new_trans(conf_mode='test')

    with pytest.raises(ValueError):
        test_obj.new_trans(on_pending_changes='test')

    with pytest.raises(TypeError):
        test_obj.new_trans(tag=1)

    with pytest.raises(ValueError):
        test_obj.get_system_setting(operation=1)

    with pytest.raises(TypeError):
        test_obj.abort(request_id='test')

    with pytest.raises(TypeError):
        test_obj.eval_xpath(xpath_expr=False)


def test_common_trans(request_data_login_get_trans, trans_data):
    test_obj = NsoJsonRpcCommon('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.login()
    test_obj.new_trans()
    test_obj.new_trans(tag='test')
    test_obj.eval_xpath('/services')
    response = test_obj.get_trans()
    test_obj.logout()
    assert response == trans_data


def test_common_trans_https(request_data_login_get_trans_https, trans_data):
    test_obj = NsoJsonRpcCommon('https', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.login()
    test_obj.new_trans()
    test_obj.new_trans(tag='test')
    test_obj.eval_xpath('/services')
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

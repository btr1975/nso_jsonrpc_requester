import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from nso_jsonrpc_requester import NsoJsonRpcComet


def test_comet_init_bad_data(request_data_login_get_comet):
    test_obj = NsoJsonRpcComet('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)

    with pytest.raises(TypeError):
        test_obj.subscribe_changes(path=1)

    with pytest.raises(TypeError):
        test_obj.subscribe_poll_leaf(path=1, interval=1)

    with pytest.raises(TypeError):
        test_obj.subscribe_poll_leaf(path='/services/path', interval='test')

    with pytest.raises(TypeError):
        test_obj.subscribe_cdboper(path=1)

    with pytest.raises(Exception):
        test_obj.start_comet()

    test_obj.stop_comet()

    with pytest.raises(Exception):
        test_obj.stop_comet()


def test_comet_init(request_data_login_get_comet):
    test_obj = NsoJsonRpcComet('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.subscribe_changes(path='/services/path')
    test_obj.subscribe_poll_leaf(path='/services/path', interval=30)
    test_obj.subscribe_cdboper(path='/services/path')
    test_obj.subscribe_upgrade()
    test_obj.subscribe_jsonrpc_batch()
    test_obj.get_subscriptions()
    test_obj.comet_poll()
    test_obj.stop_comet()

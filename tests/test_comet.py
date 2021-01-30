import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from nso_jsonrpc_requester import NsoJsonRpcComet


def test_comet_init(request_data_login_get_trans, trans_data):
    test_obj = NsoJsonRpcComet('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)

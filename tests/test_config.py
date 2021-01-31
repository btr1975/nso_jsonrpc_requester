import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
from nso_jsonrpc_requester import NsoJsonRpcConfig


def test_config_init_bad_data(request_data_login_get_trans):
    test_obj = NsoJsonRpcConfig('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.new_trans(mode='read_write')

    with pytest.raises(TypeError):
        test_obj.show_config(path=1, result_as='string', with_oper=False, max_size=0)

    with pytest.raises(KeyError):
        test_obj.show_config(path='/services/path', result_as='test', with_oper=False, max_size=0)

    with pytest.raises(TypeError):
        test_obj.show_config(path='/services/path', result_as='string', with_oper=1, max_size=0)

    with pytest.raises(TypeError):
        test_obj.show_config(path='/services/path', result_as='string', with_oper=False, max_size='test')

    with pytest.raises(TypeError):
        test_obj.deref(path=1, result_as='paths')

    with pytest.raises(KeyError):
        test_obj.deref(path='/services/path', result_as='test')

    with pytest.raises(TypeError):
        test_obj.get_leafref_values(path=1, skip_grouping=False, keys=None)

    with pytest.raises(TypeError):
        test_obj.get_leafref_values(path='/services/path', skip_grouping='test', keys=None)

    with pytest.raises(TypeError):
        test_obj.get_leafref_values(path='/services/path', skip_grouping=False, keys='test')

    with pytest.raises(TypeError):
        test_obj.run_action(path=1, input_data=None)

    with pytest.raises(TypeError):
        test_obj.run_action(path='/services/path', input_data='test')

    with pytest.raises(TypeError):
        test_obj.get_schema(path=1)

    with pytest.raises(TypeError):
        test_obj.get_list_keys(path=1)

    with pytest.raises(TypeError):
        test_obj.get_value(path=1, check_default=False)

    with pytest.raises(TypeError):
        test_obj.get_value(path='/services/path', check_default='test')

    with pytest.raises(TypeError):
        test_obj.get_values(path=1, leafs=['test'], check_default=False)

    with pytest.raises(TypeError):
        test_obj.get_values(path='/services/path', leafs='test', check_default=False)

    with pytest.raises(TypeError):
        test_obj.get_values(path='/services/path', leafs=['test'], check_default='test')

    with pytest.raises(TypeError):
        test_obj.create(path=1)

    with pytest.raises(TypeError):
        test_obj.exists(path=1)

    with pytest.raises(TypeError):
        test_obj.get_case(path=1, choice='test')

    with pytest.raises(TypeError):
        test_obj.get_case(path='/services/path', choice=1)

    with pytest.raises(TypeError):
        test_obj.load(data=5, path='/', data_format='xml', mode='merge')

    with pytest.raises(TypeError):
        test_obj.load(data='test', path=1, data_format='xml', mode='merge')

    with pytest.raises(KeyError):
        test_obj.load(data='test', path='/', data_format='test', mode='merge')

    with pytest.raises(KeyError):
        test_obj.load(data='test', path='/', data_format='xml', mode='test')

    with pytest.raises(TypeError):
        test_obj.set_value(path=1, value='test', dry_run=False)

    with pytest.raises(TypeError):
        test_obj.set_value(path='/services/path', value='test', dry_run='test')

    with pytest.raises(TypeError):
        test_obj.commit(dry_run='test', output='cli', reverse=False)

    with pytest.raises(KeyError):
        test_obj.commit(dry_run=False, output='test', reverse=False)

    with pytest.raises(TypeError):
        test_obj.commit(dry_run=False, output='cli', reverse='test')

    with pytest.raises(TypeError):
        test_obj.delete(path=1)

    with pytest.raises(TypeError):
        test_obj.get_template_variables(name=1)

    with pytest.raises(TypeError):
        test_obj.query(xpath_expr=1, result_as='string')

    with pytest.raises(ValueError):
        test_obj.query(xpath_expr='/services/path', result_as='test')

    with pytest.raises(ValueError):
        test_obj.start_query(xpath_expr=None, path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr=1, path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr=None, path=1, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=1, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size='test',
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset='test', sort=None, sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort='test', sort_order=None, include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(ValueError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order='test', include_total=True,
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total='test',
                             context_node=None, result_as='string')

    with pytest.raises(TypeError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=True,
                             context_node=1, result_as='string')

    with pytest.raises(ValueError):
        test_obj.start_query(xpath_expr='/services/path', path=None, selection=None, chunk_size=None,
                             initial_offset=None, sort=None, sort_order=None, include_total=False,
                             context_node=None, result_as='test')

    with pytest.raises(TypeError):
        test_obj.run_query(qh='test')

    with pytest.raises(TypeError):
        test_obj.reset_query(qh='test')

    with pytest.raises(TypeError):
        test_obj.stop_query(qh='test')

    test_obj.new_trans()

    with pytest.raises(ValueError):
        test_obj.create(path='/services/path')

    with pytest.raises(ValueError):
        test_obj.load(data='test')

    with pytest.raises(ValueError):
        test_obj.set_value(path='/services/path', value='test')

    with pytest.raises(ValueError):
        test_obj.validate_commit()

    with pytest.raises(ValueError):
        test_obj.commit()

    with pytest.raises(ValueError):
        test_obj.delete(path='/services/path')


def test_config_init(request_data_login_get_trans):
    test_obj = NsoJsonRpcConfig('http', 'example.com', '8080', 'admin', 'admin', ssl_verify=False)
    test_obj.new_trans(mode='read_write')
    test_obj.show_config(path='/services/path')
    test_obj.deref(path='/services/path')
    test_obj.get_leafref_values(path='/services/path')
    test_obj.get_leafref_values(path='/services/path', keys=['test'])
    test_obj.run_action(path='/services/path', input_data=None)
    test_obj.run_action(path='/services/path', input_data={'test': 'test'})
    test_obj.get_schema(path='/services/path')
    test_obj.get_list_keys(path='/services/path')
    test_obj.get_value(path='/services/path')
    test_obj.get_values(path='/services/path', leafs=['test'])
    test_obj.create(path='/services/path')
    test_obj.exists(path='/services/path')
    test_obj.get_case(path='/services/path', choice='test')
    test_obj.load(data='test')
    test_obj.set_value(path='/services/path', value='test')
    test_obj.validate_commit()
    test_obj.commit()
    test_obj.commit(output='native', reverse=True)
    test_obj.delete(path='/services/path')
    test_obj.get_service_points()
    test_obj.get_template_variables(name='test')
    test_obj.query(xpath_expr='/services/path')
    test_obj.start_query(xpath_expr='/services/path', selection=['test'], chunk_size=10, initial_offset=10,
                         sort=['test'], sort_order='descending', include_total=False,
                         context_node='/thing', result_as='string')
    test_obj.start_query(path='/services/path')
    test_obj.run_query(qh=5)
    test_obj.reset_query(qh=5)
    test_obj.stop_query(qh=5)

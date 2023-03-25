"""
Holds the config methods for the NSO-JSON RPC
"""
from nso_jsonrpc_requester.common import NsoJsonRpcCommon


class NsoJsonRpcConfig(NsoJsonRpcCommon):
    """
    This class is used for the NSO JsonRPC API for configuration

    :type protocol: String
    :param protocol: ('http', 'https') Default: http
    :type ip: String
    :param ip: IPv4 Address or hostname Default: 127.0.0.1
    :type port: String
    :param port: A protocol port Default: 8080
    :type username: String
    :param username: The username to use Default: admin
    :type password: String
    :param password: The password to use Default: admin
    :type ssl_verify: Boolean
    :param ssl_verify: Choice to verify SSL Cer Default: True

    :rtype: None
    :returns: NA init

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol: str = 'http', ip: str = '127.0.0.1', port: str = '8080',
                 username: str = 'admin', password: str = 'admin', ssl_verify: bool = True) -> None:
        super().__init__(protocol, ip, port, username, password, ssl_verify)

    def __str__(self):  # pragma: no cover
        return '<NsoJsonRpc>'

    def show_config(self, path, result_as='string', with_oper=False, max_size=0):
        """
        Method to send a show_config post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type result_as: String
        :param result_as: ('string', 'json') Defualt: string
        :type with_oper: Boolean
        :param with_oper: Default: False
        :type max_size: Integer
        :param max_size: Default: 0, 0 = disable limit

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises KeyError: if result_as is not ('string', 'json')
        :raises TypeError: if with_oper is not boolean
        :raises TypeError: if max_size is not integer

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if result_as not in {'string', 'json'}:
            raise KeyError('param result_as must be one of these {"string", "json"}')

        if not isinstance(with_oper, bool):
            raise TypeError(f'param with_oper must be of type boolean but received {type(with_oper)}')

        if not isinstance(max_size, int):
            raise TypeError(f'param max_size must be of type integer but received {type(max_size)}')

        show_config_json = {'jsonrpc': '2.0',
                            'id': self.request_id,
                            'method': 'show_config',
                            'params': {
                                'th': self.transaction_handle,
                                'path': path,
                                'result_as': result_as,
                                'with_oper': with_oper,
                                'max_size': max_size
                            }}

        response = self.post_with_cookies(show_config_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def deref(self, path, result_as='paths'):
        """
        Method to send a deref post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type result_as: String
        :param result_as: ('paths', 'target', 'list-target') Default: paths

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises KeyError: if result_as is not ('paths', 'target', 'list-target')

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if result_as not in {'paths', 'target', 'list-target'}:
            raise KeyError('param result_as must be one of these {"paths", "target", "list-target"}')

        show_config_json = {'jsonrpc': '2.0',
                            'id': self.request_id,
                            'method': 'deref',
                            'params': {
                                'th': self.transaction_handle,
                                'path': path,
                                'result_as': result_as
                            }}

        response = self.post_with_cookies(show_config_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_leafref_values(self, path, skip_grouping=False, keys=None):
        """
        Method to send a get_leafref_values post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type skip_grouping: Boolean
        :param skip_grouping: Default: False
        :type keys: List
        :param keys: A list of keys

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if skip_grouping is not boolean
        :raises TypeError: if keys is not a list

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(skip_grouping, bool):
            raise TypeError(f'param skip_grouping must be of type boolean but received {type(skip_grouping)}')

        if keys:
            if not isinstance(keys, list):
                raise TypeError(f'param keys must be of type list but received {type(keys)}')

            show_config_json = {'jsonrpc': '2.0',
                                'id': self.request_id,
                                'method': 'get_leafref_values',
                                'params': {
                                    'th': self.transaction_handle,
                                    'path': path,
                                    'skip_grouping': skip_grouping,
                                    'keys': keys
                                }}

        else:
            show_config_json = {'jsonrpc': '2.0',
                                'id': self.request_id,
                                'method': 'get_leafref_values',
                                'params': {
                                    'th': self.transaction_handle,
                                    'path': path,
                                    'skip_grouping': skip_grouping
                                }}

        response = self.post_with_cookies(show_config_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def run_action(self, path, input_data=None):
        """
        Method to send a run_action post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type input_data: Dict
        :param input_data: A Dictionary of inputs

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if input_data is not a dict

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if input_data:
            if not isinstance(input_data, dict):
                raise TypeError(f'param input must be of type dict but received {type(input_data)}')

        if input_data:
            run_action_json = {'jsonrpc': '2.0',
                               'id': self.request_id,
                               'method': 'run_action',
                               'params': {
                                   'th': self.transaction_handle,
                                   'path': path,
                                   'params': input_data
                               }}

        else:
            run_action_json = {'jsonrpc': '2.0',
                               'id': self.request_id,
                               'method': 'run_action',
                               'params': {
                                   'th': self.transaction_handle,
                                   'path': path
                               }}

        response = self.post_with_cookies(run_action_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_schema(self, path):
        """
        Method to send a get_schema post

        :type path: String
        :param path: The NSO KEYPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        get_schema_json = {'jsonrpc': '2.0',
                           'id': self.request_id,
                           'method': 'get_schema',
                           'params': {
                               'th': self.transaction_handle,
                               'path': path
                           }}

        response = self.post_with_cookies(get_schema_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_list_keys(self, path):
        """
        Method to send a get_list_keys post

        :type path: String
        :param path: The NSO KEYPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        get_list_keys_json = {'jsonrpc': '2.0',
                              'id': self.request_id,
                              'method': 'get_list_keys',
                              'params': {
                                  'th': self.transaction_handle,
                                  'path': path
                              }}

        response = self.post_with_cookies(get_list_keys_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_value(self, path, check_default=False):
        """
        Method to send a get_value post retrieves a single value

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type check_default: Boolean
        :param check_default: Default: False

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if check_default is not boolean

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(check_default, bool):
            raise TypeError(f'param check_default must be of type boolean but received {type(check_default)}')

        get_value_json = {'jsonrpc': '2.0',
                          'id': self.request_id,
                          'method': 'get_value',
                          'params': {
                              'th': self.transaction_handle,
                              'path': path,
                              'check_default': check_default
                          }}

        response = self.post_with_cookies(get_value_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_values(self, path, leafs, check_default=False):
        """
        Method to send a get_values post retrieves multiple leafs at once

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type leafs: List
        :param leafs: A list of leafs you want the data for, of type string
        :type check_default: Boolean
        :param check_default: Default: False

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if leafs is not a list
        :raises TypeError: if check_default is not boolean

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(leafs, list):
            raise TypeError(f'param leafs must be of type list but received {type(leafs)}')

        if not isinstance(check_default, bool):
            raise TypeError(f'param check_default must be of type boolean but received {type(check_default)}')

        get_values_json = {'jsonrpc': '2.0',
                           'id': self.request_id,
                           'method': 'get_values',
                           'params': {
                               'th': self.transaction_handle,
                               'path': path,
                               'check_default': check_default,
                               'leafs': leafs
                           }}

        response = self.post_with_cookies(get_values_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def create(self, path):
        """
        Method to send a create post

        :type path: String
        :param path: The NSO KEYPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises ValueError: if transaction_mode is not read_write

        """
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_create_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        create_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'create',
                       'params': {
                           'th': self.transaction_handle,
                           'path': path
                       }}

        response = self.post_with_cookies(create_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def exists(self, path):
        """
        Method to send a exists post

        :type path: String
        :param path: The NSO KEYPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        exists_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'exists',
                       'params': {
                           'th': self.transaction_handle,
                           'path': path
                       }}

        response = self.post_with_cookies(exists_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_case(self, path, choice):
        """
        Method to send a get_case post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type choice: String
        :param choice: A choice from a case

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if choice is not a string

        """
        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(choice, str):
            raise TypeError(f'param choice must be of type string but received {type(choice)}')

        get_case_json = {'jsonrpc': '2.0',
                         'id': self.request_id,
                         'method': 'get_case',
                         'params': {
                             'th': self.transaction_handle,
                             'path': path,
                             'choice': choice
                         }}

        response = self.post_with_cookies(get_case_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def load(self, data, path='/', data_format='xml', mode='merge'):
        """
        Method to send a load post

        :type data: String
        :param data: The data to be loaded in the transaction
        :type path: String
        :param path: The NSO KEYPATH to the data Default: /
        :type data_format: String
        :param data_format: ('json', 'xml') Default: xml
        :type mode: String
        :param mode: ('create', 'merge', 'replace') Default: merge

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if data is not a string
        :raises TypeError: if path is not a string
        :raises KeyError: if data_format is not ('json', 'xml')
        :raises KeyError: if mode is not ('create', 'merge', 'replace')
        :raises ValueError: if transaction_mode is not read_write

        """
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_create_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        if not isinstance(data, str):
            raise TypeError(f'param data must be of type string but received {type(data)}')

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if data_format not in {'json', 'xml'}:
            raise KeyError('param format must be one of these {"json", "xml"}')

        if mode not in {'create', 'merge', 'replace'}:
            raise KeyError('param mode must be one of these {"create", "merge", "replace"}')

        load_json = {'jsonrpc': '2.0',
                         'id': self.request_id,
                         'method': 'load',
                         'params': {
                             'th': self.transaction_handle,
                             'data': data,
                             'path': path,
                             'format': data_format,
                             'mode': mode
                         }}

        response = self.post_with_cookies(load_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def set_value(self, path, value, dry_run=False):
        """
        Method to send a set_value post

        :type path: String
        :param path: The NSO KEYPATH to the data
        :type value: User specified
        :param value: The value to set the item to
        :type dry_run: Boolean
        :param dry_run: Default: False, when set True tests if value is valid or not

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if dry_run is not boolean
        :raises ValueError: if transaction_mode is not read_write

        """
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_set_value_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(dry_run, bool):
            raise TypeError(f'param dry_run must be of type boolean but received {type(dry_run)}')

        set_value_json = {'jsonrpc': '2.0',
                          'id': self.request_id,
                          'method': 'set_value',
                          'params': {
                              'th': self.transaction_handle,
                              'path': path,
                              'value': value,
                              'dryrun': dry_run
                          }}

        response = self.post_with_cookies(set_value_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def validate_commit(self):
        """
        Method to send a validate_commit post, in the CLI commits are validated automatically, in JsonRPC
        they are not, but only validated commits can be committed

        :rtype: Dict
        :return: A dictionary of data

        :raises ValueError: if transaction_mode is not read_write

        """
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_set_value_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        validate_commit_json = {'jsonrpc': '2.0',
                                'id': self.request_id,
                                'method': 'validate_commit',
                                'params': {
                                    'th': self.transaction_handle,
                                }}

        response = self.post_with_cookies(validate_commit_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def commit(self, dry_run=True, output='cli', reverse=False):
        """
        Method to send a commit post, in the CLI commits are validated automatically, in JsonRPC
        they are not, but only validated commits can be commited

        :type dry_run: Boolean
        :param dry_run: To output a dry run, Default: is True
        :type output: String
        :param output: ('cli', 'native', 'xml') Default: cli
        :type reverse: Boolean
        :param reverse: Output the revers of the config going in, default is False, only valid when
                        output equals native

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if dry_run is not boolean
        :raises KeyError: if output is not ('cli', 'native', 'xml')
        :raises TypeError: if reverse is not boolean
        :raises ValueError: if transaction_mode is not read_write

        """
        flags = []
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_set_value_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        if output not in {'cli', 'native', 'xml'}:
            raise KeyError(f'output should be one of these cli, native, xml you entered {output}')

        if not isinstance(dry_run, bool):
            raise TypeError(f'param dry_run must be of type boolean but received {type(dry_run)}')

        if not isinstance(reverse, bool):
            raise TypeError(f'param reverse must be of type boolean but received {type(reverse)}')

        if dry_run:
            flags.append(f'dry-run={output}')
            if output == 'native' and reverse:
                flags.append('dry-run-reverse')

        commit_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'commit',
                       'params': {
                           'th': self.transaction_handle,
                           'flags': flags
                       }}

        response = self.post_with_cookies(commit_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def delete(self, path):
        """
        Method to send a delete post

        :type path: String
        :param path: The NSO KEYPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises ValueError: if transaction_mode is not read_write

        """
        if self.transaction_mode != 'read_write':
            raise ValueError(f'To use send_create_post the transaction mode must be read_'
                             f'write the current transaction mode is {self.transaction_mode}')

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        delete_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'delete',
                       'params': {
                           'th': self.transaction_handle,
                           'path': path
                       }}

        response = self.post_with_cookies(delete_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_service_points(self):
        """
        Method to send a get_service_points post

        :rtype: Dict
        :return: A dictionary of data

        """
        get_service_points_json = {'jsonrpc': '2.0',
                                   'id': self.request_id,
                                   'method': 'get_service_points',
                                   }

        response = self.post_with_cookies(get_service_points_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_template_variables(self, name):
        """
        Method to send a get_template_variables post, this retrieves device templates only

        :type name: String
        :param name: The name of the template

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if name is not a string

        """
        if not isinstance(name, str):
            raise TypeError(f'param name must be of type string but received {type(name)}')

        get_template_variables_json = {'jsonrpc': '2.0',
                                       'id': self.request_id,
                                       'method': 'get_template_variables',
                                       'params': {
                                           'th': self.transaction_handle,
                                           'name': name
                                       }}

        response = self.post_with_cookies(get_template_variables_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def query(self, xpath_expr, result_as='string'):
        """
        Method for a basic Query in NSO, This is a convenience method for calling
        start_query, run_query and stop_query This method should not be used for paginated
        results, as it results in performance degradation - use start_query, multiple
        run_query and stop_query instead.

        :type xpath_expr: String
        :param xpath_expr: The XPATH expression to query
        :type result_as: String
        :param result_as: One of these options {'string', 'keypath-value', 'leaf_value_as_string'},  Default string

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if xpath_expr is not a string
        :raises ValueError: if result_as is not one of the following {'string', 'keypath-value', 'leaf_value_as_string'}

        """
        if not isinstance(xpath_expr, str):
            raise TypeError(f'param xpath_expr must be of type string but received {type(xpath_expr)}')

        if result_as not in {'string', 'keypath-value', 'leaf_value_as_string'}:
            raise ValueError("param result_as must be one of the following {'string', 'keypath-value', "
                             "'leaf_value_as_string'} of type string but received")

        query_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'query',
                      'params': {
                          'th': self.transaction_handle,
                          'xpath_expr': xpath_expr,
                          'result_as': result_as
                      }}

        response = self.post_with_cookies(query_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def start_query(self, xpath_expr=None, path=None, selection=None, chunk_size=None, initial_offset=None,
                    sort=None, sort_order=None, include_total=True, context_node=None, result_as='string'):
        """
        Method to start a complex query

        :type xpath_expr: String
        :param xpath_expr: The XPATH expression to query is chosen above path if both are given
        :type path: String
        :param path: The KEYPATH expression to query
        :type selection: List
        :param selection: The fields to select, Optional
        :type chunk_size: Integer
        :param chunk_size: Must be greater than 0, Optional
        :type initial_offset: Integer
        :param initial_offset: Not sure on this yet, Optional
        :type sort: List
        :param sort: A list of XPATH expressions, Optional
        :type sort_order: String
        :param sort_order: One of the following {"ascending", "descending"}, Optional
        :type include_total: Boolean
        :param include_total: Include the total of records, Default: True
        :type context_node: String
        :param context_node: A KEYPATH, Optional
        :type result_as: String
        :param result_as: One of these options {'string', 'keypath-value', 'leaf_value_as_string'},  Default string

        :rtype: Dict
        :return: A dictionary of data with one key 'qh' which is the Query Handle to be used with run_query etc.

        :raises ValueError: if both xpath_expr, and path are not given
        :raises TypeError: if xpath_expr is not a string
        :raises TypeError: if path is not a string
        :raises TypeError: if selection is not a list
        :raises TypeError: if chunk_size is not a integer greater than 0
        :raises TypeError: if initial_offset is not a integer
        :raises TypeError: if sort is not a list
        :raises ValueError: if sort_order, is not one of the following {"ascending", "descending"}
        :raises TypeError: if include_total is not a boolean
        :raises TypeError: if context_node is not a string
        :raises ValueError: if result_as is not one of the following {'string', 'keypath-value', 'leaf_value_as_string'}

        """
        query_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'start_query',
                      'params': {
                          'th': self.transaction_handle,
                      }}

        if not xpath_expr and not path:
            raise ValueError('either xpath_expr needs to be given or path!')

        else:
            if xpath_expr:
                if not isinstance(xpath_expr, str):
                    raise TypeError(f'param xpath_expr must be of type string but received {type(xpath_expr)}')

                else:
                    query_json['params'].update({'xpath_expr': xpath_expr})

            elif path:
                if not isinstance(path, str):
                    raise TypeError(f'param path must be of type string but received {type(path)}')

                else:
                    query_json['params'].update({'path': path})

        if selection:
            if not isinstance(selection, list):
                raise TypeError(f'param selection must be of type list but received {type(selection)}')

            else:
                query_json['params'].update({'selection': selection})

        if chunk_size:
            if not isinstance(chunk_size, int) and chunk_size < 1:
                raise TypeError(f'param chunk_size must be of int list but received {type(chunk_size)} '
                                f'or it is less than 1')

            else:
                query_json['params'].update({'chunk_size': chunk_size})

        if initial_offset:
            if not isinstance(initial_offset, int):
                raise TypeError(f'param initial_offset must be of type int but '
                                f'received {type(initial_offset)}')

            else:
                query_json['params'].update({'initial_offset': initial_offset})

        if sort:
            if not isinstance(sort, list):
                raise TypeError(f'param sort must be of type list but received {type(sort)}')

            else:
                query_json['params'].update({'sort': sort})

        if sort_order:
            if sort_order not in {"ascending", "descending"}:
                raise ValueError('param sort_order must be one of the following {"ascending", "descending"}')

            else:
                query_json['params'].update({'sort_order': sort_order})

        if not isinstance(include_total, bool):
            raise TypeError(f'param include_total must be of type bool but received {type(include_total)}')

        else:
            query_json['params'].update({'include_total': include_total})

        if context_node:
            if not isinstance(context_node, str):
                raise TypeError(f'param context_node must be of type string but received {type(context_node)}')

            else:
                query_json['params'].update({'context_node': context_node})

        if result_as not in {'string', 'keypath-value', 'leaf_value_as_string'}:
            raise ValueError("param result_as must be one of the following {'string', 'keypath-value', "
                             "'leaf_value_as_string'} of type string but received")

        else:
            query_json['params'].update({'result_as': result_as})

        response = self.post_with_cookies(query_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def run_query(self, qh):  # pylint: disable=invalid-name
        """
        Method to run the query

        :type qh: Integer
        :param qh: The query handle to run

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if qh is not a integer

        """
        if not isinstance(qh, int):
            raise TypeError(f'param qh must be of type int but received {type(qh)}')

        query_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'run_query',
                      'params': {
                          'qh': qh,
                      }}

        response = self.post_with_cookies(query_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def reset_query(self, qh):  # pylint: disable=invalid-name
        """
        Method to reset the query

        :type qh: Integer
        :param qh: The query handle to run

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if qh is not a integer

        """
        if not isinstance(qh, int):
            raise TypeError(f'param qh must be of type int but received {type(qh)}')

        query_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'reset_query',
                      'params': {
                          'qh': qh,
                      }}

        response = self.post_with_cookies(query_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def stop_query(self, qh):  # pylint: disable=invalid-name
        """
        Method to stop the query

        :type qh: Integer
        :param qh: The query handle to run

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if qh is not a integer

        """
        if not isinstance(qh, int):
            raise TypeError(f'param qh must be of type int but received {type(qh)}')

        query_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'stop_query',
                      'params': {
                          'qh': qh,
                      }}

        response = self.post_with_cookies(query_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()


if __name__ == '__main__':  # pragma: no cover
    help(NsoJsonRpcConfig)

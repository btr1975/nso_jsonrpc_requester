import json
import logging
import random
import requests
from urllib3.exceptions import InsecureRequestWarning
import yaml
# Reference https://community.cisco.com/t5/nso-developer-hub-documents/json-rpc-basics/ta-p/3635204
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2020, Benjamin P. Trachtenberg"
__credits__ = None
__license__ = 'The MIT License (MIT)'
__status__ = 'prod'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger('nso_jsonrpc')


class NsoJsonRpcCommon(object):
    """
    This class is used as a parent for other NSO JsonRPC API classes for common needs

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
    :returns: None

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol='http', ip='127.0.0.1', port='8080', username='admin', password='admin',
                 ssl_verify=True):
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.protocol = protocol
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        # self.cookies starts as set to None, but is set when the login Method is called, from there on out
        # all other calls use the cookies as authentication
        self.cookies = None
        # self.request_id this is a id that is used to make it easy to pair requests and responses, it is
        # not used by NSO itself
        self.request_id = random.randint(1, 100000)
        # self.comet_id is a unique id (decided by the client) which must be given first in a call to the comet
        # method, and then to upcoming calls which trigger comet notifications.
        self.comet_id = 'remote-comet-{}'.format(random.randint(1, 100000))
        self.comet_handles = list()
        # self.transaction_handle starts as set to None, but is set when the new_trans method is called, it is
        # assigned by NSO
        self.transaction_handle = None
        # self.transaction_mode starts as set to None, but is set when the new_trans method is called,
        # it is just a string that is set to "read", or "read_write", and is used to verify if a json call
        # that requires "read_write" should be able to run
        self.transaction_mode = None

        self.headers = {'Content-Type': 'application/json',
                        'Accept': "application/json,"}

        if protocol not in ('http', 'https'):
            raise TypeError('Protocol should be http, or https!')

        self.server_url = '{protocol}://{ip}:{port}/jsonrpc'.format(protocol=protocol, ip=ip, port=port)

    def login(self, ack_warning=False):
        """
        Method to send a login request, if the user is able to log in, the users cookie is set
        :param ack_warning: Boolean default False
        :return:
            Dictionary

            set variable:
                self.cookies with a Cookies object

        """
        if not isinstance(ack_warning, bool):
            raise TypeError('param ack_warning must be of type boolean but received {}'.format(type(ack_warning)))

        login_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'login',
                      'params': {
                          'user': self.username,
                          'passwd': self.password
                      }}

        if self.protocol == 'http':
            response = requests.post(self.server_url, headers=self.headers, json=login_json)

        else:
            response = requests.post(self.server_url, headers=self.headers, json=login_json, verify=self.ssl_verify)

        if response.ok:
            self.cookies = response.cookies
            return response.json()

        else:
            response.raise_for_status()

    def logout(self):
        """
        Method to send a logout request
        :return:
            Dictionary

        """
        logout_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'logout',
                       }

        response = self.post_with_cookies(logout_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def new_trans(self, mode='read', conf_mode='private', tag=None, on_pending_changes='reuse'):
        """
        Method to request a new transaction
        :param mode: {'read', 'read_write'} default is read
        :param conf_mode: {'private', 'shared', 'exclusive'} default is private
        :param tag: String default None
        :param on_pending_changes: {'reuse', 'reject', 'discard'} default is reuse
        :return:
            Dictionary

            set variables:
                self.transaction_handle with a transaction handle
                self.transaction_mode with either {'read', 'read_write'}

        """
        if not isinstance(mode, str):
            raise TypeError('param mode must be of type string but received {}'.format(type(mode)))

        if mode not in {'read', 'read_write'}:
            raise ValueError('param mode valid options are {"read", "read_write"}')

        if conf_mode not in {'private', 'shared', 'exclusive'}:
            raise ValueError('param conf_mode valid options are {"private", "shared", "exclusive"}')

        if on_pending_changes not in {'reuse', 'reject', 'discard'}:
            raise ValueError('param on_pending_changes valid options are {"reuse", "reject", "discard"}')

        if tag:
            if not isinstance(tag, str):
                raise TypeError('param tag must be of type string but received {}'.format(type(tag)))

            new_trans_json = {'jsonrpc': '2.0',
                              'id': self.request_id,
                              'method': 'new_trans',
                              'params': {
                                  'db': 'running',
                                  'mode': mode,
                                  'conf_mode': conf_mode,
                                  'tag': tag,
                                  'on_pending_changes': on_pending_changes
                              }}

        else:
            new_trans_json = {'jsonrpc': '2.0',
                              'id': self.request_id,
                              'method': 'new_trans',
                              'params': {
                                  'db': 'running',
                                  'mode': mode,
                                  'conf_mode': conf_mode,
                                  'on_pending_changes': on_pending_changes
                              }}

        response = self.post_with_cookies(new_trans_json)

        if response.ok:
            self.transaction_handle = response.json()['result']['th']
            self.transaction_mode = mode
            return response.json()

        else:
            response.raise_for_status()

    def get_trans(self):
        """
        Method to get the all current transaction information
        :return:
            Dictionary

        """
        get_trans_json = {'jsonrpc': '2.0',
                          'id': self.request_id,
                          'method': 'get_trans'
                          }

        response = self.post_with_cookies(get_trans_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def get_system_setting(self, operation='version'):
        """
        Method to get get_system_setting information
        :param operation: {'capabilities', 'customizations' ,'models', 'user', 'version', 'all'} default version
        :return:
            Dictionary

        """
        if operation not in {'capabilities', 'customizations', 'models', 'user', 'version', 'all'}:
            raise ValueError('param operation must be one of these {"capabilities", "customizations", "models", '
                             '"user", "version", "all"}')

        get_system_setting_json = {'jsonrpc': '2.0',
                                   'id': self.request_id,
                                   'method': 'get_system_setting',
                                   'params': {
                                       'operation': operation
                                   }}

        response = self.post_with_cookies(get_system_setting_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def abort(self, request_id):
        """
        Method to send abort post
        :param request_id: Request ID to abort
        :return:
            Dictionary

        """
        if not isinstance(request_id, int):
            raise TypeError('param request_id must be of type integer but received {}'.format(type(request_id)))

        abort_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'abort',
                      'params': {
                          'id': request_id
                      }}

        response = self.post_with_cookies(abort_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def eval_xpath(self, xpath_expr):
        """
        Method to send eval_xpath post
        :param xpath_expr: The xpath to evaluate
        :return:
            Dictionary

        """
        if not isinstance(xpath_expr, str):
            raise TypeError('param xpath_expr must be of type string but received {}'.format(type(xpath_expr)))

        eval_xpath_json = {'jsonrpc': '2.0',
                           'id': self.request_id,
                           'method': 'eval_xpath',
                           'params': {
                               'th': self.transaction_handle,
                               'xpath_expr': xpath_expr
                           }}

        response = self.post_with_cookies(eval_xpath_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def post_with_cookies(self, json_data):
        """
        Method to request a post with yummy cookies
        :param json_data: Json Data
        :return:
            A requests response

        """
        if self.protocol == 'http':
            return requests.post(self.server_url, headers=self.headers, json=json_data, cookies=self.cookies)

        else:
            return requests.post(self.server_url, headers=self.headers, json=json_data, cookies=self.cookies,
                                 verify=self.ssl_verify)

    @staticmethod
    def print_pretty_json(json_data):
        """
        Method to print response JSON real pretty like
        :param json_data: JSON Data
        :return:
            None

        """
        print(json.dumps(json_data, sort_keys=True, indent=4))
        LOGGER.debug(json.dumps(json_data, sort_keys=True, indent=4))

    @staticmethod
    def print_pretty_yaml(json_data):
        """
        Method to print response JSON as YAML
        :param json_data: JSON Data
        :return:
            None

        """
        print(yaml.dump(json_data, default_flow_style=False, indent=4))
        LOGGER.debug(yaml.dump(json_data, default_flow_style=False, indent=4))

    @staticmethod
    def print_pretty_no_yaml_no_json(data):
        """
        Method to print Non-JSON, Non-YAML real pretty
        :param data: The Data
        :return:
            None

        """
        for line in data.content.splitlines():
            print(line.decode("utf-8"))

        for line in data.content.splitlines():
            LOGGER.debug(line.decode("utf-8"))


class NsoJsonRpcComet(NsoJsonRpcCommon):
    """
    This class is used for the NSO JsonRPC API for remote logging

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
    :returns: None

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol='http', ip='127.0.0.1', port='8080', username='admin', password='admin',
                 ssl_verify=True):
        super().__init__(protocol, ip, port, username, password, ssl_verify)
        self.comet_started = False
        self.start_comet()

    def __str__(self):
        return '<NsoJsonRpcComet>'

    def start_comet(self):
        """
        Method to start the comet process
        :return:
            None

        """
        self.__check_comet_state(False)
        self.comet_started = True
        self.login()
        self.new_trans()
        self.__comet()

    def stop_comet(self):
        """
        Method to stop the comet process
        :return:
            None

        """
        self.__check_comet_state(True)
        self.__unsubscribe()
        self.__comet()
        self.logout()
        self.comet_started = False

    def comet_poll(self):
        """
        Method to return comet result only
        :return:
            result

        """
        self.__check_comet_state(True)

        try:
            return self.__comet()['result']

        except Exception as e:
            self.stop_comet()

    def subscribe_changes(self, path):
        """
        Method to send a subscribe_changes post
        :param path: NSO path to data to watch for changes
        :return:
            Dictionary

            append variable:
                self.comet_handles to the handle given by NSO

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        subscribe_changes_json = {'jsonrpc': '2.0',
                                  'id': self.request_id,
                                  'method': 'subscribe_changes',
                                  'params': {
                                      'comet_id': self.comet_id,
                                      'path': path
                                  }}

        response = self.post_with_cookies(subscribe_changes_json)

        if response.ok:
            self.comet_handles.append(response.json()['result']['handle'])
            if self.__start_subscription(response.json()['result']['handle']).ok:
                return response.json()

        else:
            response.raise_for_status()

    def subscribe_poll_leaf(self, path, interval):
        """
        Method to send a subscribe_poll_leaf post
        :param path: NSO path to data to watch for changes
        :param interval: Interval
        :return:
            Dictionary

            append variable:
                self.comet_handles to the handle given by NSO

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(interval, int):
            raise TypeError('param interval must be of type integer but received {}'.format(type(interval)))

        subscribe_poll_leaf_json = {'jsonrpc': '2.0',
                                    'id': self.request_id,
                                    'method': 'subscribe_poll_leaf',
                                    'params': {
                                        'comet_id': self.comet_id,
                                        'path': path,
                                        'interval': interval
                                    }}

        response = self.post_with_cookies(subscribe_poll_leaf_json)

        if response.ok:
            self.comet_handles.append(response.json()['result']['handle'])
            if self.__start_subscription(response.json()['result']['handle']).ok:
                return response.json()

        else:
            response.raise_for_status()

    def subscribe_cdboper(self, path):
        """
        Method to send a subscribe_cdboper post
        :param path: NSO path to data to watch for changes
        :return:
            Dictionary

            append variable:
                self.comet_handles to the handle given by NSO

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        subscribe_cdboper_json = {'jsonrpc': '2.0',
                                  'id': self.request_id,
                                  'method': 'subscribe_cdboper',
                                  'params': {
                                      'comet_id': self.comet_id,
                                      'path': path
                                  }}

        response = self.post_with_cookies(subscribe_cdboper_json)

        if response.ok:
            self.comet_handles.append(response.json()['result']['handle'])
            if self.__start_subscription(response.json()['result']['handle']).ok:
                return response.json()

        else:
            response.raise_for_status()

    def subscribe_upgrade(self):
        """
        Method to send a subscribe_upgrade post
        :return:
            Dictionary

            append variable:
                self.comet_handles to the handle given by NSO

        """
        self.__check_comet_state(True)

        subscribe_upgrade_json = {'jsonrpc': '2.0',
                                  'id': self.request_id,
                                  'method': 'subscribe_upgrade',
                                  'params': {
                                      'comet_id': self.comet_id,
                                  }}

        response = self.post_with_cookies(subscribe_upgrade_json)

        if response.ok:
            self.comet_handles.append(response.json()['result']['handle'])
            if self.__start_subscription(response.json()['result']['handle']).ok:
                return response.json()

        else:
            response.raise_for_status()

    def subscribe_jsonrpc_batch(self):
        """
        Method to send a subscribe_jsonrpc_batch post
        :return:
            Dictionary

            append variable:
                self.comet_handles to the handle given by NSO

        """
        self.__check_comet_state(True)

        subscribe_jsonrpc_batch_json = {'jsonrpc': '2.0',
                                        'id': self.request_id,
                                        'method': 'subscribe_jsonrpc_batch',
                                        'params': {
                                            'comet_id': self.comet_id,
                                        }}

        response = self.post_with_cookies(subscribe_jsonrpc_batch_json)

        if response.ok:
            self.comet_handles.append(response.json()['result']['handle'])
            if self.__start_subscription(response.json()['result']['handle']).ok:
                return response.json()

        else:
            response.raise_for_status()

    def get_subscriptions(self):
        """
        Method to send a get_subscriptions post
        This get's the sessions subscriptions
        :return:
            Dictionary

        """
        self.__check_comet_state(True)

        get_subscriptions_json = {'jsonrpc': '2.0',
                                  'id': self.request_id,
                                  'method': 'get_subscriptions',
                                  }

        response = self.post_with_cookies(get_subscriptions_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def __comet(self):
        """
        Method to send a comet post
        comet is a log receiver, and can receive logs from the following methods
            start_cmd, subscribe_cdboper, subscribe_changes, subscribe_messages,
            subscribe_poll_leaf or subscribe_upgrade

        :return:
            Dictionary

        """
        comet_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'comet',
                      'params': {
                          'comet_id': self.comet_id,
                      }}

        response = self.post_with_cookies(comet_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def __start_subscription(self, handle):
        """
        Method to send a start_subscription post
        :param handle: NSO path to data to watch for changes
        :return:
            Dictionary

        """
        self.__check_comet_state(True)

        start_subscription_json = {'jsonrpc': '2.0',
                                   'id': self.request_id,
                                   'method': 'start_subscription',
                                   'params': {
                                       'handle': handle,
                                   }}

        response = self.post_with_cookies(start_subscription_json)

        if response.ok:
            return response

        else:
            response.raise_for_status()

    def __unsubscribe(self):
        """
        Method to send a unsubscribe post
        :return:
            Dictionary

        """
        self.__check_comet_state(True)

        for handle in self.comet_handles:
            unsubscribe_json = {'jsonrpc': '2.0',
                                'id': self.request_id,
                                'method': 'unsubscribe',
                                'params': {
                                    'handle': handle,
                                }}

            response = self.post_with_cookies(unsubscribe_json)

            if response.ok:
                pass

            else:
                response.raise_for_status()

    def __check_comet_state(self, wanted_state):
        """
        Method to verify comet state
        :param wanted_state: The state expected
        :return:
            None

        """
        if self.comet_started != wanted_state:
            if self.comet_started:
                raise Exception('Comet is already running!!')

            if not self.comet_started:
                raise Exception('Comet is not running!!')


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
    :returns: None

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol='http', ip='127.0.0.1', port='8080', username='admin', password='admin',
                 ssl_verify=True):
        super().__init__(protocol, ip, port, username, password, ssl_verify)

    def __str__(self):
        return '<NsoJsonRpc>'

    def show_config(self, path, result_as='string', with_oper=False, max_size=0):
        """
        Method to send a show_config post

        :type path: String
        :param path: The NSO XPATH to the data
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
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if result_as not in {'string', 'json'}:
            raise KeyError('param result_as must be one of these {"string", "json"}')

        if not isinstance(with_oper, bool):
            raise TypeError('param with_oper must be of type boolean but received {}'.format(type(with_oper)))

        if not isinstance(max_size, int):
            raise TypeError('param max_size must be of type integer but received {}'.format(type(max_size)))

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

        else:
            response.raise_for_status()

    def deref(self, path, result_as='paths'):
        """
        Method to send a deref post

        :type path: String
        :param path: The NSO XPATH to the data
        :type result_as: String
        :param result_as: ('paths', 'target', 'list-target') Default: paths

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises KeyError: if result_as is not ('paths', 'target', 'list-target')

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def get_leafref_values(self, path, skip_grouping=False, keys=None):
        """
        Method to send a get_leafref_values post

        :type path: String
        :param path: The NSO XPATH to the data
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
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(skip_grouping, bool):
            raise TypeError('param skip_grouping must be of type boolean but received {}'.format(type(skip_grouping)))

        if keys:
            if not isinstance(keys, list):
                raise TypeError('param keys must be of type list but received {}'.format(type(keys)))

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

        else:
            response.raise_for_status()

    def run_action(self, path, input_data=None):
        """
        Method to send a run_action post

        :type path: String
        :param path: The NSO XPATH to the data
        :type input_data: Dict
        :param input_data: A Dictionary of inputs

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if input_data is not a dict

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if input_data:
            if not isinstance(input_data, dict):
                raise TypeError('param input must be of type dict but received {}'.format(type(input_data)))

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

        else:
            response.raise_for_status()

    def get_schema(self, path):
        """
        Method to send a get_schema post

        :type path: String
        :param path: The NSO XPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def get_list_keys(self, path):
        """
        Method to send a get_list_keys post

        :type path: String
        :param path: The NSO XPATH to the data

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def get_value(self, path, check_default=False):
        """
        Method to send a get_value post retrieves a single value

        :type path: String
        :param path: The NSO XPATH to the data
        :type check_default: Boolean
        :param check_default: Default: False

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if path is not a string
        :raises TypeError: if check_default is not boolean

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(check_default, bool):
            raise TypeError('param check_default must be of type boolean but received {}'.format(type(check_default)))

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

        else:
            response.raise_for_status()

    def get_values(self, path, leafs, check_default=False):
        """
        Method to send a get_values post retrieves multiple leafs at once
        :param path: The NSO path to the data
        :param leafs: A list of leafs you want the data for, of type string
        :param check_default: Boolean default False
        :return:
            Dictionary

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(leafs, list):
            raise TypeError('param leafs must be of type list but received {}'.format(type(leafs)))

        if not isinstance(check_default, bool):
            raise TypeError('param check_default must be of type boolean but received {}'.format(type(check_default)))

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

        else:
            response.raise_for_status()

    def create(self, path):
        """
        Method to send a create post
        :param path: The NSO path to the data
        :return:
            Dictionary

        """
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_create_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def exists(self, path):
        """
        Method to send a exists post
        :param path: The NSO path to the data
        :return:
            Dictionary

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def get_case(self, path, choice):
        """
        Method to send a get_case post
        :param path: The NSO path to the data
        :param choice: ?
        :return:
            Dictionary

        """
        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(choice, str):
            raise TypeError('param choice must be of type string but received {}'.format(type(choice)))

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

        else:
            response.raise_for_status()

    def load(self, data, path='/', data_format='xml', mode='merge'):
        """
        Method to send a load post
        :param data: The data to be loaded in the transaction
        :param path: default /
        :param data_format: {'json', 'xml'} default xml
        :param mode: {'create', 'merge', 'replace'} default is merge
        :return:
            Dictionary

        """
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_create_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        if not isinstance(data, str):
            raise TypeError('param data must be of type string but received {}'.format(type(data)))

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if data_format not in {'json', 'xml'}:
            raise KeyError('param format must be one of these {"json", "xml"}')

        if mode not in {'create', 'merge', 'replace'}:
            raise KeyError('param mode must be one of these {"create", "merge", "replace"}')

        get_case_json = {'jsonrpc': '2.0',
                         'id': self.request_id,
                         'method': 'get_case',
                         'params': {
                             'th': self.transaction_handle,
                             'data': data,
                             'path': path,
                             'format': data_format,
                             'mode': mode
                         }}

        response = self.post_with_cookies(get_case_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def set_value(self, path, value, dry_run=False):
        """
        Method to send a set_value post
        :param path: The NSO path to the data
        :param value: The value to set the item to
        :param dry_run: Boolean default False, when set True tests if value is valid or not
        :return:
            Dictionary

        """
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_set_value_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

        if not isinstance(dry_run, bool):
            raise TypeError('param dry_run must be of type boolean but received {}'.format(type(dry_run)))

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

        else:
            response.raise_for_status()

    def validate_commit(self):
        """
        Method to send a validate_commit post, in the CLI commits are validated automatically, in JsonRPC
        they are not, but only validated commits can be committed
        :return:
            Dictionary

        """
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_set_value_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        validate_commit_json = {'jsonrpc': '2.0',
                                'id': self.request_id,
                                'method': 'validate_commit',
                                'params': {
                                    'th': self.transaction_handle,
                                }}

        response = self.post_with_cookies(validate_commit_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def commit(self, dry_run=True, output='cli', reverse=False):
        """
        Method to send a commit post, in the CLI commits are validated automatically, in JsonRPC
        they are not, but only validated commits can be commited

        :param dry_run: To output a dry run, default is True
        :param output: 'cli', 'native', 'xml' default is cli
        :param reverse: Output the revers of the config going in, default is False, only valid when
                        output equals native
        :return:
            Dictionary

        """
        flags = list()
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_set_value_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        if output not in {'cli', 'native', 'xml'}:
            raise KeyError('output should be one of these cli, native, xml you entered {}'.format(output))

        if not isinstance(dry_run, bool):
            raise TypeError('param dry_run must be of type boolean but received {}'.format(type(dry_run)))

        if not isinstance(reverse, bool):
            raise TypeError('param reverse must be of type boolean but received {}'.format(type(reverse)))

        if dry_run:
            flags.append('dry-run={}'.format(output))
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

        else:
            response.raise_for_status()

    def delete(self, path):
        """
        Method to send a delete post
        :param path: The NSO path to the data
        :return:
            Dictionary

        """
        if self.transaction_mode != 'read_write':
            raise ValueError('To use send_create_post the transaction mode must be read_'
                             'write the current transaction mode is {}'.format(self.transaction_mode))

        if not isinstance(path, str):
            raise TypeError('param path must be of type string but received {}'.format(type(path)))

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

        else:
            response.raise_for_status()

    def get_service_points(self):
        """
        Method to send a get_service_points post
        :return:
            Dictionary

        """
        get_service_points_json = {'jsonrpc': '2.0',
                                   'id': self.request_id,
                                   'method': 'get_service_points',
                                   }

        response = self.post_with_cookies(get_service_points_json)

        if response.ok:
            return response.json()

        else:
            response.raise_for_status()

    def get_template_variables(self, name):
        """
        Method to send a get_template_variables post, this retrieves device templates only
        :param name: The name of the template
        :return:
            Dictionary

        """
        if not isinstance(name, str):
            raise TypeError('param name must be of type string but received {}'.format(type(name)))

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

        else:
            response.raise_for_status()


if __name__ == '__main__':
    help(NsoJsonRpcComet)
    help(NsoJsonRpcConfig)

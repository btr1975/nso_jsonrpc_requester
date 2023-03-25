"""
Holds the common needs for the NSO-JSON RPC
"""
import json
import logging
import random
import requests
from urllib3.exceptions import InsecureRequestWarning
import yaml
# Reference https://community.cisco.com/t5/nso-developer-hub-documents/json-rpc-basics/ta-p/3635204

LOGGER = logging.getLogger('nso_jsonrpc')


class NsoJsonRpcCommon:
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
    :returns: NA init

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol: str = 'http', ip: str = '127.0.0.1',  # pylint: disable=invalid-name
                 port: str = '8080', username: str = 'admin', password: str = 'admin',
                 ssl_verify: bool = True) -> None:
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
        self.comet_id = f'remote-comet-{random.randint(1, 100000)}'
        self.comet_handles = []
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

        self.server_url = f'{protocol}://{ip}:{port}/jsonrpc'

    def login(self, ack_warning=False):
        """
        Method to send a login request, if the user is able to log in, the users cookie is set

        :type ack_warning: Boolean
        :param ack_warning: Default: False

        :rtype: Dict
        :return: A dictionary, also set's self.cookies with a Cookies object

        :raises TypeError: if ack_warning is not boolean

        """
        if not isinstance(ack_warning, bool):
            raise TypeError(f'param ack_warning must be of type boolean but received {type(ack_warning)}')

        login_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'login',
                      'params': {
                          'user': self.username,
                          'passwd': self.password
                      }}

        if self.protocol == 'http':
            response = requests.post(self.server_url, headers=self.headers, json=login_json, timeout=30)

        else:
            response = requests.post(self.server_url, headers=self.headers, json=login_json,
                                     verify=self.ssl_verify, timeout=30)

        if response.ok:
            self.cookies = response.cookies
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def logout(self):
        """
        Method to send a logout request

        :rtype: Dict
        :return: A dictionary of data

        """
        logout_json = {'jsonrpc': '2.0',
                       'id': self.request_id,
                       'method': 'logout',
                       }

        response = self.post_with_cookies(logout_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def new_trans(self, mode='read', conf_mode='private', tag=None, on_pending_changes='reuse'):
        """
        Method to request a new transaction

        :type mode: String
        :param mode: ('read', 'read_write') Default: read
        :type conf_mode: String
        :param conf_mode: ('private', 'shared', 'exclusive') Default: private
        :type tag: String
        :param tag: Default: None it is optional
        :type on_pending_changes: String
        :param on_pending_changes: ('reuse', 'reject', 'discard') Default: reuse

        :rtype: Dict
        :return: A dictionary, also set's self.transaction_handle with a transaction handle
                 self.transaction_mode with either ('read', 'read_write')

        :raises TypeError: if mode is not a string
        :raises ValueError: if mode is not ('read', 'read_write')
        :raises ValueError: if conf_mode not ('private', 'shared', 'exclusive')
        :raises ValueError: if on_pending_changes not ('reuse', 'reject', 'discard')
        :raises TypeError: if tag is supplied and is not a string

        """
        if not isinstance(mode, str):
            raise TypeError(f'param mode must be of type string but received {type(mode)}')

        if mode not in {'read', 'read_write'}:
            raise ValueError('param mode valid options are {"read", "read_write"}')

        if conf_mode not in {'private', 'shared', 'exclusive'}:
            raise ValueError('param conf_mode valid options are {"private", "shared", "exclusive"}')

        if on_pending_changes not in {'reuse', 'reject', 'discard'}:
            raise ValueError('param on_pending_changes valid options are {"reuse", "reject", "discard"}')

        if tag:
            if not isinstance(tag, str):
                raise TypeError(f'param tag must be of type string but received {type(tag)}')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def get_trans(self):
        """
        Method to get the all current transaction information

        :rtype: Dict
        :return: A dictionary of data

        """
        get_trans_json = {'jsonrpc': '2.0',
                          'id': self.request_id,
                          'method': 'get_trans'
                          }

        response = self.post_with_cookies(get_trans_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def get_system_setting(self, operation='version'):
        """
        Method to get get_system_setting information

        :type operation: String
        :param operation: ('capabilities', 'customizations' ,'models', 'user', 'version', 'all') Default: version

        :rtype: Dict
        :return: A dictionary of data

        :raises ValueError: if operation not ('capabilities', 'customizations' ,'models', 'user', 'version', 'all')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def abort(self, request_id):
        """
        Method to send abort post

        :type request_id: Integer
        :param request_id: Request ID to abort

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if request_id is not an integer

        """
        if not isinstance(request_id, int):
            raise TypeError(f'param request_id must be of type integer but received {type(request_id)}')

        abort_json = {'jsonrpc': '2.0',
                      'id': self.request_id,
                      'method': 'abort',
                      'params': {
                          'id': request_id
                      }}

        response = self.post_with_cookies(abort_json)
# pylint: disable=duplicate-code
        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def eval_xpath(self, xpath_expr):
        """
        Method to send eval_xpath post

        :type xpath_expr: String
        :param xpath_expr: The xpath to evaluate

        :rtype: Dict
        :return: A dictionary of data

        :raises TypeError: if xpath_expr is not an string

        """
        if not isinstance(xpath_expr, str):
            raise TypeError(f'param xpath_expr must be of type string but received {type(xpath_expr)}')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def post_with_cookies(self, json_data):
        """
        Method to request a post with yummy cookies

        :type json_data: Dict
        :param json_data: Json Data in a dictionary

        :rtype: requests response object
        :return: A requests response

        """
        if self.protocol == 'http':
            return requests.post(self.server_url, headers=self.headers, json=json_data,
                                 cookies=self.cookies, timeout=30)

        else:
            return requests.post(self.server_url, headers=self.headers, json=json_data, cookies=self.cookies,
                                 verify=self.ssl_verify, timeout=30)

    @staticmethod
    def print_pretty_json(json_data):  # pragma: no cover
        """
        Method to print response JSON real pretty like

        :type json_data: Dict
        :param json_data: JSON Data in a dictionary

        :rtype: None
        :return: prints pretty JSON

        """
        print(json.dumps(json_data, sort_keys=True, indent=4))
        LOGGER.debug(json.dumps(json_data, sort_keys=True, indent=4))

    @staticmethod
    def print_pretty_yaml(json_data):  # pragma: no cover
        """
        Method to print response JSON as YAML

        :type json_data: Dict
        :param json_data: JSON Data in a dictionary

        :rtype: None
        :return: prints pretty YAML

        """
        print(yaml.dump(json_data, default_flow_style=False, indent=4))
        LOGGER.debug(yaml.dump(json_data, default_flow_style=False, indent=4))

    @staticmethod
    def print_pretty_no_yaml_no_json(data):  # pragma: no cover
        """
        Method to print Non-JSON, Non-YAML real pretty

        :type data: String
        :param data: The Data

        :rtype: None
        :return: prints pretty text

        """
        for line in data.content.splitlines():
            print(line.decode("utf-8"))

        for line in data.content.splitlines():
            LOGGER.debug(line.decode("utf-8"))

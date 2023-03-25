"""
Holds the comet methods for the NSO-JSON RPC
"""
from nso_jsonrpc_requester.common import NsoJsonRpcCommon


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
    :returns: NA init

    :rasies TypeError: If protocol is not ('http', 'https')

    """

    def __init__(self, protocol: str = 'http', ip: str = '127.0.0.1', port: str = '8080',
                 username: str = 'admin', password: str = 'admin', ssl_verify: bool = True) -> None:
        super().__init__(protocol, ip, port, username, password, ssl_verify)
        self.comet_started = False
        self.start_comet()

    def __str__(self):  # pragma: no cover
        return '<NsoJsonRpcComet>'

    def start_comet(self):
        """
        Method to start the comet process

        :rtype: None
        :return: None

        """
        self.__check_comet_state(False)
        self.comet_started = True
        self.login()
        self.new_trans()
        self.__comet()

    def stop_comet(self):
        """
        Method to stop the comet process

        :rtype: None
        :return: None

        """
        self.__check_comet_state(True)
        self.__unsubscribe()
        self.__comet()
        self.logout()
        self.comet_started = False

    def comet_poll(self):
        """
        Method to return comet result only

        :rtype: String
        :return: result

        """
        self.__check_comet_state(True)

        try:
            return self.__comet()['result']

        except Exception as err:  # pragma: no cover
            self.stop_comet()

    def subscribe_changes(self, path):
        """
        Method to send a subscribe_changes post

        :type path: String
        :param path: The NSO KEYPATH to the data to watch for changes

        :rtype: Dict
        :return: A dictionary of data, also appends variables to self.comet_handles to the handle given by NSO

        :raises TypeError: if path is not a string

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def subscribe_poll_leaf(self, path, interval):
        """
        Method to send a subscribe_poll_leaf post

        :type path: String
        :param path: The NSO KEYPATH to the data to watch for changes
        :type interval: Integer
        :param interval: The interval of time for polling

        :rtype: Dict
        :return: A dictionary of data, also appends variables to self.comet_handles to the handle given by NSO

        :raises TypeError: if path is not a string
        :raises TypeError: if interval is not a integer

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

        if not isinstance(interval, int):
            raise TypeError(f'param interval must be of type integer but received {type(interval)}')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def subscribe_cdboper(self, path):
        """
        Method to send a subscribe_cdboper post

        :type path: String
        :param path: The NSO KEYPATH to the data to watch for changes

        :rtype: Dict
        :return: A dictionary of data, also appends variables to self.comet_handles to the handle given by NSO

        :raises TypeError: if path is not a string

        """
        self.__check_comet_state(True)

        if not isinstance(path, str):
            raise TypeError(f'param path must be of type string but received {type(path)}')

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

        else:  # pragma: no cover
            response.raise_for_status()

    def subscribe_upgrade(self):
        """
        Method to send a subscribe_upgrade post

        :rtype: Dict
        :return: A dictionary of data, also appends variables to self.comet_handles to the handle given by NSO

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

        else:  # pragma: no cover
            response.raise_for_status()

    def subscribe_jsonrpc_batch(self):
        """
        Method to send a subscribe_jsonrpc_batch post

        :rtype: Dict
        :return: A dictionary of data, also appends variables to self.comet_handles to the handle given by NSO

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

        else:  # pragma: no cover
            response.raise_for_status()

    def get_subscriptions(self):
        """
        Method to send a get_subscriptions post
        This get's the sessions subscriptions

        :rtype: Dict
        :return: A dictionary of subscriptions

        """
        self.__check_comet_state(True)

        get_subscriptions_json = {'jsonrpc': '2.0',
                                  'id': self.request_id,
                                  'method': 'get_subscriptions',
                                  }

        response = self.post_with_cookies(get_subscriptions_json)

        if response.ok:
            return response.json()

        else:  # pragma: no cover
            response.raise_for_status()

    def __comet(self):
        """
        Method to send a comet post
        comet is a log receiver, and can receive logs from the following methods
            start_cmd, subscribe_cdboper, subscribe_changes, subscribe_messages,
            subscribe_poll_leaf or subscribe_upgrade

        :rtype: Dict
        :return: A dictionary of data

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

        else:  # pragma: no cover
            response.raise_for_status()

    def __start_subscription(self, handle):
        """
        Method to send a start_subscription post

        :type handle: String
        :param handle: Handle to start the subscription on

        :rtype: Dict
        :return: A dictionary of data

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

        else:  # pragma: no cover
            response.raise_for_status()

    def __unsubscribe(self):
        """
        Method to send a unsubscribe post

        :rtype: Dict
        :return: A dictionary of data

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

            else:  # pragma: no cover
                response.raise_for_status()

    def __check_comet_state(self, wanted_state):
        """
        Method to verify comet state

        :type wanted_state: Boolean
        :param wanted_state: The state expected

        :rtype: None
        :return: None

        :raises Exception: if wanted_state is False, but it is True
        :raises Exception: if wanted_state is True, but it is False

        """
        if self.comet_started != wanted_state:
            if self.comet_started:
                raise Exception('Comet is already running!!')  # pylint: disable=broad-exception-raised

            if not self.comet_started:
                raise Exception('Comet is not running!!')  # pylint: disable=broad-exception-raised


if __name__ == '__main__':  # pragma: no cover
    help(NsoJsonRpcComet)

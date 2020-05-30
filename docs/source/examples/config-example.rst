Using NsoJsonRpcConfig
----------------------


What is NsoJsonRpcConfig for?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This class is used to get data from a NSO server, or set data on a NSO server.


How to use NsoJsonRpcConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the object, call login, call new_trans to create a new transaction, do what you want, and call logout,
when you are complete. There is a simple example below.


.. code-block:: python

    from nso_jsonrpc_requester import NsoJsonRpcConfig


    def main():
        nso_config_obj = NsoJsonRpcConfig('http', ip='10.0.0.146', ssl_verify=True)
        nso_config_obj.login()
        nso_config_obj.new_trans()
        data = nso_config_obj.get_list_keys('/services/base_spine_and_leaf:base_spine_and_leaf{unit-test}/location-devices')

        print(data)

        data = nso_config_obj.get_list_keys('/services/spine_and_leaf_devices')

        print(data)

        data = nso_config_obj.get_values("/services/base_spine_and_leaf:base_spine_and_leaf{unit-test}/location-devices{UNIT-TEST-NX-LEA10}", ['service'], check_default=True)

        print(data)

        nso_config_obj.logout()


    if __name__ == '__main__':
        main()

Using NsoJsonRpcConfig Query
----------------------------


What is NsoJsonRpcConfig Query for?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There set of methods are for querying the NSO CDB for data


How to use NsoJsonRpcConfig Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the object, call login, call new_trans to create a new transaction, do what you want, and call logout,
when you are complete. There is a simple example below.


.. code-block:: python

    from nso_jsonrpc_requester import NsoJsonRpcConfig


    def main():
        nso_config_obj = NsoJsonRpcConfig('http', ip='10.0.0.146', ssl_verify=True)
        nso_config_obj.login()
        nso_config_obj.new_trans()

        data = nso_config_obj.start_query("/services/spine_and_leaf_devices[location='unit-test']/l2vni-interfaces",
                                          selection=['interface-slot-port', 'l2vni', '../device-name'])
        print(data)

        new_data = nso_config_obj.run_query(data.get('result').get('qh'))

        print(nso_config_obj.print_pretty_json(new_data))

        nso_config_obj.stop_query(data.get('result').get('qh'))

        nso_config_obj.logout()


    if __name__ == '__main__':
        main()

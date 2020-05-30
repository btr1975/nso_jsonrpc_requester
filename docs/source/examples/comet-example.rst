Using NsoJsonRpcComet
---------------------


What is NsoJsonRpcComet for?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comet in NSO is basically remote logging from an NSO server.  It allows you to subscribe to KEYPATH locations in
the NSO CDB, and if something changes it will show you the changes.


How to use NsoJsonRpcComet
~~~~~~~~~~~~~~~~~~~~~~~~~~

The whole concept of Comet in NSO is to start a separate transaction with he NSO server before, making changes.  It will
then poll according to your time interval for logging of the items you were watching for. You create the transaction,
subscribe to items, and keep polling for results.  There is a simple example below.


.. code-block:: python

    from nso_jsonrpc_requester import NsoJsonRpcComet
    import time


    def main():
        nso_comet_obj = NsoJsonRpcComet('http', ip='10.0.0.146', ssl_verify=False)
        nso_comet_obj.subscribe_changes('/services/spine_and_leaf_devices')
        nso_comet_obj.subscribe_changes('/services/l2vni')
        nso_comet_obj.subscribe_changes('/services/l3vni')
        nso_comet_obj.subscribe_changes('/services/base_spine_and_leaf')
        nso_comet_obj.subscribe_changes('/services/bgp')
        nso_comet_obj.subscribe_changes('/services/external_vrf_bgp')
        nso_comet_obj.subscribe_upgrade()

        while True:
            try:
                result = nso_comet_obj.comet_poll()
                if result:
                    print(nso_comet_obj.print_pretty_json(result))
                time.sleep(1)

            except KeyboardInterrupt as e:
                nso_comet_obj.stop_comet()
                break

        print('EXIT')

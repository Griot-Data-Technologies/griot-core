==========
Connectors
==========

Data source connectors for fetching data as Arrow IPC.

DataConnector Protocol
----------------------

.. code-block:: python

   from griot_core.connectors import DataConnector

   class MyConnector(DataConnector):
       async def fetch_as_arrow(
           self,
           query: str | None = None,
           **kwargs
       ) -> bytes:
           # Return Arrow IPC bytes
           ...

ConnectorRegistry
-----------------

.. code-block:: python

   from griot_core.connectors import ConnectorRegistry

   registry = ConnectorRegistry()

   # Register connector
   registry.register("my-source", MyConnector, ...)

   # Create connector
   connector = registry.create_connector("my-source", config)

   # Fetch data
   arrow_data = await connector.fetch_as_arrow()

API Reference
-------------

.. automodule:: griot_core.connectors
   :members:
   :undoc-members:

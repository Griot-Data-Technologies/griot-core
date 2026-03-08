======
Export
======

Export schemas to JSON Schema format.

JSON Schema Export
------------------

.. code-block:: python

   from griot_core.export import export_to_jsonschema

   json_schema = export_to_jsonschema(
       schema,
       draft_version="2020-12",
       include_extensions=True,
   )

Supported Drafts
~~~~~~~~~~~~~~~~

- ``2020-12`` (default)
- ``draft-07``
- ``draft-04``

Extensions
~~~~~~~~~~

With ``include_extensions=True``, the output includes:

- ``x-griot-schema-id``
- ``x-griot-pii-type``
- ``x-griot-physical-type``

API Reference
-------------

.. automodule:: griot_core.export
   :members:
   :undoc-members:

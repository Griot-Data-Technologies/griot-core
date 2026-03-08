=======
Parsing
=======

YAML and JSON parsing for contracts and schemas.

Loading Contracts
-----------------

.. code-block:: python

   from griot_core import (
       load_contract,
       load_contract_from_string,
       load_contract_from_dict,
   )

   # From file
   contract = load_contract("path/to/contract.yaml")

   # From string
   contract = load_contract_from_string(yaml_content)

   # From dict
   contract = load_contract_from_dict(contract_dict)

YAML Parser
-----------

.. code-block:: python

   from griot_core.parsing import parse_contract_yaml, parse_schema_yaml

   contract = parse_contract_yaml(yaml_string)
   schema = parse_schema_yaml(yaml_string)

JSON Parser
-----------

.. code-block:: python

   from griot_core.parsing import parse_contract_json, parse_schema_json

   contract = parse_contract_json(json_string)
   schema = parse_schema_json(json_string)

Structure Validation
--------------------

.. code-block:: python

   from griot_core import validate_contract_structure

   result = validate_contract_structure(contract)

   if not result.is_valid:
       for issue in result.issues:
           print(f"[{issue.severity}] {issue.path}: {issue.message}")

API Reference
-------------

.. automodule:: griot_core.parsing
   :members:
   :undoc-members:

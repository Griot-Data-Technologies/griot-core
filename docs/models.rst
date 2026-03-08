======
Models
======

Core data models for the Griot contract system.

Overview
--------

The models module provides dataclasses representing the core entities:

- **Schema**: First-class data assets (tables, views, files)
- **Contract**: Data contracts with inheritance support
- **Property**: Column definitions with constraints
- **Check**: Validation rules with executor URIs
- **Enums**: Type definitions (LogicalType, Severity, etc.)

Schema
------

Schemas are first-class entities representing data assets.

.. code-block:: python

   from griot_core.models import Schema, Property
   from griot_core.models.enums import SchemaStatus, LogicalType

   schema = Schema(
       id="users-schema",
       name="Users",
       version="1.0.0",
       status=SchemaStatus.ACTIVE,
       physical_name="dim_users",
       description="User dimension table",
       owner_team="data-engineering",
       properties=[
           Property(
               id="user-id",
               name="user_id",
               logical_type=LogicalType.STRING,
               required=True,
               primary_key=True,
           ),
           Property(
               id="email",
               name="email",
               logical_type=LogicalType.STRING,
               is_pii=True,
           ),
       ],
   )

Contract
--------

Contracts define data quality expectations and can extend other contracts.

.. code-block:: python

   from griot_core.models import Contract
   from griot_core.models.enums import ContractStatus

   contract = Contract(
       id="users-contract",
       name="Users Contract",
       version="1.0.0",
       status=ContractStatus.ACTIVE,
       owner="data-engineering",
       extends="griot://templates/pii-contract@1.0",
       inline_schemas=[schema],
       checks=[...],
   )

Property
--------

Properties define columns/fields in a schema.

.. code-block:: python

   from griot_core.models import Property, PropertyConstraints
   from griot_core.models.enums import LogicalType, PIIType

   property = Property(
       id="email-property",
       name="email",
       logical_type=LogicalType.STRING,
       physical_type="VARCHAR(255)",
       description="User email address",
       required=True,
       unique=True,
       is_pii=True,
       pii_type=PIIType.EMAIL,
   )

Check
-----

Checks define validation rules with executor URIs.

.. code-block:: python

   from griot_core.models import Check, CheckCondition
   from griot_core.models.enums import CheckType, Severity

   check = Check(
       name="null_check",
       description="Ensure no nulls in required field",
       type=CheckType.DATA_QUALITY,
       executor="registry://executors/null-check@1.0",
       parameters={"column": "user_id", "threshold": 0},
       severity=Severity.CRITICAL,
       when=CheckCondition(
           environment=["production"],
           profile=["data_engineering"],
       ),
   )

Enums
-----

LogicalType
~~~~~~~~~~~

.. code-block:: python

   class LogicalType(str, Enum):
       STRING = "string"
       INTEGER = "integer"
       DECIMAL = "decimal"
       BOOLEAN = "boolean"
       DATE = "date"
       TIMESTAMP = "timestamp"
       ARRAY = "array"
       OBJECT = "object"

Severity
~~~~~~~~

.. code-block:: python

   class Severity(str, Enum):
       CRITICAL = "critical"
       WARNING = "warning"
       INFO = "info"

CheckType
~~~~~~~~~

.. code-block:: python

   class CheckType(str, Enum):
       DATA_QUALITY = "data_quality"
       PRIVACY = "privacy"
       SCHEMA = "schema"

PIIType
~~~~~~~

.. code-block:: python

   class PIIType(str, Enum):
       NAME = "name"
       EMAIL = "email"
       PHONE = "phone"
       SSN = "ssn"
       NATIONAL_ID = "national_id"
       CREDIT_CARD = "credit_card"
       ...

API Reference
-------------

.. automodule:: griot_core.models
   :members:
   :undoc-members:

.. automodule:: griot_core.models.enums
   :members:

.. automodule:: griot_core.models.schema
   :members:

.. automodule:: griot_core.models.contract
   :members:

.. automodule:: griot_core.models.property
   :members:

.. automodule:: griot_core.models.check
   :members:

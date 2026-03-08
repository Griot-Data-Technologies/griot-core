==========
Quickstart
==========

This guide will help you get started with griot-core for data contract validation.

Installation
------------

.. code-block:: bash

   pip install griot-core

   # With optional dependencies
   pip install griot-core[kubernetes]  # K8s dispatcher
   pip install griot-core[aws]         # Lambda dispatcher
   pip install griot-core[gcp]         # Cloud Run dispatcher

Basic Usage
-----------

Loading a Contract
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from griot_core import load_contract

   # From YAML file
   contract = load_contract("path/to/contract.yaml")

   # From YAML string
   yaml_content = """
   apiVersion: v1.0.0
   kind: DataContract
   id: my-contract
   name: My Contract
   version: 1.0.0
   status: active
   """
   contract = load_contract_from_string(yaml_content)

Creating Models Programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from griot_core.models import Contract, Schema, Property
   from griot_core.models.enums import SchemaStatus, LogicalType, ContractStatus

   # Create a schema
   schema = Schema(
       id="users-schema",
       name="Users",
       version="1.0.0",
       status=SchemaStatus.ACTIVE,
       physical_name="dim_users",
       properties=[
           Property(
               id="user-id",
               name="user_id",
               logical_type=LogicalType.STRING,
               required=True,
           ),
           Property(
               id="email",
               name="email",
               logical_type=LogicalType.STRING,
               is_pii=True,
           ),
       ],
   )

   # Create a contract
   contract = Contract(
       id="users-contract",
       name="Users Contract",
       version="1.0.0",
       status=ContractStatus.ACTIVE,
       owner="data-engineering",
       inline_schemas=[schema],
   )

Validation with Orchestration
-----------------------------

The recommended way to run validation is using the orchestration module,
which handles WASM/container check splitting and parallel execution.

Local Development
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from griot_core.orchestration import (
       ValidationOrchestrator,
       DispatcherConfig,
       ComputeBackend,
   )

   # Local dispatcher for development
   config = DispatcherConfig(backend=ComputeBackend.LOCAL)

   orchestrator = ValidationOrchestrator(dispatcher_config=config)

   # Run validation
   result = await orchestrator.validate(
       contract=contract,
       profile="data_engineering",
       data_reference={"file": "/path/to/data.parquet"},
   )

   print(f"Valid: {result.is_valid}")
   for check in result.check_results:
       status = "PASS" if check.passed else "FAIL"
       print(f"  [{status}] {check.check_name}")

Production (Kubernetes)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   config = DispatcherConfig(
       backend=ComputeBackend.KUBERNETES,
       wasm_worker_image="griot/wasm-worker:v1.0",
       timeout_seconds=600,
   )

   orchestrator = ValidationOrchestrator(
       dispatcher_config=config,
       callback_base_url="https://registry.example.com",
       namespace="griot",
       service_account="griot-worker",
   )

   # Async validation (results via callback)
   job_id = await orchestrator.validate(
       contract=contract,
       profile="data_engineering",
       data_reference={"s3": "s3://bucket/data.parquet"},
       wait_for_completion=False,
   )

   # Or wait for completion
   result = await orchestrator.validate(
       contract=contract,
       profile="data_engineering",
       data_reference={"s3": "s3://bucket/data.parquet"},
       wait_for_completion=True,
       timeout_seconds=1800,
   )

Using the Validation Engine Directly
------------------------------------

For simpler use cases or testing, you can use the ValidationEngine directly:

.. code-block:: python

   from griot_core.validation import ValidationEngine, ValidationOptions
   from griot_core.executors import ExecutorRuntime

   # Create engine
   engine = ValidationEngine(executor_runtime=ExecutorRuntime())

   # Run validation
   result = await engine.validate(
       contract=contract,
       options=ValidationOptions(
           profile="data_engineering",
           fail_fast=True,
       ),
   )

Execution Profiles
------------------

Profiles control which checks run for different use cases:

.. code-block:: python

   # Data engineering - all checks
   result = await orchestrator.validate(contract, profile="data_engineering", ...)

   # Software engineering - schema checks only
   result = await orchestrator.validate(contract, profile="software_engineering", ...)

   # Quick validation - critical checks only
   result = await orchestrator.validate(contract, profile="quick", ...)

   # Privacy audit - PII checks
   result = await orchestrator.validate(contract, profile="privacy_audit", ...)

Contract Inheritance
--------------------

Contracts can extend templates:

.. code-block:: python

   from griot_core.resolution import ContractResolver

   resolver = ContractResolver()

   # Register parent contract
   resolver.register(parent_contract)

   # Resolve inheritance
   resolved = resolver.resolve(child_contract)

   # resolved.resolved_definition has merged properties
   # resolved.inheritance_chain shows parent URIs

JSON Schema Export
------------------

Export schemas to JSON Schema format:

.. code-block:: python

   from griot_core.export import export_to_jsonschema

   json_schema = export_to_jsonschema(
       schema,
       draft_version="2020-12",
       include_extensions=True,
   )

Next Steps
----------

- :doc:`models` - Learn about Schema, Contract, Property, Check models
- :doc:`orchestration` - Deep dive into compute orchestration
- :doc:`validation` - ValidationEngine and profiles
- :doc:`executors` - WASM and container runtime
- :doc:`workers` - Deploy workers to Lambda, K8s, Cloud Run

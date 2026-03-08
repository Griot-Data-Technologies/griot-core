==================
griot-core Library
==================

``griot-core`` is the foundation library for the Griot data contract system.
It provides all core functionality including models, validation, parsing,
orchestration, and executor runtime.

.. important::

   ``griot-core`` is **framework-agnostic**. It does NOT import pandas, polars,
   pyspark, or dask. All DataFrame processing happens inside WASM/Container
   executors. Data is exchanged using Arrow IPC format.

Installation
------------

.. code-block:: bash

   pip install griot-core

   # With compute backend support
   pip install griot-core[kubernetes]
   pip install griot-core[aws]
   pip install griot-core[gcp]

Architecture Overview
---------------------

.. code-block:: text

   griot-core/
   ├── models/        # Schema, Contract, Property, Check, Enums
   ├── parsing/       # YAML/JSON parsing and validation
   ├── resolution/    # Contract inheritance resolution
   ├── export/        # JSON Schema export
   ├── validation/    # ValidationEngine, ProfileResolver
   ├── executors/     # WASM/Container runtime
   ├── orchestration/ # Compute orchestration, job splitting, dispatchers
   ├── connectors/    # Data source connectors
   ├── workers/       # Lambda, K8s, Cloud Run, WASM workers
   ├── integrations/  # Airflow, Prefect, Dagster
   └── privacy/       # PII patterns and validators

Key Concepts
------------

**Schema-First Architecture**
   Schemas are first-class entities representing data assets (tables, views, files).
   Contracts reference schemas rather than embedding them.

**Contract Inheritance**
   Contracts can extend templates or other contracts using the ``extends`` field.
   Child properties are deep-merged with parent properties.

**Profile-Based Validation**
   Different teams run different check subsets using execution profiles:
   ``data_engineering``, ``software_engineering``, ``data_science``, etc.

**Orchestration with Smart Job Splitting**
   The orchestration module separates WASM and container checks, running them
   in parallel. WASM checks run in a single worker container; container checks
   spawn as native K8s pods (no Docker-in-Docker).

**Executor Runtime**
   Validation checks run inside WASM modules or containers, receiving Arrow IPC
   data and returning structured results.

Quick Example
-------------

.. code-block:: python

   from griot_core.orchestration import (
       ValidationOrchestrator,
       DispatcherConfig,
       ComputeBackend,
   )

   # Configure orchestrator for Kubernetes
   config = DispatcherConfig(
       backend=ComputeBackend.KUBERNETES,
       wasm_worker_image="griot/wasm-worker:v1.0",
   )

   orchestrator = ValidationOrchestrator(
       dispatcher_config=config,
       namespace="griot",
   )

   # Execute validation
   result = await orchestrator.validate(
       contract=my_contract,
       profile="data_engineering",
       data_reference={"s3": "s3://bucket/data.parquet"},
   )

   print(f"Valid: {result.is_valid}")
   print(f"Passed: {result.passed_checks}/{result.total_checks}")

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Core Modules

   models
   parsing
   resolution
   export

.. toctree::
   :maxdepth: 2
   :caption: Validation & Orchestration

   validation
   orchestration
   executors

.. toctree::
   :maxdepth: 2
   :caption: Data & Connectivity

   connectors

.. toctree::
   :maxdepth: 2
   :caption: Deployment

   workers
   integrations

.. toctree::
   :maxdepth: 2
   :caption: Privacy & Compliance

   privacy

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

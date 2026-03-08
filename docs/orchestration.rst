=============
Orchestration
=============

The orchestration module provides compute orchestration for validation jobs.
It implements smart job splitting to avoid Docker-in-Docker issues and enables
parallel execution of WASM and container checks.

.. note::

   This module was moved from ``griot-registry`` to ``griot-core`` to provide
   better separation of concerns. The registry now imports orchestration from
   ``griot_core.orchestration``.

Overview
--------

The key challenge in distributed validation is handling mixed check types:

- **WASM checks**: Run inside a worker using embedded WASM runtime
- **Container checks**: Require running a container

Running containers inside containers (Docker-in-Docker) is problematic in
Kubernetes environments. The orchestration module solves this by:

1. Splitting jobs by runtime type (JobSplitter)
2. Running WASM checks in a single worker container
3. Spawning container checks as native K8s pods
4. Running all jobs in parallel and aggregating results (ResultAggregator)

Architecture
------------

.. code-block:: text

   Contract with mixed checks
           │
           ▼
   ┌──────────────────┐
   │   JobSplitter    │  Separates WASM vs Container checks
   └──────────────────┘
           │
           ├──► WASM checks ────► griot-core worker pod (runs all WASM)
           │                              │
           ├──► Container check A ──► K8s pod (native)  │
           │                                            ├──► PARALLEL
           ├──► Container check B ──► K8s pod (native)  │
           │                                            │
           ▼                                            │
   ┌──────────────────┐                                 │
   │ ResultAggregator │ ◄───────────────────────────────┘
   └──────────────────┘
           │
           ▼
     AggregatedResult

Key Benefits
~~~~~~~~~~~~

1. **No Docker-in-Docker**: Container checks run as native K8s pods
2. **Parallel execution**: WASM and container checks run simultaneously
3. **Efficient WASM batching**: All WASM checks run in one container
4. **Result aggregation**: Combines results from all parallel jobs

Quick Start
-----------

.. code-block:: python

   from griot_core.orchestration import (
       ValidationOrchestrator,
       DispatcherConfig,
       ComputeBackend,
   )

   # Configure for Kubernetes
   config = DispatcherConfig(
       backend=ComputeBackend.KUBERNETES,
       wasm_worker_image="griot/wasm-worker:v1.0",
       timeout_seconds=600,
   )

   # Create orchestrator
   orchestrator = ValidationOrchestrator(
       dispatcher_config=config,
       callback_base_url="https://registry.example.com",
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

Components
----------

ValidationOrchestrator
~~~~~~~~~~~~~~~~~~~~~~

The main entry point for orchestrated validation.

.. code-block:: python

   class ValidationOrchestrator:
       def __init__(
           self,
           dispatcher_config: DispatcherConfig | None = None,
           dispatcher: ComputeDispatcher | None = None,
           splitter: JobSplitter | None = None,
           callback_base_url: str | None = None,
           **dispatcher_kwargs,
       ): ...

**Methods:**

- ``validate(contract, profile, data_reference, ...)``: Execute validation
- ``validate_checks(job_id, checks, ...)``: Lower-level API with explicit checks
- ``receive_callback(job_id, result)``: Handle worker callback
- ``get_aggregator(job_id)``: Get result aggregator for a job

JobSplitter
~~~~~~~~~~~

Separates checks by runtime type.

.. code-block:: python

   from griot_core.orchestration import JobSplitter, CheckSpec, CheckRuntime

   splitter = JobSplitter()

   checks = [
       CheckSpec(
           name="null_check",
           executor_uri="registry://null-check@1.0",
           runtime=CheckRuntime.WASM,
       ),
       CheckSpec(
           name="drift_check",
           executor_uri="oci://ghcr.io/griot/drift:1.0",
           runtime=CheckRuntime.CONTAINER,
       ),
   ]

   split_job = splitter.split(
       job_id="job-123",
       contract_id="orders",
       contract_version="1.0.0",
       profile="data_engineering",
       checks=checks,
       data_reference={"s3": "s3://bucket/data.parquet"},
   )

   # split_job.wasm_job contains WASM checks
   # split_job.container_jobs contains one job per container check

ResultAggregator
~~~~~~~~~~~~~~~~

Collects results from parallel executions.

.. code-block:: python

   from griot_core.orchestration import ResultAggregator

   aggregator = ResultAggregator(split_job)
   aggregator.start()

   # As results come in from callbacks
   aggregator.add_wasm_result(wasm_callback_data)
   aggregator.add_container_result(container_callback_data)

   # Check completion
   if aggregator.is_complete:
       result = aggregator.aggregate()
       print(f"Valid: {result.is_valid}")

Compute Dispatchers
-------------------

ComputeDispatcher Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~

All dispatchers implement this interface:

.. code-block:: python

   class ComputeDispatcher(ABC):
       @abstractmethod
       async def dispatch_wasm_worker(self, spec: WasmJobSpec) -> DispatchResult:
           """Dispatch WASM checks to a worker container."""
           ...

       @abstractmethod
       async def dispatch_container(self, spec: ContainerJobSpec) -> DispatchResult:
           """Dispatch a single container check as a native pod."""
           ...

       @abstractmethod
       async def check_status(self, invocation_id: str) -> dict:
           """Check job status."""
           ...

       @abstractmethod
       async def cancel(self, invocation_id: str) -> bool:
           """Cancel a running job."""
           ...

KubernetesDispatcher
~~~~~~~~~~~~~~~~~~~~

Creates native K8s Jobs for both WASM workers and container checks.

.. code-block:: python

   from griot_core.orchestration import (
       KubernetesDispatcher,
       DispatcherConfig,
       ComputeBackend,
   )

   config = DispatcherConfig(
       backend=ComputeBackend.KUBERNETES,
       wasm_worker_image="griot/wasm-worker:v1.0",
       timeout_seconds=600,
       memory_mb=1024,
       cpu_millicores=1000,
       labels={"app": "griot"},
   )

   dispatcher = KubernetesDispatcher(
       config,
       namespace="griot",
       service_account="griot-worker",
   )

LambdaDispatcher
~~~~~~~~~~~~~~~~

Uses AWS Lambda for serverless execution.

.. code-block:: python

   from griot_core.orchestration import LambdaDispatcher

   dispatcher = LambdaDispatcher(
       config,
       wasm_function_name="griot-wasm-worker",
       container_function_prefix="griot-check-",
   )

CloudRunDispatcher
~~~~~~~~~~~~~~~~~~

Uses Google Cloud Run for serverless containers.

.. code-block:: python

   from griot_core.orchestration import CloudRunDispatcher

   dispatcher = CloudRunDispatcher(
       config,
       project_id="my-project",
       region="us-central1",
       wasm_service_url="https://griot-wasm-worker-xxx.run.app",
   )

LocalDispatcher
~~~~~~~~~~~~~~~

For development and testing.

.. code-block:: python

   from griot_core.orchestration import LocalDispatcher

   dispatcher = LocalDispatcher(config, max_workers=4)

Factory Function
~~~~~~~~~~~~~~~~

.. code-block:: python

   from griot_core.orchestration import create_dispatcher, DispatcherConfig

   config = DispatcherConfig(backend=ComputeBackend.KUBERNETES, ...)
   dispatcher = create_dispatcher(config, namespace="griot")

Type Definitions
----------------

CheckSpec
~~~~~~~~~

.. code-block:: python

   @dataclass
   class CheckSpec:
       name: str
       executor_uri: str
       runtime: CheckRuntime  # WASM or CONTAINER
       parameters: dict[str, Any] = field(default_factory=dict)
       severity: str = "warning"
       timeout_seconds: int = 300

       @classmethod
       def from_executor_uri(cls, name: str, executor_uri: str, **kwargs):
           """Create CheckSpec, inferring runtime from URI."""

WasmJobSpec
~~~~~~~~~~~

.. code-block:: python

   @dataclass
   class WasmJobSpec:
       job_id: str
       contract_id: str
       contract_version: str
       profile: str
       checks: list[CheckSpec]  # All WASM checks batched together
       data_reference: dict[str, Any]
       callback_url: str | None = None
       timeout_seconds: int = 600

ContainerJobSpec
~~~~~~~~~~~~~~~~

.. code-block:: python

   @dataclass
   class ContainerJobSpec:
       job_id: str
       parent_job_id: str
       contract_id: str
       contract_version: str
       check: CheckSpec  # Single container check
       data_reference: dict[str, Any]
       image: str | None = None  # Extracted from executor_uri
       timeout_seconds: int = 600
       resource_limits: dict[str, str] = field(default_factory=dict)

SplitJob
~~~~~~~~

.. code-block:: python

   @dataclass
   class SplitJob:
       parent_job_id: str
       wasm_job: WasmJobSpec | None  # If any WASM checks
       container_jobs: list[ContainerJobSpec]  # One per container check
       total_checks: int

       @property
       def has_wasm_checks(self) -> bool: ...
       @property
       def has_container_checks(self) -> bool: ...

AggregatedResult
~~~~~~~~~~~~~~~~

.. code-block:: python

   @dataclass
   class AggregatedResult:
       job_id: str
       contract_id: str
       contract_version: str
       profile: str
       is_valid: bool
       total_checks: int
       passed_checks: int
       failed_checks: int
       check_results: list[CheckResultItem]
       wasm_execution_time_ms: float | None
       container_execution_time_ms: float | None
       total_execution_time_ms: float | None
       errors: list[str]

DispatcherConfig
~~~~~~~~~~~~~~~~

.. code-block:: python

   @dataclass
   class DispatcherConfig:
       backend: ComputeBackend
       wasm_worker_image: str = "griot/wasm-worker:latest"
       timeout_seconds: int = 600
       memory_mb: int = 512
       cpu_millicores: int = 1000
       retry_count: int = 3
       environment: dict[str, str] = field(default_factory=dict)
       labels: dict[str, str] = field(default_factory=dict)

WASM Worker
-----------

The ``WasmWorker`` class runs inside the WASM worker container.

.. code-block:: python

   from griot_core.workers import WasmWorker

   # Entry point for container
   async def main():
       worker = WasmWorker()
       result = await worker.run()  # Reads spec from env vars

   # Or execute specific checks
   worker = WasmWorker()
   result = await worker.execute_wasm_checks(wasm_job_spec)

**Environment Variables:**

- ``GRIOT_JOB_SPEC``: JSON-serialized WasmJobSpec
- ``GRIOT_JOB_ID``: Job identifier
- ``GRIOT_CALLBACK_URL``: URL to POST results

Integration with Registry
-------------------------

The griot-registry uses the orchestration module:

.. code-block:: python

   # In griot-registry/services/validation_jobs.py
   from griot_core.orchestration import (
       ValidationOrchestrator,
       ComputeBackend,
       DispatcherConfig,
   )

   class ValidationJobService:
       def __init__(self, storage, settings):
           self._orchestrator = None

       @property
       def orchestrator(self) -> ValidationOrchestrator:
           if self._orchestrator is None:
               config = DispatcherConfig(
                   backend=ComputeBackend(self.settings.compute_backend),
                   wasm_worker_image=self.settings.wasm_worker_image,
               )
               self._orchestrator = ValidationOrchestrator(
                   dispatcher_config=config,
                   callback_base_url=self.settings.callback_base_url,
               )
           return self._orchestrator

API Reference
-------------

.. automodule:: griot_core.orchestration
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: griot_core.orchestration.types
   :members:

.. automodule:: griot_core.orchestration.splitter
   :members:

.. automodule:: griot_core.orchestration.aggregator
   :members:

.. automodule:: griot_core.orchestration.orchestrator
   :members:

.. automodule:: griot_core.orchestration.dispatcher
   :members:

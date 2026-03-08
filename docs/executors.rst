=========
Executors
=========

The executors module provides WASM and container runtime for executing
validation checks.

Overview
--------

Executors are versioned, portable validation modules that can be:

- **WASM modules**: Sandboxed, fast startup, portable
- **Container images**: Full-featured, flexible

.. code-block:: text

   ┌─────────────┐     Arrow IPC      ┌─────────────┐
   │   Engine    │ ─────────────────► │  Executor   │
   │             │                    │  (WASM/     │
   │             │ ◄───────────────── │  Container) │
   └─────────────┘     CheckResult    └─────────────┘

ExecutorRuntime
---------------

Unified interface for both WASM and container execution.

.. code-block:: python

   from griot_core.executors import ExecutorRuntime

   runtime = ExecutorRuntime()

   # Check capabilities
   caps = runtime.capabilities
   print(f"WASM available: {caps.wasm_available}")
   print(f"Container available: {caps.container_available}")

   # Execute a check
   result = await runtime.execute(executor_spec, check, arrow_data)

ExecutorRegistry
----------------

Registry of available executors.

.. code-block:: python

   from griot_core.executors import ExecutorRegistry

   registry = ExecutorRegistry()

   # Get built-in executor
   spec = registry.get_executor("registry://executors/null-check@1.0")

   # Register custom executor
   registry.register_executor(my_executor_spec)

   # List all executors
   for spec in registry.list_executors():
       print(f"{spec.id}@{spec.version}: {spec.description}")

Built-in Executors
~~~~~~~~~~~~~~~~~~

- ``null-check``: Check for null values
- ``unique-check``: Check for uniqueness
- ``pattern-check``: Regex pattern validation
- ``range-check``: Numeric range validation
- ``row-count``: Row count validation
- ``freshness-check``: Data freshness validation
- ``masking-check``: PII masking validation
- ``pii-detection``: Detect PII in data
- ``distribution-drift``: Statistical drift detection
- ``referential-check``: Referential integrity

WasmRuntime
-----------

WASM execution using wasmtime.

.. code-block:: python

   from griot_core.executors import WasmRuntime

   runtime = WasmRuntime(cache_dir="/tmp/wasm-cache")

   result = await runtime.execute(
       executor_spec,
       check,
       arrow_data,
       timeout=30,
   )

ContainerRuntime
----------------

Container execution using Podman/Docker.

.. code-block:: python

   from griot_core.executors import ContainerRuntime, ContainerConfig

   config = ContainerConfig(
       runtime="podman",  # or "docker"
       memory_limit="512m",
       cpu_limit="1.0",
       network_mode="none",  # Sandboxed
       timeout=60,
   )

   runtime = ContainerRuntime(config)

   result = await runtime.execute(
       executor_spec,
       check,
       arrow_data,
   )

ExecutorSpec
------------

Specification for an executor.

.. code-block:: python

   @dataclass
   class ExecutorSpec:
       id: str                    # e.g., "null-check"
       version: str               # e.g., "1.0.0"
       runtime: Runtime           # WASM or CONTAINER
       artifact_url: str          # URL to WASM file or OCI image
       description: str = ""
       input_schema: dict = None  # Expected parameters
       output_schema: dict = None # Result format
       tags: list[str] = field(default_factory=list)

CheckResult
-----------

Result from check execution.

.. code-block:: python

   @dataclass
   class CheckResult:
       passed: bool
       metric_value: float | None = None
       threshold: float | None = None
       operator: str | None = None
       details: dict = field(default_factory=dict)
       samples: list[dict] = field(default_factory=list)
       error: str | None = None

API Reference
-------------

.. automodule:: griot_core.executors
   :members:
   :undoc-members:

.. automodule:: griot_core.executors.types
   :members:

.. automodule:: griot_core.executors.registry
   :members:

.. automodule:: griot_core.executors.runtime
   :members:

.. automodule:: griot_core.executors.wasm_runtime
   :members:

.. automodule:: griot_core.executors.container_runtime
   :members:

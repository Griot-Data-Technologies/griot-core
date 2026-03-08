==========
Validation
==========

The validation module provides the ValidationEngine for executing checks
and the ProfileResolver for profile-based check selection.

.. note::

   For production deployments, consider using the :doc:`orchestration` module
   which handles job splitting, parallel execution, and result aggregation.

ValidationEngine
----------------

The ValidationEngine orchestrates check execution.

.. code-block:: python

   from griot_core.validation import ValidationEngine, ValidationOptions
   from griot_core.executors import ExecutorRuntime

   engine = ValidationEngine(executor_runtime=ExecutorRuntime())

   result = await engine.validate(
       contract=contract,
       options=ValidationOptions(
           profile="data_engineering",
           fail_fast=True,
           max_parallel=4,
       ),
   )

   print(f"Valid: {result.is_valid}")
   print(f"Passed: {result.passed_checks}/{result.total_checks}")

ValidationOptions
~~~~~~~~~~~~~~~~~

.. code-block:: python

   @dataclass
   class ValidationOptions:
       profile: str = "default"
       mode: ValidationMode = ValidationMode.FULL
       fail_fast: bool = False
       max_parallel: int = 10
       timeout_seconds: int = 300
       dry_run: bool = False
       sample_size: int | None = None

ValidationMode
~~~~~~~~~~~~~~

.. code-block:: python

   class ValidationMode(str, Enum):
       FULL = "full"           # Run all checks
       SAMPLE = "sample"       # Run on sample data
       SCHEMA_ONLY = "schema_only"  # Schema validation only
       QUICK = "quick"         # Critical checks only

ProfileResolver
---------------

Resolves which checks to run for a given profile.

.. code-block:: python

   from griot_core.validation import ProfileResolver

   resolver = ProfileResolver()

   # Get checks for a profile
   resolved = resolver.resolve(contract, profile="data_engineering")

   for check in resolved.checks:
       print(f"Will run: {check.name}")

Default Profiles
~~~~~~~~~~~~~~~~

- **default**: All checks
- **data_engineering**: All checks
- **software_engineering**: Schema and constraint checks
- **data_science**: Quality and schema checks
- **privacy_audit**: Privacy-related checks
- **quick**: Critical checks only

Auto-Generated Checks
~~~~~~~~~~~~~~~~~~~~~

The ProfileResolver auto-generates checks from property constraints:

- ``nullable`` constraint → ``null-check``
- ``unique`` constraint → ``unique-check``
- ``primary_key`` → ``null-check`` + ``unique-check``
- ``is_pii`` with masking → ``masking-check``

ValidationResult
----------------

.. code-block:: python

   @dataclass
   class ValidationResult:
       contract_id: str
       contract_version: str
       is_valid: bool
       started_at: datetime
       completed_at: datetime
       profile: str
       mode: ValidationMode
       schema_results: list[SchemaValidationResult]
       summary: ValidationSummary
       metadata: dict

   @dataclass
   class ValidationSummary:
       total_checks: int
       passed_checks: int
       failed_checks: int
       skipped_checks: int
       warnings: int
       critical_failures: int

API Reference
-------------

.. automodule:: griot_core.validation
   :members:
   :undoc-members:

.. automodule:: griot_core.validation.engine
   :members:

.. automodule:: griot_core.validation.profile
   :members:

.. automodule:: griot_core.validation.result
   :members:

.. automodule:: griot_core.validation.types
   :members:

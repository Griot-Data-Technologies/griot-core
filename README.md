# griot-core

Core library for the Griot data contract system. Provides contract models, validation, parsing, orchestration, and executor runtime.

## Features

- **Schema-First Models**: First-class schema entities with property definitions
- **Contract Inheritance**: Templates and `extends` support with deep merge
- **Validation Engine**: Profile-based check execution
- **Orchestration**: Smart job splitting to avoid Docker-in-Docker
- **Executor Runtime**: WASM and container execution
- **Workers**: Lambda, K8s, Cloud Run, and local workers

## Installation

```bash
pip install griot-core

# With compute backends
pip install griot-core[kubernetes]
pip install griot-core[aws]
pip install griot-core[gcp]
```

## Quick Start

### Loading Contracts

```python
from griot_core import load_contract

contract = load_contract("path/to/contract.yaml")
```

### Validation with Orchestration

```python
from griot_core.orchestration import (
    ValidationOrchestrator,
    DispatcherConfig,
    ComputeBackend,
)

# Configure for Kubernetes
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
    contract=contract,
    profile="data_engineering",
    data_reference={"s3": "s3://bucket/data.parquet"},
)

print(f"Valid: {result.is_valid}")
print(f"Passed: {result.passed_checks}/{result.total_checks}")
```

### Local Development

```python
config = DispatcherConfig(backend=ComputeBackend.LOCAL)
orchestrator = ValidationOrchestrator(dispatcher_config=config)

result = await orchestrator.validate(
    contract=contract,
    profile="data_engineering",
    data_reference={"file": "/path/to/data.parquet"},
)
```

## Architecture

```
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
```

## Orchestration Module

The orchestration module handles compute orchestration for validation jobs:

- **JobSplitter**: Separates WASM and container checks
- **ValidationOrchestrator**: Main entry point
- **ResultAggregator**: Combines parallel execution results
- **Dispatchers**: K8s, Lambda, Cloud Run, Local

This avoids Docker-in-Docker by:
1. Running WASM checks in a single worker container
2. Spawning container checks as native K8s pods
3. Executing all jobs in parallel

## Important

griot-core is **framework-agnostic**. It does NOT import pandas, polars, pyspark, or dask. All DataFrame processing happens inside WASM/Container executors. Data is exchanged using Arrow IPC format.

## Documentation

```bash
cd docs
pip install -r requirements.txt
sphinx-build -b html . _build/html
```

## License

Apache-2.0

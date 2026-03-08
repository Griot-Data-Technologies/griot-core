"""
Griot Core Workers.

This module provides worker entrypoints for different compute environments.
Workers are the execution units that receive validation jobs from the registry
and run them using the ValidationEngine.

Supported compute environments:
- Local: For development and testing
- AWS Lambda: Serverless execution on AWS
- Kubernetes: Container-based execution on K8s
- Cloud Run: Serverless containers on GCP

Special workers:
- WasmWorker: Dedicated WASM-only worker for running inside containers
  (used by the orchestration module to avoid Docker-in-Docker)
"""
from __future__ import annotations

from .base import (
    Worker,
    WorkerConfig,
    WorkerResult,
    WorkerStatus,
    JobPayload,
    ContractFetcher,
)
from .local import LocalWorker, LocalContractFetcher, run_local_validation
from .lambda_worker import LambdaWorker, handler as lambda_handler
from .kubernetes import KubernetesWorker
from .cloudrun import CloudRunWorker
from .wasm_worker import WasmWorker, WasmCheckResult, WasmWorkerResult

__all__ = [
    # Base types
    "Worker",
    "WorkerConfig",
    "WorkerResult",
    "WorkerStatus",
    "JobPayload",
    "ContractFetcher",
    # Local Worker
    "LocalWorker",
    "LocalContractFetcher",
    "run_local_validation",
    # AWS Lambda
    "LambdaWorker",
    "lambda_handler",
    # Kubernetes
    "KubernetesWorker",
    # Cloud Run
    "CloudRunWorker",
    # WASM Worker (for orchestration)
    "WasmWorker",
    "WasmCheckResult",
    "WasmWorkerResult",
]

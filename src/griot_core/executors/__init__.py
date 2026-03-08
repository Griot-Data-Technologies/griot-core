"""
Griot Core Executor Runtime.

This module provides the executor runtime for running validation checks.
Executors can be WASM modules or container images that receive Arrow IPC
data and return CheckResult.
"""
from __future__ import annotations

from .types import CheckResult, ExecutorResult, ExecutorSpec
from .registry import ExecutorRegistry, ExecutorNotFoundError, InvalidExecutorURIError
from .wasm_runtime import WasmRuntime, WasmExecutionResult
from .container_runtime import ContainerRuntime, ContainerConfig, ContainerExecutionResult
from .runtime import ExecutorRuntime, RuntimeCapabilities

__all__ = [
    # Types
    "CheckResult",
    "ExecutorResult",
    "ExecutorSpec",
    # Registry
    "ExecutorRegistry",
    "ExecutorNotFoundError",
    "InvalidExecutorURIError",
    # WASM Runtime
    "WasmRuntime",
    "WasmExecutionResult",
    # Container Runtime
    "ContainerRuntime",
    "ContainerConfig",
    "ContainerExecutionResult",
    # Unified Runtime
    "ExecutorRuntime",
    "RuntimeCapabilities",
]

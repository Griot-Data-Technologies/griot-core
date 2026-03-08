"""
Griot Core Validation Module.

This module provides the validation engine for running checks
against data using executor runtime.
"""
from __future__ import annotations

from .result import (
    ValidationResult,
    SchemaValidationResult,
    CheckExecutionResult,
    ValidationSummary,
    ValidationMode,
    CheckStatus,
)
from .types import (
    ValidationContext,
    ValidationOptions,
    ProfileConfig,
)
from .profile import (
    ProfileResolver,
    ResolvedProfile,
    ResolvedCheck,
)
from .engine import ValidationEngine

__all__ = [
    # Results
    "ValidationResult",
    "SchemaValidationResult",
    "CheckExecutionResult",
    "ValidationSummary",
    "ValidationMode",
    "CheckStatus",
    # Types
    "ValidationContext",
    "ValidationOptions",
    "ProfileConfig",
    # Profile
    "ProfileResolver",
    "ResolvedProfile",
    "ResolvedCheck",
    # Engine
    "ValidationEngine",
]

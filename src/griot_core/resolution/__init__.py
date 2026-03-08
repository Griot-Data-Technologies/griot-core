"""
Griot Core Resolution Module.

This module provides contract inheritance resolution,
merging parent contracts with child overrides.
"""
from __future__ import annotations

from .resolver import (
    ContractResolver,
    ResolvedContract,
    InMemoryFetcher,
    ContractNotFoundError,
    CircularInheritanceError,
)
from .merge import deep_merge

__all__ = [
    "ContractResolver",
    "ResolvedContract",
    "InMemoryFetcher",
    "ContractNotFoundError",
    "CircularInheritanceError",
    "deep_merge",
]

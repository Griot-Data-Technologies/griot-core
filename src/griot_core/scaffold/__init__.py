"""Scaffold module — code generation from data contracts.

Provides lock-file management, type mapping, code generation,
and Jinja2-based template rendering for scaffolding boilerplate
pipeline code from approved data contracts.
"""

from griot_core.scaffold.dbt_codegen import DbtArtifactGenerator

__all__ = ["DbtArtifactGenerator"]

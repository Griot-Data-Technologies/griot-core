"""
Griot Core Entity Models.

This module provides dataclasses for all core entities in the Griot
data contract system, including Schema, Contract, Property, and Check.
"""
from __future__ import annotations

from .enums import (
    Cardinality,
    CheckCategory,
    CheckType,
    ComplianceFramework,
    ContractStatus,
    LogicalType,
    MaskingStrategy,
    PIIType,
    RelationshipType,
    Runtime,
    SchemaStatus,
    Sensitivity,
    Severity,
)
from .property import Property, PropertyConstraints, Relationship
from .check import Check, CheckCondition
from .schema import Schema
from .schema_ref import SchemaRef
from .contract import (
    # Main contract class
    Contract,
    # Description
    ContractDescription,
    # Executor configuration
    ExecutorConfig,
    ExecutorProfile,
    AutoCheckConfig,
    # Compliance configuration
    ComplianceConfig,
    LegalConfig,
    Regulation,
    DataSubjectRights,
    DataSubjectRight,
    RetentionPolicy,
    CrossBorderConfig,
    AuditConfig,
    ExportControls,
    # SLA configuration
    SLAConfig,
    # Governance configuration
    GovernanceConfig,
    ReviewConfig,
    ChangeManagement,
    ApprovalWorkflow,
    # Infrastructure
    Server,
    TeamConfig,
    TeamMember,
    SupportChannel,
    AuthoritativeDefinition,
)

__all__ = [
    # Enums
    "Cardinality",
    "CheckCategory",
    "CheckType",
    "ComplianceFramework",
    "ContractStatus",
    "LogicalType",
    "MaskingStrategy",
    "PIIType",
    "RelationshipType",
    "Runtime",
    "SchemaStatus",
    "Sensitivity",
    "Severity",
    # Core Models
    "Check",
    "CheckCondition",
    "Contract",
    "Property",
    "PropertyConstraints",
    "Relationship",
    "Schema",
    "SchemaRef",
    # Contract Description
    "ContractDescription",
    # Executor Configuration
    "ExecutorConfig",
    "ExecutorProfile",
    "AutoCheckConfig",
    # Compliance Configuration
    "ComplianceConfig",
    "LegalConfig",
    "Regulation",
    "DataSubjectRights",
    "DataSubjectRight",
    "RetentionPolicy",
    "CrossBorderConfig",
    "AuditConfig",
    "ExportControls",
    # SLA Configuration
    "SLAConfig",
    # Governance Configuration
    "GovernanceConfig",
    "ReviewConfig",
    "ChangeManagement",
    "ApprovalWorkflow",
    # Infrastructure
    "Server",
    "TeamConfig",
    "TeamMember",
    "SupportChannel",
    "AuthoritativeDefinition",
]

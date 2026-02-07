# Feature Specification: Action Notation Schema

**Feature Branch**: `025-action-schema`  
**Created**: 2026-02-06  
**Status**: Draft  
**Target**: Week 3 | **Repository**: WARScribe-Core

## User Scenarios & Testing

### User Story 1 - Define Action Types (Priority: P1)

System provides standardized action type definitions.

**Acceptance Scenarios**:
1. **Given** action data, **When** validated, **Then** conforms to schema
2. **Given** invalid action, **When** validated, **Then** error raised

---

## Requirements

### Functional Requirements
- **FR-001**: Schema MUST define all action types (MOVE, SHOOT, etc.)
- **FR-002**: Schema MUST be JSON Schema compatible
- **FR-003**: Schema MUST support extension for editions

### Key Entities
- **Action**: type, source, target, params
- **ActionSchema**: types[], validators[]

## Success Criteria
- **SC-001**: 100% of game actions representable
- **SC-002**: Schema validates in <10ms

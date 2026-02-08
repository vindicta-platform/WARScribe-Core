# Feature Proposal: Army List Import/Export Hub

**Proposal ID**: FEAT-010
**Author**: Unified Product Architect (Autonomous)
**Created**: 2026-02-01
**Status**: Draft
**Priority**: Critical
**Target Repository**: WARScribe-Core

---

## Part A: Software Design Document (SDD)

### 1. Executive Summary

Create a universal army list import/export hub supporting multiple formats (BattleScribe, NewRecruit, plain text) to maximize interoperability with the broader Warhammer community ecosystem.

### 2. System Architecture

#### 2.1 Current State

- WARScribe notation engine (JSON schema)
- No import from other formats
- Limited export options

#### 2.2 Proposed Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Import/Export Hub                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Format Router                         │    │
│  │   Detect format → Select adapter → Transform            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                  │
│      ┌───────────────────────┼───────────────────────┐          │
│      ▼                       ▼                       ▼          │
│ ┌──────────┐          ┌──────────┐          ┌──────────┐        │
│ │BattleScribe│        │NewRecruit│          │PlainText │        │
│ │  Adapter  │          │  Adapter │          │  Parser  │        │
│ │(.ros/.rosz)│         │  (.json) │          │  (.txt)  │        │
│ └──────────┘          └──────────┘          └──────────┘        │
│      │                       │                       │          │
│      └───────────────────────┴───────────────────────┘          │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │             WARScribe Canonical Format                  │    │
│  │                (Internal JSON Schema)                   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.3 File Changes

```text
WARScribe-Core/
├── src/
│   └── warscribe/
│       ├── adapters/
│       │   ├── __init__.py         [NEW]
│       │   ├── battlescribe.py     [NEW] .ros/.rosz import/export
│       │   ├── newrecruit.py       [NEW] NewRecruit JSON
│       │   └── plaintext.py        [NEW] Text parsing
│       ├── hub.py                  [NEW] Format router
│       └── schema.py               [MODIFY] Validation updates
├── tests/
│   ├── fixtures/                   [NEW] Sample files per format
│   └── test_adapters.py            [NEW]
└── docs/
    └── formats.md                  [NEW] Format documentation
```

### 3. Supported Formats

| Format                   | Import | Export | Notes                  |
| ------------------------ | ------ | ------ | ---------------------- |
| WARScribe JSON           | ✅      | ✅      | Canonical format       |
| BattleScribe XML (.ros)  | ✅      | ✅      | Most popular           |
| BattleScribe Zip (.rosz) | ✅      | ✅      | Compressed XML         |
| NewRecruit JSON          | ✅      | ✅      | Mobile app format      |
| Plain Text               | ✅      | ✅      | Tournament submissions |
| Tabletop Simulator       | ❌      | ✅      | Export only            |

### 4. BattleScribe Adapter

```python
class BattleScribeAdapter:
    """Import/export BattleScribe roster files."""

    def import_ros(self, file: BinaryIO) -> ArmyList:
        """Parse BattleScribe .ros XML into ArmyList."""

    def import_rosz(self, file: BinaryIO) -> ArmyList:
        """Decompress and parse .rosz file."""

    def export_ros(self, army: ArmyList) -> bytes:
        """Export ArmyList to BattleScribe XML."""
```

### 5. Plain Text Parser (Tournament Format)

```text
++ ARMY FACTION: NECRONS ++
++ DETACHMENT: Hypercrypt Legion ++
++ POINTS: 2000 ++

CHARACTERS
- Overlord [105pts]: Resurrection Orb
- Technomancer [60pts]: Canoptek Cloak

BATTLELINE
- 10x Necron Warriors [100pts]: Gauss Flayers
- 10x Necron Warriors [100pts]: Gauss Reapers

...
```

### 6. Data Preservation

- Round-trip fidelity: import → export preserves all data
- Unsupported fields stored in `_metadata`
- Warnings for lossy conversions
- Validation before export

---

## Part B: Behavior Driven Development (BDD)

### User Stories

#### US-001: Import from BattleScribe

**As a** competitive player
**I want to** import my BattleScribe lists
**So that** I can use Vindicta tools without re-entering data

#### US-002: Share Tournament List

**As a** tournament organizer
**I want** players to export plain-text lists
**So that** I can collect standardized submissions

#### US-003: Cross-Platform Sync

**As a** mobile user
**I want to** export to NewRecruit format
**So that** I can view my lists on my phone

### Acceptance Criteria

```gherkin
Feature: Army List Import/Export

  Scenario: Import BattleScribe roster
    Given I have a valid BattleScribe .rosz file
    When I upload it to the import hub
    Then it should be converted to WARScribe format
    And display the army list with all units and options
    And show any warnings for unsupported features

  Scenario: Export to plain text
    Given I have an army list in WARScribe format
    When I select "Export as Plain Text"
    Then a tournament-ready text file should be generated
    And it should include points totals per unit
    And match standard tournament submission format

  Scenario: Round-trip preservation
    Given I import a BattleScribe file
    When I export it back to BattleScribe format
    Then the output should be functionally identical
    And BattleScribe should open it without errors
```

---

## Implementation Estimate

| Phase                | Effort       | Dependencies   |
| -------------------- | ------------ | -------------- |
| BattleScribe Adapter | 10 hours     | XML parsing    |
| NewRecruit Adapter   | 4 hours      | JSON schema    |
| PlainText Parser     | 6 hours      | Regex patterns |
| Format Router        | 3 hours      | None           |
| Testing              | 6 hours      | Sample files   |
| **Total**            | **29 hours** |                |

---

## References

- [BattleScribe XML Format](https://github.com/BSData/catalogue-development/wiki)
- [NewRecruit App](https://www.newrecruit.eu/)
- [WARScribe Notation Spec](file:///c:/Users/bfoxt/Vindicta-Platform/platform-core/specs/003-warscribe-notation)

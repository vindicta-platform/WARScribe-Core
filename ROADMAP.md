# WARScribe-Core Roadmap

> **Vision**: The edition-agnostic notation engine for Warhammer gameplay  
> **Status**: Active Development  
> **Last Updated**: 2026-02-05

---

## 📅 6-Week Schedule (Feb 4 - Mar 17, 2026)

> **GitHub Project**: https://github.com/orgs/vindicta-platform/projects/4  
> **Master Roadmap**: https://github.com/vindicta-platform/.github/blob/master/ROADMAP.md

### Week 1: Feb 4-10 — Schema Refinement ✅
| Day | Task | Priority | Status |
|-----|------|----------|--------|
| Mon 4 | Schema refinement and validation | P1 | ✅ PR #7 |
| Tue 5 | Design edition abstraction layer | P1 | ✅ PR #8 |
| Wed 6 | Implement edition abstraction interfaces | P1 | ✅ PR #8 |
| Thu 7 | Unit tests for schema | P1 | ✅ PR #8 |
| Fri 8 | Complete unit tests | P1 | ✅ 100% coverage |
| **Sun 10** | **v0.1.5 Schema Release** | ⭐ | **On track** |

**Status**: 100% complete ahead of schedule! Edition abstraction fully implemented with tests.

### Week 2: Feb 11-17 — Edition Plugin
| Day | Task | Priority |
|-----|------|----------|
| Mon 11 | Edition plugin architecture | P1 |
| Tue 12 | 10th Edition plugin (part 1) | P1 |
| Wed 13 | 10th Edition plugin (part 2) | P1 |
| Thu 14 | Tests for edition plugin | P1 |
| Fri 15 | Complete tests | P1 |
| **Sun 17** | **v0.2.0 Edition Layer Release** | ⭐ |

### Weeks 3-6: Continued Development
*Focus on 11th Edition plugin scaffold and stable API for Primordia AI consumption*

---

## v1.0 Target: March 2026

### Mission Statement

Deliver a stable, production-ready notation engine that records Warhammer games in a machine-readable format, supporting both 10th and 11th Edition through pluggable edition modules.

---

## Milestone Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│  Feb 2026          Mar 2026          Apr 2026                   │
│  ─────────────────────────────────────────────────────────────  │
│  [v0.1.0]          [v0.2.0]          [v1.0.0]                   │
│  Foundation        Edition Layer     Production                 │
│                                                                  │
│  Week 1-2          Week 3-4          Week 5-8                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## v0.1.0 — Foundation (Target: Feb 10, 2026)

### Deliverables
- [x] Extract warscribe module from platform-core
- [x] Define core notation schema (JSON Schema)
- [x] Implement basic notation engine
- [x] Action types: Move, Shoot, Charge, Fight
- [x] Unit reference system
- [x] Transcript serialization (JSON)
- [x] Edition abstraction layer (delivered early!)

### Key Measurable Results
| Metric | Target | Status |
|--------|--------|--------|
| **Schema Coverage** | 100% of core action types | ✅ Complete |
| **Serialization Round-trip** | 100% fidelity | ✅ Complete |
| **Documentation** | API reference complete | ⚠️ EditionPlugin docs pending (Issue #9) |

### Exit Criteria
- [x] `warscribe-core` package installable via pip
- [x] Unit tests passing (100% coverage on edition abstraction)
- [x] Edition plugin system implemented
- [ ] README documentation complete (Issue #9 - Week 2)

**Status**: 90% complete, 1 day ahead of schedule. Documentation pending.

---

*Last Updated: 2026-02-05*

# WARScribe-Core Roadmap

> **Vision**: The edition-agnostic notation engine for Warhammer gameplay  
> **Status**: Active Development  
> **Last Updated**: 2026-02-04

---

## 📅 6-Week Schedule (Feb 4 - Mar 17, 2026)

> **GitHub Project**: https://github.com/orgs/vindicta-platform/projects/4  
> **Master Roadmap**: https://github.com/vindicta-platform/.github/blob/master/ROADMAP.md

### Week 1: Feb 4-10 — Schema Refinement
| Day | Task | Priority |
|-----|------|----------|
| Mon 4 | Schema refinement and validation | P1 |
| Tue 5 | Design edition abstraction layer | P1 |
| Wed 6 | Implement edition abstraction interfaces | P1 |
| Thu 7 | Unit tests for schema | P1 |
| Fri 8 | Complete unit tests | P1 |
| **Sun 10** | **v0.1.5 Schema Release** | ⭐ |

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
- [ ] Extract warscribe module from platform-core
- [ ] Define core notation schema (JSON Schema)
- [ ] Implement basic notation engine
- [ ] Action types: Move, Shoot, Charge, Fight
- [ ] Unit reference system
- [ ] Transcript serialization (JSON)

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Schema Coverage** | 100% of core action types | Unit tests pass |
| **Serialization Round-trip** | 100% fidelity | Parse → Serialize → Parse identical |
| **Documentation** | API reference complete | All public methods documented |

### Exit Criteria
- [ ] `warscribe-core` package installable via pip
- [ ] 10 example transcripts in test suite
- [ ] README with installation and usage

---

## v0.2.0 — Edition Abstraction Layer (Target: Feb 24, 2026)

### Deliverables
- [ ] Edition plugin interface
- [ ] 10th Edition plugin (complete)
- [ ] 11th Edition plugin (scaffold)
- [ ] Phase sequence validation
- [ ] Action context (unit stats, modifiers)

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Edition Isolation** | 0 edition-specific code in core | Code review |
| **10th Ed Coverage** | All phases implemented | Integration tests |
| **Plugin API Stability** | No breaking changes after v0.2 | Semantic versioning |

### Exit Criteria
- [ ] 10th Edition games recordable end-to-end
- [ ] Edition plugin documentation
- [ ] Migration guide for 11th Edition authors

---

## v1.0.0 — Production Release (Target: Mar 31, 2026)

### Deliverables
- [ ] Full spec compliance
- [ ] 10th Edition plugin stable
- [ ] 11th Edition plugin complete
- [ ] PyPI publication
- [ ] Comprehensive test suite (>90% coverage)
- [ ] Performance optimization

### Key Measurable Results
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Test Coverage** | >90% | pytest-cov report |
| **Performance** | <100ms transcript parse | Benchmark suite |
| **Adoption** | 100+ transcripts recorded | Usage telemetry |
| **PyPI Downloads** | 50+/month | PyPI stats |

### Exit Criteria
- [ ] No critical bugs for 2 weeks
- [ ] External contributor guide published
- [ ] Primordia AI integration validated

---

## Key Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| **Primordia AI** | Primary consumer — structured training data |
| **Logi-Slate-UI** | Frontend integration |
| **Meta-Oracle** | Game outcome analysis |
| **Community** | Battle report sharing |

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| platform-core | ✅ Exists | Extract warscribe module |
| Pydantic v2 | ✅ Available | Schema validation |
| Primordia AI | 🔄 Parallel dev | Consumer of transcripts |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 11th Edition delayed | Medium | High | Scaffold plugin early |
| Schema changes break consumers | Low | High | Semantic versioning |
| Performance issues at scale | Low | Medium | Benchmark from v0.1 |

---

## Out of Scope for v1

- Army list validation (separate product)
- Replay visualization (Logi-Slate responsibility)
- Natural language parsing (WARScribe-Parser responsibility)

---

## Success Criteria for v1

1. **Stability**: No breaking API changes for 6 months post-v1
2. **Adoption**: Primordia AI training on 100+ transcripts
3. **Extensibility**: Community can author edition plugins
4. **Performance**: Sub-second transcript processing

---

*Maintained by: Vindicta Platform Team*

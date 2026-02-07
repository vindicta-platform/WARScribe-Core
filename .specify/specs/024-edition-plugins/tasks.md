# Tasks: Edition Plugin System

**Input**: specs/024-edition-plugins/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/plugins/` directory
- [ ] T002 [P] Create `base.py`, `registry.py`

---

## Phase 2: Foundational

- [ ] T003 Define abstract EditionPlugin base class
- [ ] T004 [P] Define required plugin contract methods

---

## Phase 3: User Story 1 - Register Edition Plugin (P1) 🎯 MVP

- [ ] T005 [US1] Implement PluginRegistry class
- [ ] T006 [US1] Add `register(plugin)` method
- [ ] T007 [US1] Validate plugin implements contract
- [ ] T008 [US1] Raise ValidationError on invalid plugin
- [ ] T009 [US1] Implement 10th Edition plugin

---

## Phase 4: Polish

- [ ] T010 [P] Add plugin discovery mechanism
- [ ] T011 [P] Write contract validation tests

# Tasks: Transcript Serializer

**Input**: specs/026-transcript-serializer/ | **Prerequisites**: spec.md, plan.md

## Phase 1: Setup

- [ ] T001 Create `src/serialization/` directory
- [ ] T002 [P] Add orjson dependency

---

## Phase 2: Foundational

- [ ] T003 Define Transcript Pydantic model
- [ ] T004 [P] Define SerializedTranscript model

---

## Phase 3: User Story 1 - Serialize Game Transcript (P1) 🎯 MVP

- [ ] T005 [US1] Implement `serialize()` method
- [ ] T006 [US1] Implement `deserialize()` method
- [ ] T007 [US1] Add checksum generation
- [ ] T008 [US1] Validate round-trip integrity

---

## Phase 4: Polish

- [ ] T009 [P] Optimize for large transcripts
- [ ] T010 [P] Write serialization tests

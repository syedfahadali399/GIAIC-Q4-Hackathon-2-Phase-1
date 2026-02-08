---
description: "Task list for Basic Todo Operations feature implementation"
---

# Tasks: Basic Todo Operations

**Input**: Design documents from `/specs/001-basic-todo-operations/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Manual testing for Phase I (automated tests not requested for Basic Level)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use repository root structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src/ directory for source code
- [X] T002 Create src/__init__.py to mark package
- [X] T003 Create requirements.txt with rich>=13.0.0 (optional dependency)
- [X] T004 Create .gitignore with Python patterns (__pycache__, *.pyc, .env)

**Checkpoint**: Project structure ready for code implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create TodoItemDict TypedDict in src/models.py with 9 fields (id, title, description, completed, priority, tags, created_at, updated_at, due_date)
- [X] T006 [P] Add type hints imports in src/models.py (from datetime import datetime; from typing import Optional, TypedDict)
- [X] T007 [P] Initialize TodoManager class in src/todo_manager.py with __init__ method
- [X] T008 [P] Add TodoManager state: self.tasks list and self._next_id counter in src/todo_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create todo tasks with title and optional fields (description, priority, tags, due_date)

**Independent Test**: Launch app, add task with title "Buy groceries", verify task created with ID 1, success message displayed, task details shown

### Implementation for User Story 1

- [X] T009 [P] [US1] Implement _validate_title method in src/todo_manager.py (check non-empty, max 200 chars)
- [X] T010 [P] [US1] Implement _validate_description method in src/todo_manager.py (check max 1000 chars)
- [X] T011 [P] [US1] Implement _validate_priority method in src/todo_manager.py (check high/medium/low, normalize to lowercase)
- [X] T012 [P] [US1] Implement _parse_tags method in src/todo_manager.py (parse comma-separated string to list, normalize, deduplicate)
- [X] T013 [P] [US1] Implement _parse_due_date method in src/todo_manager.py (parse YYYY-MM-DD HH:MM format, handle optional)
- [X] T014 [US1] Implement add_task method in src/todo_manager.py (validate inputs, generate ID, create task dict, append to list, increment _next_id)
- [X] T015 [P] [US1] Create ConsoleUI class with __init__ in src/ui.py (accept TodoManager dependency)
- [X] T016 [P] [US1] Implement _get_input helper method in src/ui.py (generic input prompt with strip)
- [X] T017 [P] [US1] Implement _show_success helper method in src/ui.py (display green success message if possible)
- [X] T018 [P] [US1] Implement _show_error helper method in src/ui.py (display red error message if possible)
- [X] T019 [US1] Implement handle_add_task method in src/ui.py (prompt for all fields, call manager.add_task, display result)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (can add tasks via console)

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to see all tasks in a formatted table with ID, Title, Priority, Status, Due Date, Tags

**Independent Test**: Add 2-3 tasks, select "View All Tasks", verify all tasks displayed in table format with correct columns

### Implementation for User Story 2

- [X] T020 [US2] Implement view_all_tasks method in src/todo_manager.py (return self.tasks list)
- [X] T021 [P] [US2] Implement _format_priority helper in src/ui.py (convert "high" → "High", etc.)
- [X] T022 [P] [US2] Implement _format_status helper in src/ui.py (True → "✓", False → "✗")
- [X] T023 [P] [US2] Implement _format_due_date helper in src/ui.py (datetime → "YYYY-MM-DD HH:MM" or "-" if None)
- [X] T024 [P] [US2] Implement _format_tags helper in src/ui.py (list → comma-separated string, truncate if needed)
- [X] T025 [US2] Implement _format_task_table method in src/ui.py (use rich.Table if available, else plain text)
- [X] T026 [US2] Implement handle_view_all_tasks method in src/ui.py (call manager.view_all_tasks, display table or "No tasks found")

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (can add and view tasks)

---

## Phase 5: User Story 3 - Delete Task (Priority: P2)

**Goal**: Enable users to delete tasks by ID with confirmation prompt

**Independent Test**: Add a task, note ID, select "Delete Task", enter ID, confirm, verify task removed from list

### Implementation for User Story 3

- [X] T027 [P] [US3] Implement _find_task_by_id helper in src/todo_manager.py (search list for matching ID, return task or None)
- [X] T028 [US3] Implement delete_task method in src/todo_manager.py (find by ID, raise ValueError if not found, remove from list)
- [X] T029 [US3] Implement handle_delete_task method in src/ui.py (prompt for ID, show confirmation, call manager.delete_task, handle errors)

**Checkpoint**: All user stories (1, 2, 3) should now be independently functional (complete CRUD for Basic Level)

---

## Phase 6: Integration & Main Application

**Purpose**: Wire all components together into complete application with menu system

- [X] T030 [P] Implement display_welcome method in src/ui.py (show welcome banner)
- [X] T031 [P] Implement display_goodbye method in src/ui.py (show goodbye message)
- [X] T032 [P] Implement display_menu method in src/ui.py (show 4 menu options: Add, View, Delete, Exit)
- [X] T033 [P] Implement get_menu_choice method in src/ui.py (validate input 1-4, loop until valid)
- [X] T034 [US1] [US2] [US3] Implement run method in src/ui.py (main loop: display menu, get choice, dispatch to handlers, repeat until exit)
- [X] T035 Create main.py in src/main.py with entry point: initialize TodoManager, create ConsoleUI, call ui.run()
- [X] T036 Add if __name__ == "__main__" block in src/main.py to enable direct execution

**Checkpoint**: Complete application ready - can run python src/main.py and use all features

---

## Phase 7: Validation & Testing

**Purpose**: Manual testing of all user stories and edge cases

- [ ] T037 Test US1 Scenario 1: Add task with title only, verify ID 1 and success message
- [ ] T038 Test US1 Scenario 2: Add task with title and description, verify both fields saved
- [ ] T039 Test US1 Scenario 3: Add task with high priority, verify priority displayed correctly
- [ ] T040 Test US1 Scenario 4: Add task with due date "2025-12-30 14:00", verify date saved
- [ ] T041 Test US1 Scenario 5: Add task with tags "work,urgent", verify both tags assigned
- [ ] T042 Test US2 Scenario 1: Add 3 tasks, view all, verify table shows all with correct columns
- [ ] T043 Test US2 Scenario 2: View tasks when empty, verify "No tasks found" message
- [ ] T044 Test US2 Scenario 3: Add tasks with different priorities, verify display shows High/Medium/Low
- [ ] T045 Test US2 Scenario 4: Verify pending tasks show ✗ symbol
- [ ] T046 Test US2 Scenario 5: Add tasks with tags, verify tags displayed in readable format
- [ ] T047 Test US3 Scenario 1: Delete task, verify confirmation prompt appears
- [ ] T048 Test US3 Scenario 2: Confirm deletion with "yes", verify success message and task removed
- [ ] T049 Test US3 Scenario 3: Cancel deletion with "no", verify task NOT deleted
- [ ] T050 Test US3 Scenario 4: Enter non-existent ID 999, verify error "Task ID 999 not found"
- [ ] T051 Test US3 Scenario 5: Delete task from list of 3, verify only 2 remain
- [ ] T052 Test Edge Case: Empty title, verify error "Title cannot be empty. Please enter a title."
- [ ] T053 Test Edge Case: Invalid priority "urgent", verify error "Invalid priority. Please choose: high, medium, or low."
- [ ] T054 Test Edge Case: Invalid date format "12/30/2025", verify error "Invalid date format. Please use: YYYY-MM-DD HH:MM"
- [ ] T055 Test Edge Case: Title > 200 chars, verify error "Title too long. Maximum 200 characters allowed."
- [ ] T056 Test Edge Case: Description > 1000 chars, verify error "Description too long. Maximum 1000 characters allowed."
- [ ] T057 Test Edge Case: Invalid menu option "5", verify error "Invalid option. Please choose 1-4."
- [ ] T058 Test menu option 4 (Exit), verify goodbye message and application exits cleanly

**Checkpoint**: All acceptance scenarios and edge cases validated - Basic Level complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational completion - No dependencies on other stories (can run parallel with US1)
- **User Story 3 (Phase 5)**: Depends on Foundational completion - No dependencies on other stories (can run parallel with US1/US2)
- **Integration (Phase 6)**: Depends on all user stories (US1, US2, US3) completion
- **Validation (Phase 7)**: Depends on Integration completion

### User Story Dependencies

- **User Story 1 (P1 - Add Task)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - View All Tasks)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2 - Delete Task)**: Can start after Foundational (Phase 2) - No dependencies on other stories

**Note**: All three user stories are independent and can be developed in parallel once Foundational phase completes

### Within Each User Story

**User Story 1 (Add Task)**:
- T009-T013: Validation and parsing helpers [P] - can all run in parallel
- T014: add_task method - depends on T009-T013 complete
- T015-T018: UI helpers [P] - can all run in parallel, independent of manager
- T019: handle_add_task - depends on T014 complete (manager) and T015-T018 complete (UI helpers)

**User Story 2 (View All Tasks)**:
- T020: view_all_tasks method - can start immediately
- T021-T024: Format helpers [P] - can all run in parallel
- T025: _format_task_table - depends on T021-T024 complete
- T026: handle_view_all_tasks - depends on T020 and T025 complete

**User Story 3 (Delete Task)**:
- T027: _find_task_by_id helper [P] - can run in parallel with other helpers
- T028: delete_task method - depends on T027 complete
- T029: handle_delete_task - depends on T028 complete

### Parallel Opportunities

- **Setup Phase**: All tasks (T001-T004) can run in parallel [not marked P because they're trivial file creation]
- **Foundational Phase**: T005-T006 [P], T007-T008 [P] can run in parallel
- **User Story 1**: T009-T013 [P] in parallel, then T014; T015-T018 [P] in parallel, then T019
- **User Story 2**: T021-T024 [P] in parallel, then T025 and T026
- **User Story 3**: T027 [P] can run with other helpers
- **Integration**: T030-T033 [P] can run in parallel, then T034-T036
- **After Foundational**: All three user stories (Phase 3, 4, 5) can be developed in parallel by different developers

---

## Parallel Example: User Story 1 (Add Task)

```bash
# Step 1: Launch all validation helpers in parallel
Task: "Implement _validate_title method in src/todo_manager.py"
Task: "Implement _validate_description method in src/todo_manager.py"
Task: "Implement _validate_priority method in src/todo_manager.py"
Task: "Implement _parse_tags method in src/todo_manager.py"
Task: "Implement _parse_due_date method in src/todo_manager.py"

# Step 2: After all helpers complete, implement add_task
Task: "Implement add_task method in src/todo_manager.py"

# Step 3: In parallel with Step 1-2, launch UI helpers
Task: "Create ConsoleUI class with __init__ in src/ui.py"
Task: "Implement _get_input helper method in src/ui.py"
Task: "Implement _show_success helper method in src/ui.py"
Task: "Implement _show_error helper method in src/ui.py"

# Step 4: After add_task and UI helpers complete, implement handler
Task: "Implement handle_add_task method in src/ui.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T008)
3. Complete Phase 3: User Story 1 - Add Task (T009-T019)
4. **STOP and VALIDATE**: Test adding tasks independently
5. Optionally: Add minimal main.py to enable testing

**Result**: Working MVP where users can add tasks via console

### Incremental Delivery (Recommended)

1. **Foundation**: Complete Setup + Foundational → Foundation ready
2. **MVP (US1)**: Add User Story 1 → Test independently → Deliverable 1 ✅
3. **Enhanced (US1 + US2)**: Add User Story 2 → Test independently → Deliverable 2 ✅
4. **Complete Basic Level (US1 + US2 + US3)**: Add User Story 3 → Test independently → Deliverable 3 ✅
5. **Integrated App**: Complete Integration → Test complete flow → Final Deliverable ✅

Each deliverable adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. **Team together**: Complete Setup + Foundational (critical path)
2. **Once Foundational is done, split work**:
   - Developer A: User Story 1 (Add Task) - T009-T019
   - Developer B: User Story 2 (View All Tasks) - T020-T026
   - Developer C: User Story 3 (Delete Task) - T027-T029
3. **Stories complete independently**: Each developer can test their story in isolation
4. **Team together**: Integration (T030-T036) and Validation (T037-T058)

---

## Task Summary

**Total Tasks**: 58
- Setup: 4 tasks
- Foundational: 4 tasks (BLOCKING)
- User Story 1 (Add Task): 11 tasks
- User Story 2 (View All Tasks): 7 tasks
- User Story 3 (Delete Task): 3 tasks
- Integration: 7 tasks
- Validation: 22 tasks (manual testing)

**Parallel Opportunities**:
- Foundational: 4 tasks can run in parallel (after setup)
- US1: 9 tasks can run in parallel (5 manager helpers + 4 UI helpers)
- US2: 4 tasks can run in parallel (format helpers)
- Integration: 4 tasks can run in parallel (display methods)
- **Cross-Story Parallelism**: All 3 user stories can be developed in parallel (21 total implementation tasks)

**Critical Path** (sequential dependencies):
1. Setup (any task) → 2. Foundational (T005-T008) → 3. US1 core (T014, T019) OR US2 core (T020, T026) OR US3 core (T028, T029) → 4. Integration (T034-T036) → 5. Validation

**Estimated Effort**:
- **MVP (US1 only)**: ~8 implementation tasks (T001-T008 + T009-T019) + minimal integration
- **Basic Level Complete**: 36 implementation tasks (T001-T036)
- **Fully Validated**: 58 tasks total (including 22 manual tests)

---

## Notes

- **[P] tasks** = Different files, no dependencies within phase
- **[Story] label** = Maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Commit after each completed user story or logical group
- **Tests**: Manual testing approach for Phase I (automated tests in future phases)
- **No TDD**: Tests requested for Basic Level, validating with manual scenarios instead
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Constitutional Alignment

- ✅ **Principle I (Spec-First)**: Tasks generated from complete specifications (spec.md, plan.md, contracts/)
- ✅ **Principle II (Agent-Driven)**: Tasks organized for agent execution with clear file paths and acceptance criteria
- ✅ **Principle III (Incremental)**: Tasks grouped by user story priority (P1, P1, P2), enabling MVP-first delivery
- ✅ **Principle IV (Code Quality)**: Validation tasks, error handling tasks, type hints in foundational phase
- ✅ **Principle V (Data Management)**: Foundational phase establishes in-memory data model, no external dependencies

---

**Tasks Status**: ✅ READY FOR IMPLEMENTATION
**Next Command**: `/sp.implement` to execute tasks via Claude Code agents
**MVP Scope**: T001-T019 (Setup + Foundational + User Story 1)
**Full Basic Level**: T001-T036 (all implementation tasks)
**Fully Validated**: T001-T058 (implementation + manual testing)

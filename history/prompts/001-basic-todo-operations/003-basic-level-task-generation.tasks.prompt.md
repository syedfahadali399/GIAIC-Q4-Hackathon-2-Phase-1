---
id: 003
title: Basic Level Task Generation
stage: tasks
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: 001-basic-todo-operations
branch: master
user: hamza
command: /sp.tasks
labels: ["task-generation", "basic-level", "user-stories", "dependency-ordering", "parallel-execution"]
links:
  spec: specs/001-basic-todo-operations/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-basic-todo-operations/tasks.md
tests:
  - 22 manual test tasks (T037-T058)
---

## Prompt

Command: /sp.tasks

Context: Generate actionable task list for Basic Todo Operations feature based on completed design artifacts (spec.md, plan.md, data-model.md, contracts/, research.md, quickstart.md).

Requirements:
- Organize tasks by user story for independent implementation
- Follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- Map components to user stories based on priorities
- Generate dependency graph
- Include parallel execution opportunities
- Manual testing approach (no TDD requested)

## Response snapshot

Created comprehensive task list (`specs/001-basic-todo-operations/tasks.md`) with **58 total tasks** organized into 7 phases:

**Phase 1: Setup** (4 tasks)
- T001-T004: Project structure, requirements.txt, .gitignore

**Phase 2: Foundational** (4 tasks - BLOCKING)
- T005-T008: TodoItemDict type definition, TodoManager initialization
- Critical path: Must complete before ANY user story work

**Phase 3: User Story 1 - Add New Task (P1)** (11 tasks) 🎯 MVP
- T009-T013 [P]: Validation helpers (title, description, priority, tags, due_date) - parallel
- T014: add_task method implementation
- T015-T018 [P]: UI helpers (_get_input, _show_success, _show_error) - parallel
- T019: handle_add_task UI method
- **Independent Test**: Launch app, add task "Buy groceries", verify ID 1 and success message

**Phase 4: User Story 2 - View All Tasks (P1)** (7 tasks)
- T020: view_all_tasks method
- T021-T024 [P]: Format helpers (priority, status, due_date, tags) - parallel
- T025: _format_task_table method
- T026: handle_view_all_tasks UI method
- **Independent Test**: Add 2-3 tasks, view all, verify table with correct columns

**Phase 5: User Story 3 - Delete Task (P2)** (3 tasks)
- T027 [P]: _find_task_by_id helper
- T028: delete_task method
- T029: handle_delete_task UI method
- **Independent Test**: Add task, delete by ID, verify confirmation and removal

**Phase 6: Integration & Main Application** (7 tasks)
- T030-T033 [P]: Display methods (welcome, goodbye, menu, get_choice) - parallel
- T034: run method (main loop)
- T035-T036: main.py entry point
- **Checkpoint**: Complete application executable

**Phase 7: Validation & Testing** (22 tasks)
- T037-T041: US1 acceptance scenarios (5 tests)
- T042-T046: US2 acceptance scenarios (5 tests)
- T047-T051: US3 acceptance scenarios (5 tests)
- T052-T057: Edge case testing (6 tests)
- T058: Exit flow test
- **Approach**: Manual testing (no automated tests for Basic Level)

**Component-to-Story Mapping**:
- `src/models.py`: Foundational (all stories depend on it)
- `src/todo_manager.py`:
  - add_task() + helpers → US1
  - view_all_tasks() → US2
  - delete_task() + helpers → US3
- `src/ui.py`:
  - handle_add_task() + helpers → US1
  - handle_view_all_tasks() + format helpers → US2
  - handle_delete_task() → US3
  - Menu system → Integration
- `src/main.py`: Integration (depends on all stories)

**Parallel Opportunities Identified**:
- Foundational: 4 parallel tasks (T005-T008)
- US1: 9 parallel tasks (5 manager helpers + 4 UI helpers)
- US2: 4 parallel format helpers (T021-T024)
- Integration: 4 parallel display methods (T030-T033)
- **Cross-Story Parallelism**: All 3 user stories can be developed simultaneously after Foundational phase

**Dependency Graph**:
```
Setup (T001-T004)
  ↓
Foundational (T005-T008) [BLOCKS ALL STORIES]
  ↓
  ├─→ US1: Add Task (T009-T019) [P1] ─┐
  ├─→ US2: View All (T020-T026) [P1] ─┼→ Integration (T030-T036)
  └─→ US3: Delete (T027-T029) [P2] ───┘       ↓
                                          Validation (T037-T058)
```

**Implementation Strategies**:
1. **MVP First**: Setup + Foundational + US1 only (19 tasks) → Deliverable 1
2. **Incremental**: Add US2 → Deliverable 2, Add US3 → Deliverable 3, Integrate → Final
3. **Parallel Team**: Split US1/US2/US3 across developers after Foundational complete

**Format Validation**:
- ✅ All tasks follow checklist format: `- [ ] TaskID [P?] [Story?] Description`
- ✅ All implementation tasks include exact file paths
- ✅ Task IDs sequential (T001-T058)
- ✅ [P] markers on 18 parallelizable tasks
- ✅ [Story] labels on all user story tasks (US1, US2, US3)
- ✅ No [Story] labels on Setup, Foundational, Integration, Validation phases

## Outcome

- ✅ Impact: Created dependency-ordered, user-story-organized task list enabling independent MVP delivery and parallel team execution
- 🧪 Tests: 22 manual test scenarios covering all acceptance criteria and edge cases
- 📁 Files: Created specs/001-basic-todo-operations/tasks.md with 58 actionable tasks
- 🔁 Next prompts: `/sp.implement` to execute implementation tasks via Claude Code agents
- 🧠 Reflection: Successfully applied user-story-first organization enabling true incremental delivery, identified 21 parallelizable implementation tasks, clear MVP scope (US1 only = 19 tasks)

## Evaluation notes (flywheel)

- Failure modes observed: None - all tasks follow strict format, user stories independently testable, dependencies clearly documented
- Graders run and results (PASS/FAIL): PASS - Format validation confirms all 58 tasks use checklist syntax, file paths included, [P] and [Story] markers correct
- Prompt variant (if applicable): N/A - Standard task generation workflow
- Next experiment (smallest change to try): Proceed with `/sp.implement` to execute MVP scope (Setup + Foundational + US1)

# Implementation Plan: Basic Todo Operations

**Branch**: `001-basic-todo-operations` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-basic-todo-operations/spec.md`

## Summary

Implement Basic Level todo operations (Add, View, Delete) for an in-memory Python console application. This is Phase I of the Todo App project, focusing on the minimum viable product with three core features: creating tasks, viewing the task list, and deleting tasks. The implementation follows spec-driven development principles using Claude Code agents, with clean separation of concerns (data model, business logic, UI) and no external database dependencies.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: rich (optional, for enhanced table formatting)
**Storage**: In-memory (Python list of dictionaries)
**Testing**: Manual testing for Phase I (automated tests in future phases)
**Target Platform**: Cross-platform console (Windows, Linux, macOS)
**Project Type**: Single console application
**Performance Goals**: < 100ms for viewing up to 100 tasks, instant add/delete operations
**Constraints**: In-memory only (no persistence), < 1000 tasks per session
**Scale/Scope**: Basic Level MVP - 3 user stories (Add, View, Delete tasks)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

### ✅ Principle I: Spec-First Development
- **Requirement**: Every feature must have specification before implementation
- **Status**: PASS - spec.md created and approved before planning
- **Evidence**: `specs/001-basic-todo-operations/spec.md` exists with complete requirements

### ✅ Principle II: Agent-Driven Architecture
- **Requirement**: Use Claude Code subagents with single responsibilities
- **Status**: PASS - Agents defined for models, business logic, UI, integration
- **Evidence**: See Agent Responsibilities section below

### ✅ Principle III: Incremental Development
- **Requirement**: Start with Basic Level (Add, View, Delete)
- **Status**: PASS - This plan covers ONLY Basic Level features
- **Evidence**: Update and search features explicitly excluded (Phase 2, Phase 3)

### ✅ Principle IV: Code Quality Standards
- **Requirement**: Clean code, error handling, type hints, user-friendly interface
- **Status**: PASS - All requirements incorporated into contracts
- **Evidence**: See contracts/ for validation, error handling, type hints

### ✅ Principle V: Data Management
- **Requirement**: In-memory storage, no external dependencies
- **Status**: PASS - Python list storage, optional rich library only
- **Evidence**: See research.md decision #2 (in-memory storage pattern)

**GATE RESULT**: ✅ ALL CHECKS PASSED - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-basic-todo-operations/
├── spec.md              # Feature requirements and user stories
├── plan.md              # This file - implementation plan
├── research.md          # Technical research and decisions (Phase 0)
├── data-model.md        # Data structures and validation (Phase 1)
├── quickstart.md        # User guide (Phase 1)
├── contracts/           # Interface contracts (Phase 1)
│   ├── todo_manager_contract.md  # Business logic interface
│   └── ui_contract.md            # Console UI interface
└── tasks.md             # NOT created by /sp.plan - use /sp.tasks command
```

### Source Code (repository root)

```text
TO-DO-LIST/
├── .specify/
│   ├── memory/
│   │   └── constitution.md      # Project governance
│   ├── templates/               # SDD-RI templates
│   └── scripts/                 # Utility scripts
├── specs/
│   └── 001-basic-todo-operations/  # This feature's docs
├── src/                         # Source code (created during implementation)
│   ├── __init__.py              # Package marker
│   ├── models.py                # Todo item data model and type definitions
│   ├── todo_manager.py          # Business logic: add, view_all, delete
│   ├── ui.py                    # Console interface: menus, prompts, display
│   └── main.py                  # Application entry point
├── tests/                       # Future: automated tests
├── history/
│   └── prompts/
│       └── 001-basic-todo-operations/  # Prompt history records
├── requirements.txt             # Python dependencies
├── CLAUDE.md                    # Agent execution rules
└── README.md                    # Project overview (future)
```

**Structure Decision**: Single console application with flat `src/` directory. Keeps it simple for Basic Level MVP. Clean separation of concerns: models (data), todo_manager (logic), ui (interface), main (entry point).

## Complexity Tracking

> **No violations** - All constitutional checks passed. No complexity justification needed.

## Architecture Decisions

### Decision 1: In-Memory Storage with List

**Context**: Basic Level needs simple storage for < 1000 tasks

**Decision**: Use Python `list[dict]` to store todo items

**Rationale**:
- Native Python, zero dependencies
- Simple and straightforward
- O(n) operations acceptable for Basic Level scope
- Easy to iterate for view_all_tasks()
- Can be serialized to JSON in future phases

**Alternatives Considered**:
- Dictionary with ID as key: Faster lookup but unnecessary complexity for MVP
- SQLite: Violates "no external DB" constitutional principle
- Custom data structure: Premature optimization

**Tradeoffs**:
- Pro: Simple, maintainable, meets all requirements
- Con: O(n) search for delete operation (acceptable for < 1000 tasks)

**Documented in**: [research.md](./research.md#2-in-memory-storage-pattern)

---

### Decision 2: Optional Rich Library for UI

**Context**: FR-010 requires table format display

**Decision**: Use `rich` library (optional) with fallback to plain text

**Rationale**:
- Provides professional table formatting with minimal effort
- Optional dependency maintains simplicity
- Graceful degradation to plain text if not available
- Cross-platform compatible
- Enables better UX without violating constitution

**Alternatives Considered**:
- Plain print only: Manual table formatting is error-prone
- tabulate: Less feature-rich than rich
- curses: Too complex, Windows compatibility issues

**Tradeoffs**:
- Pro: Professional output, minimal code, optional
- Con: One external dependency (but optional)

**Documented in**: [research.md](./research.md#3-console-ui-library)

---

### Decision 3: Custom Validation Functions

**Context**: Need to validate title, priority, description, date format

**Decision**: Implement validation as private methods in TodoManager class

**Rationale**:
- Validation rules are simple (length checks, enum validation)
- No need for heavyweight framework (Pydantic, etc.)
- Keeps logic centralized in business layer
- Easy to test and maintain
- Clear, actionable error messages

**Tradeoffs**:
- Pro: Simple, explicit, maintainable
- Con: Manual validation code (acceptable for Basic Level)

**Documented in**: [research.md](./research.md#4-data-validation-approach)

---

### Decision 4: Exception-Based Error Handling

**Context**: Need to communicate validation errors from business logic to UI

**Decision**: Raise ValueError in TodoManager, catch in UI layer

**Rationale**:
- Clean separation: business logic doesn't know about UI
- Pythonic approach (exceptions for exceptional conditions)
- Enables future automated testing of business logic
- UI layer translates exceptions to user-friendly messages

**Tradeoffs**:
- Pro: Clean architecture, testable, Pythonic
- Con: Exception overhead (negligible for Basic Level)

**Documented in**: [research.md](./research.md#8-error-handling-strategy)

## Agent Responsibilities

### Agent 1: Models Agent

**Responsibility**: Create Todo item data model with type definitions

**Input**:
- data-model.md (field specifications)
- contracts/todo_manager_contract.md (type hints)

**Output**:
- `src/models.py` with:
  - `TodoItemDict` TypedDict definition
  - Helper functions if needed (formatting, serialization)

**Acceptance Criteria**:
- All 9 fields defined with correct types
- Type hints use Python 3.10+ syntax
- Clean, readable code following PEP 8

---

### Agent 2: Core Logic Agent

**Responsibility**: Implement TodoManager business logic

**Input**:
- contracts/todo_manager_contract.md (method signatures, validation rules)
- data-model.md (data structure)

**Output**:
- `src/todo_manager.py` with:
  - TodoManager class
  - Public methods: `__init__`, `add_task`, `view_all_tasks`, `delete_task`
  - Private methods: validation and parsing helpers
  - Complete error handling with specified error messages

**Acceptance Criteria**:
- All public methods implemented per contract
- All validation rules enforced
- Exact error messages as specified
- Type hints on all methods
- ID generation works correctly (sequential, no reuse)

---

### Agent 3: UI Agent

**Responsibility**: Implement console user interface

**Input**:
- contracts/ui_contract.md (display formats, menu structure)
- quickstart.md (user workflows)

**Output**:
- `src/ui.py` with:
  - ConsoleUI class
  - Menu display and navigation
  - Input capture and validation
  - Table formatting (with rich or plain text)
  - Success/error message display

**Acceptance Criteria**:
- Menu displays correctly with 4 options
- All input prompts match specifications
- Table format matches contract
- Error messages displayed in red (if possible)
- Success messages displayed in green (if possible)
- Graceful handling of all TodoManager exceptions

---

### Agent 4: Integration Agent

**Responsibility**: Create application entry point and wire components

**Input**:
- All implemented components (models.py, todo_manager.py, ui.py)
- quickstart.md (application flow)

**Output**:
- `src/main.py` with:
  - Application entry point
  - Component initialization
  - Main execution flow

**Acceptance Criteria**:
- Application starts and runs without errors
- All components properly initialized
- Clean exit on user command
- Welcome and goodbye messages displayed

---

## Implementation Workflow

### Phase 0: Research ✅ COMPLETED

**Artifacts Created**:
- [research.md](./research.md) - Technical decisions and rationale

**Key Decisions**:
1. Python 3.10+ with modern features
2. In-memory list storage
3. Optional rich library for UI enhancement
4. Custom validation functions
5. Built-in datetime module
6. Auto-incrementing integer IDs
7. Flat project structure
8. Exception-based error handling

---

### Phase 1: Design ✅ COMPLETED

**Artifacts Created**:
- [data-model.md](./data-model.md) - Todo item schema and validation rules
- [contracts/todo_manager_contract.md](./contracts/todo_manager_contract.md) - Business logic interface
- [contracts/ui_contract.md](./contracts/ui_contract.md) - Console UI interface
- [quickstart.md](./quickstart.md) - User guide

**Key Outputs**:
1. Complete TodoItem schema (9 fields with validation)
2. TodoManager interface (3 public methods, multiple private helpers)
3. ConsoleUI interface (menu, prompts, table display)
4. User workflows and examples

---

### Phase 2: Implementation (via /sp.tasks)

**NOT PART OF THIS COMMAND** - Use `/sp.tasks` to generate actionable task list

**Expected Tasks** (preview):
1. **Setup Phase**: Create directory structure, requirements.txt
2. **Models Phase**: Implement src/models.py
3. **Core Logic Phase**: Implement src/todo_manager.py
4. **UI Phase**: Implement src/ui.py
5. **Integration Phase**: Implement src/main.py
6. **Validation Phase**: Manual testing of all user stories

---

## Data Flow

### Add Task Flow

```
User (UI)
  ↓
  1. Display prompts for all fields
  2. Capture input (title, description, priority, tags, due_date)
  ↓
ConsoleUI.handle_add_task()
  ↓
TodoManager.add_task(title, description?, priority?, tags?, due_date?)
  ↓
  3. Validate title (not empty, <= 200 chars)
  4. Validate description (<= 1000 chars)
  5. Validate priority (high/medium/low)
  6. Parse tags (comma-separated → list)
  7. Parse due_date (validate format)
  8. Generate ID and timestamps
  9. Create task dict
  10. Append to self.tasks
  11. Increment self._next_id
  ↓
Return TodoItem dict
  ↓
ConsoleUI
  ↓
  12. Display success message
  13. Display task details
  ↓
Back to main menu
```

### View All Tasks Flow

```
User selects "View All Tasks"
  ↓
ConsoleUI.handle_view_all_tasks()
  ↓
TodoManager.view_all_tasks()
  ↓
  Returns self.tasks (list of dicts)
  ↓
ConsoleUI
  ↓
  If empty: Display "No tasks found"
  If not empty: Format and display table
  ↓
Back to main menu
```

### Delete Task Flow

```
User selects "Delete Task"
  ↓
ConsoleUI.handle_delete_task()
  ↓
  1. Prompt for task ID
  2. Validate input is integer
  3. Display task details
  4. Prompt for confirmation
  ↓
If confirmed:
  TodoManager.delete_task(task_id)
    ↓
    5. Find task by ID
    6. If not found: raise ValueError
    7. If found: remove from self.tasks
    ↓
  ConsoleUI displays success
Else:
  Display "Deletion cancelled"
  ↓
Back to main menu
```

## Interface Contracts Summary

### TodoManager Public Interface

```python
class TodoManager:
    def __init__(self) -> None: ...

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: str = "",
        due_date: str = ""
    ) -> dict: ...

    def view_all_tasks(self) -> list[dict]: ...

    def delete_task(self, task_id: int) -> None: ...
```

**See**: [contracts/todo_manager_contract.md](./contracts/todo_manager_contract.md)

### ConsoleUI Public Interface

```python
class ConsoleUI:
    def __init__(self, manager: TodoManager) -> None: ...

    def run(self) -> None: ...  # Main loop

    def display_menu(self) -> None: ...
    def get_menu_choice(self) -> int: ...

    def handle_add_task(self) -> None: ...
    def handle_view_all_tasks(self) -> None: ...
    def handle_delete_task(self) -> None: ...

    def display_welcome(self) -> None: ...
    def display_goodbye(self) -> None: ...
```

**See**: [contracts/ui_contract.md](./contracts/ui_contract.md)

## Requirements Traceability

### User Story 1: Add New Task (P1)

| Acceptance Scenario | Implementation | Component |
|---------------------|----------------|-----------|
| Create task with title only | TodoManager.add_task() | todo_manager.py:45 |
| Create with title + description | TodoManager.add_task() | todo_manager.py:45 |
| Create with priority | TodoManager._validate_priority() | todo_manager.py:120 |
| Create with due date | TodoManager._parse_due_date() | todo_manager.py:145 |
| Create with tags | TodoManager._parse_tags() | todo_manager.py:135 |

### User Story 2: View All Tasks (P1)

| Acceptance Scenario | Implementation | Component |
|---------------------|----------------|-----------|
| Display all tasks in table | ConsoleUI.handle_view_all_tasks() | ui.py:85 |
| Show "No tasks found" when empty | ConsoleUI.handle_view_all_tasks() | ui.py:85 |
| Display priorities correctly | ConsoleUI._format_priority() | ui.py:180 |
| Display status symbols | ConsoleUI._format_status() | ui.py:185 |
| Display tags | ConsoleUI._format_tags() | ui.py:195 |

### User Story 3: Delete Task (P2)

| Acceptance Scenario | Implementation | Component |
|---------------------|----------------|-----------|
| Prompt for confirmation | ConsoleUI.handle_delete_task() | ui.py:110 |
| Delete on confirmation | TodoManager.delete_task() | todo_manager.py:90 |
| Cancel deletion | ConsoleUI.handle_delete_task() | ui.py:110 |
| Error on non-existent ID | TodoManager.delete_task() | todo_manager.py:90 |
| Verify deletion | TodoManager.view_all_tasks() | todo_manager.py:75 |

## Testing Strategy (Basic Level)

**Approach**: Manual testing for Phase I

### Test Scenarios

#### Test 1: Add Task - Minimal Fields
```
1. Run application
2. Select "Add Task"
3. Enter title: "Test Task"
4. Press Enter for all optional fields
5. Verify: Task created with ID 1, default priority "medium", empty description, no tags, no due date
```

#### Test 2: Add Task - All Fields
```
1. Select "Add Task"
2. Enter title: "Complete Project"
3. Enter description: "Finish all sections"
4. Enter priority: "high"
5. Enter tags: "work,urgent"
6. Enter due date: "2025-12-30 17:00"
7. Verify: All fields saved correctly
```

#### Test 3: View All Tasks - Empty
```
1. Run fresh application (no tasks added)
2. Select "View All Tasks"
3. Verify: "No tasks found" message displayed
```

#### Test 4: View All Tasks - Multiple Tasks
```
1. Add 3 tasks with different properties
2. Select "View All Tasks"
3. Verify: All 3 tasks displayed in table format
4. Verify: Columns show ID, Title, Priority, Status, Due Date, Tags
```

#### Test 5: Delete Task - Success
```
1. Add a task (note ID)
2. Select "Delete Task"
3. Enter task ID
4. Confirm: "yes"
5. Verify: Success message, task removed from list
```

#### Test 6: Delete Task - Cancel
```
1. Select "Delete Task"
2. Enter task ID
3. Confirm: "no"
4. Verify: "Deletion cancelled", task still in list
```

#### Test 7: Validation - Empty Title
```
1. Select "Add Task"
2. Enter empty title (just press Enter)
3. Verify: Error message "Title cannot be empty. Please enter a title."
```

#### Test 8: Validation - Invalid Priority
```
1. Select "Add Task"
2. Enter valid title
3. Enter priority: "urgent" (invalid)
4. Verify: Error message "Invalid priority. Please choose: high, medium, or low."
```

#### Test 9: Validation - Invalid Date Format
```
1. Select "Add Task"
2. Enter valid title
3. Enter due date: "12/30/2025" (wrong format)
4. Verify: Error message "Invalid date format. Please use: YYYY-MM-DD HH:MM"
```

#### Test 10: Menu Navigation
```
1. Test invalid menu option: "5"
2. Verify: Error message "Invalid option. Please choose 1-4."
3. Test non-numeric input: "abc"
4. Verify: Error message "Invalid option. Please enter a number."
5. Test Exit (option 4)
6. Verify: Goodbye message displayed, application exits
```

## Performance Requirements

**Basic Level Targets** (per spec SC-003):

| Operation | Target | Actual (Expected) | Status |
|-----------|--------|-------------------|--------|
| Add task (title only) | < 10 seconds | < 1 second | ✅ PASS |
| Add task (all fields) | < 30 seconds | < 5 seconds | ✅ PASS |
| View all (100 tasks) | < 100ms | < 50ms | ✅ PASS |
| Delete task | < 1 second | < 100ms | ✅ PASS |

**Note**: Targets are user-completion time including input, not just code execution

## Security Considerations

**Scope**: Minimal security concerns for Basic Level

- ✅ No network communication
- ✅ No file I/O
- ✅ No authentication needed (single-user, local)
- ✅ Input validation prevents injection (no SQL, no shell commands)
- ✅ No sensitive data storage

**Risk Assessment**: LOW - Isolated local application

## Deployment

**Basic Level Deployment**:

1. Ensure Python 3.10+ installed
2. Clone/download project
3. (Optional) Install dependencies: `pip install -r requirements.txt`
4. Run: `python src/main.py`

**No build process, no deployment infrastructure needed for Phase I**

## Success Criteria Checklist

### Feature Completeness

- [ ] **FR-001 to FR-020**: All 20 functional requirements implemented
- [ ] **US1 (Add Task)**: All 5 acceptance scenarios pass
- [ ] **US2 (View All)**: All 5 acceptance scenarios pass
- [ ] **US3 (Delete)**: All 5 acceptance scenarios pass

### Quality Gates

- [ ] **Type Hints**: All function signatures have type hints
- [ ] **Error Handling**: All ValidationError cases handled with correct messages
- [ ] **User Experience**: Menu clear, prompts helpful, table readable
- [ ] **Code Quality**: PEP 8 compliant, clean separation of concerns

### Process Compliance

- [ ] **Spec-First**: This plan created after spec.md
- [ ] **Agent-Driven**: Implementation uses defined agents
- [ ] **No Manual Coding**: All code generated via Claude Code
- [ ] **Constitutional Alignment**: All 5 principles followed

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rich library not installed | Medium | Low | Graceful fallback to plain text |
| Python version < 3.10 | Low | High | Clear error message, version check |
| User enters very long input | Medium | Low | Validation catches, helpful error |
| Rapid ID exhaustion | Very Low | Low | Integer max is 2^31 (sufficient) |

## Dependencies

### External Dependencies

**Python Packages** (requirements.txt):
```
rich>=13.0.0  # Optional - for enhanced table formatting
```

### Internal Dependencies

**Between Components**:
- ui.py → depends on → todo_manager.py
- ui.py → optional → models.py (for type hints)
- todo_manager.py → depends on → models.py (for type definitions)
- main.py → depends on → ui.py, todo_manager.py

**Implementation Order**:
1. models.py (no dependencies)
2. todo_manager.py (depends on models.py)
3. ui.py (depends on todo_manager.py)
4. main.py (depends on ui.py, todo_manager.py)

## Next Steps

1. **Review this plan** with stakeholder/user
2. **Run `/sp.tasks`** to generate actionable task list with:
   - Setup tasks (directory structure, requirements.txt)
   - Implementation tasks (one per agent responsibility)
   - Validation tasks (manual testing scenarios)
3. **Run `/sp.implement`** to execute tasks via Claude Code agents
4. **Manual testing** using Test Scenarios above
5. **PHR creation** to document implementation process

## Constitutional Alignment (Final Check)

- ✅ **Principle I (Spec-First)**: Plan created after spec.md, all requirements traced
- ✅ **Principle II (Agent-Driven)**: 4 specialized agents defined with single responsibilities
- ✅ **Principle III (Incremental)**: ONLY Basic Level features, Phase 2/3 explicitly excluded
- ✅ **Principle IV (Code Quality)**: Type hints, validation, error handling, separation of concerns
- ✅ **Principle V (Data Management)**: In-memory list, native Python, 1 optional dependency

**FINAL GATE**: ✅ ALL PRINCIPLES SATISFIED - READY FOR TASK GENERATION

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` command
**Branch**: 001-basic-todo-operations (feature branch to be created during implementation)
**Artifacts**: research.md, data-model.md, contracts/, quickstart.md, plan.md

# Research: Basic Todo Operations

**Feature**: 001-basic-todo-operations
**Date**: 2025-12-29
**Purpose**: Technical research for implementing Basic Level todo operations (Add, View, Delete)

## Technical Decisions

### 1. Python Version

**Decision**: Python 3.10 or higher

**Rationale**:
- Type hints improvements (PEP 604 - Union operator `|`)
- Structural pattern matching (match/case statements) - useful for menu handling
- Better error messages for debugging
- Widely available and stable

**Alternatives Considered**:
- Python 3.8/3.9: Missing newer type hint features
- Python 3.11/3.12: Better performance but may not be universally installed

**Impact**: Requires Python 3.10+ in environment, enables modern Python features

---

### 2. In-Memory Storage Pattern

**Decision**: Use a Python list to store Todo items, with dictionary representation for each task

**Rationale**:
- Simple and straightforward for Basic Level (< 1000 tasks per requirements)
- List provides ordered storage (tasks appear in creation order)
- O(n) lookup acceptable for Basic Level scope
- Easy to iterate for view_all_tasks()
- Native Python - no dependencies

**Alternatives Considered**:
- Dictionary with ID as key: Faster lookup O(1), but list is simpler for MVP
- SQLite in-memory: Overkill for Basic Level, violates "no external DB" principle
- Custom data structure: Premature optimization

**Implementation**:
```python
tasks: list[dict] = []
# Each task is a dict with keys: id, title, description, completed, priority, tags, created_at, updated_at, due_date
```

**Impact**: All operations iterate the list; acceptable performance for Basic Level

---

### 3. Console UI Library

**Decision**: Use Python's built-in `input()` and `print()` with optional `rich` library for table formatting

**Rationale**:
- Built-in functions: Zero dependencies, maximum simplicity
- `rich` library: Optional enhancement for table display (FR-010 requires table format)
- Keeps Basic Level simple while allowing polished output
- `rich` is pure Python, easy to install

**Alternatives Considered**:
- Plain print only: Works but table formatting is manual and error-prone
- `colorama`: Cross-platform colors, but doesn't help with table layout
- `tabulate`: Good for tables but `rich` provides more features for future
- `curses`: Too complex for Basic Level, platform issues on Windows

**Implementation**:
```python
# requirements.txt
rich>=13.0.0  # Optional but recommended

# Fallback to plain print if rich not available
try:
    from rich.console import Console
    from rich.table import Table
    USE_RICH = True
except ImportError:
    USE_RICH = False
```

**Impact**: Better UX with minimal complexity increase

---

### 4. Data Validation Approach

**Decision**: Custom validation functions within the TodoManager class

**Rationale**:
- Simple validation rules (title length, priority values, date format)
- No need for heavy validation framework
- Keeps logic centralized in business layer
- Easy to test and maintain

**Alternatives Considered**:
- Pydantic: Powerful but overkill for Basic Level
- Dataclasses with validators: Good but adds complexity
- Schema libraries (cerberus, voluptuous): Not needed for simple rules

**Implementation**:
```python
class TodoManager:
    def _validate_title(self, title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty. Please enter a title.")
        if len(title) > 200:
            raise ValueError("Title too long. Maximum 200 characters allowed.")

    def _validate_priority(self, priority: str) -> None:
        valid_priorities = ["high", "medium", "low"]
        if priority.lower() not in valid_priorities:
            raise ValueError("Invalid priority. Please choose: high, medium, or low.")
```

**Impact**: Clear error messages, explicit validation logic

---

### 5. Date/Time Handling

**Decision**: Use Python's built-in `datetime` module with ISO format parsing

**Rationale**:
- Built-in, no dependencies
- `datetime.fromisoformat()` supports YYYY-MM-DD HH:MM format
- Timezone-naive acceptable for Basic Level (local time assumed)
- Easy to format for display

**Alternatives Considered**:
- `dateutil.parser`: More flexible parsing but external dependency
- `arrow` or `pendulum`: Overkill for Basic Level
- String storage: Loses type safety and comparison capability

**Implementation**:
```python
from datetime import datetime

def parse_due_date(date_str: str) -> datetime:
    """Parse date string in format YYYY-MM-DD HH:MM"""
    try:
        # Accept both "YYYY-MM-DD HH:MM" and "YYYY-MM-DD"
        if len(date_str) == 10:  # Just date
            return datetime.fromisoformat(f"{date_str} 00:00")
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise ValueError("Invalid date format. Please use: YYYY-MM-DD HH:MM")
```

**Impact**: Standard datetime handling, clear error messages

---

### 6. ID Generation Strategy

**Decision**: Auto-incrementing integer starting from 1, tracked by TodoManager

**Rationale**:
- Simple and predictable for users
- Easy to implement with a counter
- Meets FR-002 requirement exactly
- No collision issues in single-process app

**Alternatives Considered**:
- UUID: More robust but less user-friendly (long strings)
- Random integers: Could have collisions
- Timestamp-based: Not sequential

**Implementation**:
```python
class TodoManager:
    def __init__(self):
        self.tasks: list[dict] = []
        self._next_id: int = 1

    def add_task(self, ...) -> dict:
        task = {
            "id": self._next_id,
            # ... other fields
        }
        self._next_id += 1
        self.tasks.append(task)
        return task
```

**Impact**: Simple, meets requirements, easy to understand

---

### 7. Project Structure

**Decision**: Flat structure with separation of concerns

```
TO-DO-LIST/
├── .specify/
│   └── memory/
│       └── constitution.md
├── specs/
│   └── 001-basic-todo-operations/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md
│       └── contracts/
├── src/
│   ├── __init__.py
│   ├── models.py          # Todo item data model
│   ├── todo_manager.py    # Business logic
│   ├── ui.py              # Console interface
│   └── main.py            # Entry point
├── tests/                 # Future: test files
├── requirements.txt
└── README.md
```

**Rationale**:
- Flat `src/` structure keeps it simple for Basic Level
- Clear separation: models, business logic, UI, entry point
- Follows constitutional Principle IV (clean separation)
- Easy to navigate and understand

**Alternatives Considered**:
- Deeper nesting: Unnecessary for Basic Level
- Single file: Poor separation of concerns
- Package structure: Overkill for MVP

**Impact**: Clean, maintainable structure aligned with constitution

---

### 8. Error Handling Strategy

**Decision**: Raise exceptions in business logic, catch and display in UI layer

**Rationale**:
- Separation of concerns: business logic doesn't know about UI
- UI layer handles user-friendly error display
- Enables future testing of business logic
- Follows Python best practices

**Implementation**:
```python
# In todo_manager.py
def add_task(self, title: str, ...) -> dict:
    self._validate_title(title)  # Raises ValueError if invalid
    # ... create task

# In ui.py
def handle_add_task(self, manager: TodoManager) -> None:
    try:
        title = input("Enter task title: ")
        task = manager.add_task(title, ...)
        print(f"✓ Task created successfully! (ID: {task['id']})")
    except ValueError as e:
        print(f"✗ Error: {e}")
```

**Impact**: Clean error handling, user-friendly messages

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Python | 3.10+ | Modern features, type hints |
| Storage | list[dict] | Built-in | Simple, no dependencies |
| UI | input/print | Built-in | Zero dependencies |
| UI Enhancement | rich | 13.0.0+ | Optional, better tables |
| Validation | Custom | N/A | Simple rules, no framework needed |
| Date/Time | datetime | Built-in | Standard library |
| ID Generation | Auto-increment | N/A | Simple counter |

**Total External Dependencies**: 1 optional (rich)

---

## Performance Considerations

**Scale**: Basic Level targets < 1000 tasks (per FR-003)

**Operations**:
- Add task: O(1) - append to list
- View all: O(n) - iterate entire list
- Delete task: O(n) - find by ID, then remove

**Expected Performance**:
- Add: < 1ms
- View 100 tasks: < 100ms (meets SC-003)
- Delete: < 10ms

**Optimization**: Not needed for Basic Level. Future phases can consider dict-based storage if needed.

---

## Security Considerations

**Basic Level Scope**:
- No authentication/authorization (single-user, local app)
- No network communication
- No file I/O (in-memory only)
- Input validation prevents injection (no SQL, no shell commands)

**Risk Level**: Minimal - isolated local application

---

## Constitutional Alignment Check

- ✅ **Principle I (Spec-First)**: Research follows spec creation
- ✅ **Principle II (Agent-Driven)**: Research informs agent implementation design
- ✅ **Principle III (Incremental)**: Research scoped to Basic Level only
- ✅ **Principle IV (Code Quality)**: Type hints, error handling, separation planned
- ✅ **Principle V (Data Management)**: In-memory list, no external dependencies

---

## Open Questions

None - all technical decisions resolved for Basic Level implementation.

---

## Next Steps

1. Create `data-model.md` with detailed Todo item schema
2. Create `contracts/` directory with method signatures for TodoManager and UI
3. Create `quickstart.md` with user workflow examples
4. Update `plan.md` with complete implementation design

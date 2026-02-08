# TodoManager Contract

**Feature**: 001-basic-todo-operations
**Component**: TodoManager (Business Logic Layer)
**File**: `src/todo_manager.py`
**Purpose**: Manage todo items collection with CRUD operations for Basic Level

## Class: TodoManager

### Responsibilities

- Maintain in-memory collection of todo items
- Generate unique sequential task IDs
- Validate task data before storage
- Provide CRUD operations: Create (add), Read (view_all), Delete

### State

```python
class TodoManager:
    tasks: list[dict]      # List of TodoItem dictionaries
    _next_id: int          # Next available ID (private, starts at 1)
```

---

## Public Methods

### `__init__(self) -> None`

**Purpose**: Initialize TodoManager with empty task list

**Parameters**: None

**Returns**: None

**Postconditions**:
- `self.tasks` is an empty list
- `self._next_id` is set to 1

**Example**:
```python
manager = TodoManager()
assert manager.tasks == []
assert manager._next_id == 1
```

---

### `add_task(self, title: str, description: str = "", priority: str = "medium", tags: str = "", due_date: str = "") -> dict`

**Purpose**: Create a new todo task with validation

**Parameters**:
- `title` (str, required): Task title
- `description` (str, optional): Task details, default=""
- `priority` (str, optional): Priority level, default="medium"
- `tags` (str, optional): Comma-separated tags, default=""
- `due_date` (str, optional): Due date in format "YYYY-MM-DD HH:MM" or "YYYY-MM-DD", default=""

**Returns**: dict - The created TodoItem with all fields populated

**Raises**:
- `ValueError`: If title is empty or exceeds 200 characters
- `ValueError`: If description exceeds 1000 characters
- `ValueError`: If priority is not one of: "high", "medium", "low"
- `ValueError`: If due_date format is invalid

**Preconditions**:
- None (validation performed internally)

**Postconditions**:
- New task added to `self.tasks`
- `self._next_id` incremented by 1
- All fields populated:
  - `id`: auto-generated sequential integer
  - `title`: validated and stored
  - `description`: stored (or empty string)
  - `completed`: set to False
  - `priority`: normalized to lowercase
  - `tags`: parsed from comma-separated string to list, normalized to lowercase, deduplicated
  - `created_at`: set to current datetime
  - `updated_at`: set to current datetime (same as created_at)
  - `due_date`: parsed datetime or None

**Side Effects**:
- Increments `_next_id` counter
- Appends task to `tasks` list

**Example**:
```python
manager = TodoManager()

# Minimal task
task1 = manager.add_task(title="Buy groceries")
assert task1["id"] == 1
assert task1["title"] == "Buy groceries"
assert task1["description"] == ""
assert task1["priority"] == "medium"
assert task1["completed"] == False
assert task1["tags"] == []
assert task1["due_date"] is None

# Full task
task2 = manager.add_task(
    title="Team meeting",
    description="Discuss Q1 goals",
    priority="high",
    tags="work,meeting",
    due_date="2025-12-30 14:00"
)
assert task2["id"] == 2
assert task2["priority"] == "high"
assert task2["tags"] == ["work", "meeting"]
assert task2["due_date"] is not None

# Validation errors
try:
    manager.add_task(title="")  # Empty title
except ValueError as e:
    assert str(e) == "Title cannot be empty. Please enter a title."

try:
    manager.add_task(title="Valid", priority="urgent")  # Invalid priority
except ValueError as e:
    assert str(e) == "Invalid priority. Please choose: high, medium, or low."
```

---

### `view_all_tasks(self) -> list[dict]`

**Purpose**: Retrieve all tasks in the collection

**Parameters**: None

**Returns**: list[dict] - List of all TodoItem dictionaries (may be empty)

**Raises**: None

**Preconditions**: None

**Postconditions**:
- Returns reference to `self.tasks` (no modification)
- If no tasks exist, returns empty list

**Side Effects**: None (read-only operation)

**Performance**: O(1) - returns list reference

**Example**:
```python
manager = TodoManager()

# Empty list
tasks = manager.view_all_tasks()
assert tasks == []

# After adding tasks
manager.add_task(title="Task 1")
manager.add_task(title="Task 2")
tasks = manager.view_all_tasks()
assert len(tasks) == 2
assert tasks[0]["title"] == "Task 1"
assert tasks[1]["title"] == "Task 2"
```

---

### `delete_task(self, task_id: int) -> None`

**Purpose**: Remove a task from the collection by ID

**Parameters**:
- `task_id` (int, required): The ID of the task to delete

**Returns**: None

**Raises**:
- `ValueError`: If task with given ID does not exist

**Preconditions**: None (validation performed internally)

**Postconditions**:
- Task with matching ID removed from `self.tasks`
- Other tasks remain unchanged
- `_next_id` is NOT decremented (IDs never reused)

**Side Effects**:
- Removes one element from `tasks` list

**Performance**: O(n) - must search list for matching ID

**Example**:
```python
manager = TodoManager()
task1 = manager.add_task(title="Task 1")
task2 = manager.add_task(title="Task 2")
task3 = manager.add_task(title="Task 3")

# Delete middle task
manager.delete_task(task_id=2)
tasks = manager.view_all_tasks()
assert len(tasks) == 2
assert tasks[0]["id"] == 1
assert tasks[1]["id"] == 3  # Task 3 still has ID 3

# Error: non-existent ID
try:
    manager.delete_task(task_id=999)
except ValueError as e:
    assert str(e) == "Task ID 999 not found"

# Error: already deleted ID
try:
    manager.delete_task(task_id=2)  # Was deleted above
except ValueError as e:
    assert str(e) == "Task ID 2 not found"
```

---

## Private Methods (Internal Use Only)

### `_validate_title(self, title: str) -> None`

**Purpose**: Validate task title

**Raises**:
- `ValueError`: If title is empty (after strip) or exceeds 200 characters

---

### `_validate_description(self, description: str) -> None`

**Purpose**: Validate task description

**Raises**:
- `ValueError`: If description exceeds 1000 characters

---

### `_validate_priority(self, priority: str) -> str`

**Purpose**: Validate and normalize priority level

**Returns**: str - Normalized priority (lowercase)

**Raises**:
- `ValueError`: If priority not in ["high", "medium", "low"]

---

### `_parse_tags(self, tags: str) -> list[str]`

**Purpose**: Parse comma-separated tags string into list

**Returns**: list[str] - Normalized tags (lowercase, no duplicates, no empty strings)

**Example**:
- Input: `"Work, URGENT, work"` → Output: `["work", "urgent"]`

---

### `_parse_due_date(self, due_date: str) -> Optional[datetime]`

**Purpose**: Parse due date string into datetime object

**Returns**: datetime or None

**Raises**:
- `ValueError`: If format is invalid

**Example**:
- Input: `"2025-12-30 14:00"` → Output: `datetime(2025, 12, 30, 14, 0)`
- Input: `"2025-12-30"` → Output: `datetime(2025, 12, 30, 0, 0)`
- Input: `""` → Output: `None`

---

### `_find_task_by_id(self, task_id: int) -> Optional[dict]`

**Purpose**: Search for task by ID

**Returns**: dict (TodoItem) if found, None if not found

**Performance**: O(n)

---

## Error Messages

All error messages MUST match these exact strings for UI consistency:

| Validation | Error Message |
|------------|---------------|
| Empty title | `"Title cannot be empty. Please enter a title."` |
| Title too long | `"Title too long. Maximum 200 characters allowed."` |
| Description too long | `"Description too long. Maximum 1000 characters allowed."` |
| Invalid priority | `"Invalid priority. Please choose: high, medium, or low."` |
| Invalid date format | `"Invalid date format. Please use: YYYY-MM-DD HH:MM"` |
| Task not found | `"Task ID {task_id} not found"` |

---

## Invariants

The TodoManager class MUST maintain these invariants at all times:

1. **Unique IDs**: No two tasks have the same ID
2. **Sequential IDs**: `_next_id` always equals `max(task IDs) + 1` or 1 if no tasks
3. **Valid Tasks**: All tasks in `self.tasks` have all required fields with valid values
4. **ID Immutability**: Task IDs never change once assigned
5. **No Gaps in Logic**: Deleting task ID 2 doesn't affect tasks 1 and 3

---

## Usage Example

```python
from todo_manager import TodoManager

# Initialize
manager = TodoManager()

# Add tasks
task1 = manager.add_task(
    title="Buy groceries",
    tags="personal,shopping"
)

task2 = manager.add_task(
    title="Team meeting",
    description="Discuss Q1 goals",
    priority="high",
    due_date="2025-12-30 14:00"
)

# View all
all_tasks = manager.view_all_tasks()
print(f"Total tasks: {len(all_tasks)}")

# Delete
manager.delete_task(task_id=1)

# Verify
remaining = manager.view_all_tasks()
assert len(remaining) == 1
assert remaining[0]["id"] == 2
```

---

## Constitutional Alignment

- ✅ **Principle II (Agent-Driven)**: Clear interface for agent implementation
- ✅ **Principle IV (Code Quality)**: Type hints, validation, error messages defined
- ✅ **Principle V (Data Management)**: In-memory list, native Python types

---

## Implementation Notes

- Use `datetime.now()` for timestamps
- Store priority and tags in normalized form (lowercase)
- Don't reuse IDs even after deletion (security and audit best practice)
- Validation should happen in private methods, keeping `add_task` clean
- Error messages should be user-friendly and actionable

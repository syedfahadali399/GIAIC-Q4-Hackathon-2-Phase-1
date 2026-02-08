# Data Model: Basic Todo Operations

**Feature**: 001-basic-todo-operations
**Date**: 2025-12-29
**Purpose**: Define data structures and models for Basic Level todo operations

## Todo Item Entity

### Schema

```python
from datetime import datetime
from typing import Optional

TodoItem = {
    "id": int,                      # Unique identifier (auto-generated, sequential)
    "title": str,                   # Task title (required)
    "description": str,             # Task details (optional)
    "completed": bool,              # Completion status
    "priority": str,                # Priority level: "high", "medium", "low"
    "tags": list[str],              # Category labels
    "created_at": datetime,         # Creation timestamp
    "updated_at": datetime,         # Last modification timestamp
    "due_date": Optional[datetime]  # Optional deadline
}
```

### Field Specifications

#### id (int)
- **Type**: Integer
- **Required**: Yes (auto-generated)
- **Constraints**:
  - Positive integer >= 1
  - Unique across all tasks
  - Sequential (auto-incrementing)
- **Generation**: TodoManager maintains `_next_id` counter
- **Example**: `1`, `2`, `3`, ...

#### title (str)
- **Type**: String
- **Required**: Yes
- **Constraints**:
  - Non-empty (after stripping whitespace)
  - Maximum 200 characters
- **Validation**:
  ```python
  if not title or not title.strip():
      raise ValueError("Title cannot be empty. Please enter a title.")
  if len(title) > 200:
      raise ValueError("Title too long. Maximum 200 characters allowed.")
  ```
- **Examples**:
  - `"Buy groceries"`
  - `"Team meeting - Q1 planning"`
  - `"Review PR #123"`

#### description (str)
- **Type**: String
- **Required**: No
- **Default**: `""` (empty string)
- **Constraints**:
  - Maximum 1000 characters
- **Validation**:
  ```python
  if len(description) > 1000:
      raise ValueError("Description too long. Maximum 1000 characters allowed.")
  ```
- **Examples**:
  - `""` (empty)
  - `"Discuss Q1 goals and priorities"`
  - `"Check tests, review code style, approve if all looks good"`

#### completed (bool)
- **Type**: Boolean
- **Required**: Yes
- **Default**: `False`
- **Values**: `True` (completed) or `False` (pending)
- **Display**:
  - `True` → `"✓"` or `"Completed"`
  - `False` → `"✗"` or `"Pending"`
- **Note**: Basic Level creates all tasks as pending; completion functionality is Phase 2

#### priority (str)
- **Type**: String (enumeration)
- **Required**: Yes
- **Default**: `"medium"`
- **Allowed Values**: `"high"`, `"medium"`, `"low"` (case-insensitive input, stored lowercase)
- **Validation**:
  ```python
  valid_priorities = ["high", "medium", "low"]
  if priority.lower() not in valid_priorities:
      raise ValueError("Invalid priority. Please choose: high, medium, or low.")
  priority = priority.lower()  # Normalize to lowercase
  ```
- **Display**: Title case (High, Medium, Low)
- **Examples**: `"high"`, `"medium"`, `"low"`

#### tags (list[str])
- **Type**: List of strings
- **Required**: No
- **Default**: `[]` (empty list)
- **Constraints**:
  - Each tag is a non-empty string
  - Tags are case-insensitive (stored lowercase)
  - No duplicate tags in a single task
- **Input Format**: Comma-separated string → parsed to list
  - Input: `"work,urgent"` → Stored: `["work", "urgent"]`
- **Validation**:
  ```python
  # Input parsing
  if tags_input:
      tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]
      tags = list(set(tags))  # Remove duplicates
  else:
      tags = []
  ```
- **Display**: Comma-separated string
- **Examples**:
  - `[]` (no tags)
  - `["work"]`
  - `["work", "urgent", "meeting"]`

#### created_at (datetime)
- **Type**: datetime object
- **Required**: Yes (auto-generated)
- **Generation**: `datetime.now()` when task is created
- **Format**:
  - Storage: Python datetime object
  - Display: `"YYYY-MM-DD HH:MM:SS"` or `"YYYY-MM-DD"`
- **Example**: `datetime(2025, 12, 29, 14, 30, 0)`
- **Note**: Set once on creation, never modified

#### updated_at (datetime)
- **Type**: datetime object
- **Required**: Yes (auto-generated)
- **Generation**:
  - Initially same as `created_at`
  - Updated to `datetime.now()` on any modification (Phase 2)
- **Format**: Same as created_at
- **Example**: `datetime(2025, 12, 29, 14, 30, 0)`
- **Note**: Basic Level: always equals created_at (no update operation yet)

#### due_date (Optional[datetime])
- **Type**: datetime object or None
- **Required**: No
- **Default**: `None`
- **Input Format**: `"YYYY-MM-DD HH:MM"` or `"YYYY-MM-DD"`
- **Validation**:
  ```python
  if due_date_str:
      try:
          if len(due_date_str) == 10:  # Just date
              due_date = datetime.fromisoformat(f"{due_date_str} 00:00")
          else:
              due_date = datetime.fromisoformat(due_date_str)
      except ValueError:
          raise ValueError("Invalid date format. Please use: YYYY-MM-DD HH:MM")
  else:
      due_date = None
  ```
- **Display**:
  - `None` → `"-"` or `"No deadline"`
  - datetime → `"YYYY-MM-DD HH:MM"`
- **Examples**:
  - `None` (no due date)
  - `datetime(2025, 12, 30, 14, 0, 0)` → Display: `"2025-12-30 14:00"`

---

## TodoManager State

### Schema

```python
class TodoManager:
    tasks: list[dict]      # List of TodoItem dictionaries
    _next_id: int          # Counter for ID generation
```

### Fields

#### tasks (list[dict])
- **Type**: List of dictionaries (each dict is a TodoItem)
- **Initialization**: Empty list `[]`
- **Operations**:
  - Add: `tasks.append(new_task)`
  - View: Iterate entire list
  - Delete: Find by ID, then `tasks.remove(task)`
- **Performance**: O(n) for search, O(1) for append
- **Constraints**:
  - All tasks must have unique IDs
  - Performance target: < 1000 tasks

#### _next_id (int)
- **Type**: Integer (private)
- **Initialization**: `1`
- **Purpose**: Generate unique sequential IDs
- **Usage**:
  ```python
  new_task_id = self._next_id
  self._next_id += 1
  ```
- **Constraints**:
  - Always positive
  - Never decreases
  - Never reuses IDs (even after deletion)

---

## Data Flow

### Add Task Flow

```
User Input (UI)
    ↓
Parse & Validate (UI layer)
    ↓
TodoManager.add_task(title, description?, priority?, tags?, due_date?)
    ↓
    1. Validate title (not empty, <= 200 chars)
    2. Validate description (<= 1000 chars)
    3. Validate priority (high/medium/low)
    4. Parse & validate tags (comma-separated → list)
    5. Parse & validate due_date (format check)
    6. Generate ID (self._next_id)
    7. Generate timestamps (created_at, updated_at)
    8. Create task dict
    9. Append to self.tasks
    10. Increment self._next_id
    ↓
Return task dict
    ↓
Display success & task details (UI layer)
```

### View All Tasks Flow

```
User selects "View All Tasks" (UI)
    ↓
TodoManager.view_all_tasks()
    ↓
    1. Check if tasks list is empty
    2. If empty: return empty list
    3. If not empty: return self.tasks (full list)
    ↓
UI displays table or "No tasks found"
```

### Delete Task Flow

```
User inputs task ID (UI)
    ↓
UI prompts for confirmation
    ↓
If confirmed:
    TodoManager.delete_task(task_id)
        ↓
        1. Search tasks for matching ID
        2. If not found: raise ValueError
        3. If found: remove from self.tasks
        ↓
    Return success
        ↓
    Display success message (UI)
Else:
    Cancel and return to menu
```

---

## Example Data

### Sample TodoItem (All Fields)

```python
{
    "id": 1,
    "title": "Team meeting - Q1 planning",
    "description": "Discuss goals, priorities, and resource allocation for Q1 2025",
    "completed": False,
    "priority": "high",
    "tags": ["work", "meeting", "planning"],
    "created_at": datetime(2025, 12, 29, 10, 0, 0),
    "updated_at": datetime(2025, 12, 29, 10, 0, 0),
    "due_date": datetime(2025, 12, 30, 14, 0, 0)
}
```

### Sample TodoItem (Minimal Fields)

```python
{
    "id": 2,
    "title": "Buy groceries",
    "description": "",
    "completed": False,
    "priority": "medium",
    "tags": [],
    "created_at": datetime(2025, 12, 29, 10, 5, 0),
    "updated_at": datetime(2025, 12, 29, 10, 5, 0),
    "due_date": None
}
```

### Sample TodoManager State

```python
{
    "tasks": [
        {
            "id": 1,
            "title": "Team meeting - Q1 planning",
            "description": "Discuss goals, priorities, and resource allocation",
            "completed": False,
            "priority": "high",
            "tags": ["work", "meeting"],
            "created_at": datetime(2025, 12, 29, 10, 0, 0),
            "updated_at": datetime(2025, 12, 29, 10, 0, 0),
            "due_date": datetime(2025, 12, 30, 14, 0, 0)
        },
        {
            "id": 2,
            "title": "Buy groceries",
            "description": "",
            "completed": False,
            "priority": "medium",
            "tags": [],
            "created_at": datetime(2025, 12, 29, 10, 5, 0),
            "updated_at": datetime(2025, 12, 29, 10, 5, 0),
            "due_date": None
        },
        {
            "id": 3,
            "title": "Review PR #123",
            "description": "Check tests and code style",
            "completed": False,
            "priority": "high",
            "tags": ["work", "code-review"],
            "created_at": datetime(2025, 12, 29, 10, 10, 0),
            "updated_at": datetime(2025, 12, 29, 10, 10, 0),
            "due_date": datetime(2025, 12, 29, 17, 0, 0)
        }
    ],
    "_next_id": 4
}
```

---

## Validation Rules Summary

| Field | Required | Validation Rule | Error Message |
|-------|----------|-----------------|---------------|
| id | Yes (auto) | Positive integer, unique | N/A (auto-generated) |
| title | Yes | Non-empty, <= 200 chars | "Title cannot be empty" / "Title too long. Maximum 200 characters allowed." |
| description | No | <= 1000 chars | "Description too long. Maximum 1000 characters allowed." |
| completed | Yes (default) | Boolean | N/A (always valid) |
| priority | Yes (default) | One of: high, medium, low | "Invalid priority. Please choose: high, medium, or low." |
| tags | No | List of non-empty strings | N/A (parsed from comma-separated) |
| created_at | Yes (auto) | Valid datetime | N/A (auto-generated) |
| updated_at | Yes (auto) | Valid datetime | N/A (auto-generated) |
| due_date | No | Valid datetime format | "Invalid date format. Please use: YYYY-MM-DD HH:MM" |

---

## Storage Considerations

**Basic Level (Phase 1)**:
- In-memory only (list of dicts)
- Data lost on application exit
- No file I/O, no database
- Simple and fast for < 1000 tasks

**Future Phases**:
- Phase 2: Still in-memory (focus on Update/Mark Complete features)
- Phase 3+: Consider file persistence (JSON, pickle, SQLite)
- Data model designed to be serialization-friendly (all fields are JSON-compatible except datetime → can convert to ISO strings)

---

## Type Hints

```python
from datetime import datetime
from typing import Optional, TypedDict

class TodoItemDict(TypedDict):
    """Type definition for TodoItem dictionary"""
    id: int
    title: str
    description: str
    completed: bool
    priority: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
```

---

## Constitutional Alignment

- ✅ **Principle IV (Code Quality)**: Type hints defined, validation rules explicit
- ✅ **Principle V (Data Management)**: In-memory list, native Python data structures, no external dependencies

---

## Next Steps

1. Create contracts/ directory with method signatures
2. Create quickstart.md with user workflow examples
3. Update plan.md with complete implementation design

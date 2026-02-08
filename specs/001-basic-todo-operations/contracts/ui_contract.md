# UI Contract

**Feature**: 001-basic-todo-operations
**Component**: ConsoleUI (User Interface Layer)
**File**: `src/ui.py`
**Purpose**: Console-based user interface for todo application

## Class: ConsoleUI

### Responsibilities

- Display main menu and handle user navigation
- Capture and validate user input
- Format and display task data in readable tables
- Show success and error messages
- Handle graceful application exit

### Dependencies

```python
from todo_manager import TodoManager
from rich.console import Console  # Optional
from rich.table import Table       # Optional
```

---

## Public Methods

### `__init__(self, manager: TodoManager) -> None`

**Purpose**: Initialize console UI with TodoManager dependency

**Parameters**:
- `manager` (TodoManager, required): Instance of TodoManager for business logic

**Returns**: None

**Postconditions**:
- `self.manager` references the provided TodoManager
- `self.running` is set to True
- If `rich` library available, initialize Console

**Example**:
```python
from todo_manager import TodoManager
from ui import ConsoleUI

manager = TodoManager()
ui = ConsoleUI(manager)
```

---

### `run(self) -> None`

**Purpose**: Start the main application loop

**Parameters**: None

**Returns**: None (runs until user exits)

**Behavior**:
1. Display welcome message
2. Loop while `self.running` is True:
   - Display menu
   - Get user choice
   - Execute corresponding action
   - Clear screen or add spacing
3. Display goodbye message on exit

**Side Effects**:
- Reads from stdin (user input)
- Writes to stdout (display)
- Modifies `self.running` when user selects Exit

**Example**:
```python
ui = ConsoleUI(manager)
ui.run()  # Blocks until user exits
```

---

### `display_menu(self) -> None`

**Purpose**: Show main menu options

**Parameters**: None

**Returns**: None

**Output Format**:
```
=== TODO APP - PHASE I ===

1. Add Task
2. View All Tasks
3. Delete Task
4. Exit

Choose option (1-4): _
```

**Example**:
```python
ui.display_menu()
# Displays menu and waits for input
```

---

### `get_menu_choice(self) -> int`

**Purpose**: Capture and validate menu selection

**Parameters**: None

**Returns**: int - Valid menu choice (1-4)

**Behavior**:
- Read user input
- Validate input is an integer
- Validate integer is in range 1-4
- If invalid, show error and prompt again (loop until valid)

**Error Messages**:
- Non-integer input: `"Invalid option. Please enter a number."`
- Out of range: `"Invalid option. Please choose 1-4."`

**Example**:
```python
choice = ui.get_menu_choice()
# User enters "abc" → Error message → Prompts again
# User enters "5" → Error message → Prompts again
# User enters "2" → Returns 2
```

---

### `handle_add_task(self) -> None`

**Purpose**: Guide user through adding a new task

**Parameters**: None

**Returns**: None

**Behavior**:
1. Prompt for title (required)
2. Prompt for description (optional, press Enter to skip)
3. Prompt for priority (optional, default: medium)
4. Prompt for tags (optional, comma-separated)
5. Prompt for due date (optional, format: YYYY-MM-DD HH:MM)
6. Call `manager.add_task()` with inputs
7. If successful: display success message with task details
8. If error: display error message and return to menu

**Prompts**:
```
Enter task title: _
Enter description (optional, press Enter to skip): _
Enter priority (high/medium/low, default: medium): _
Enter tags (comma-separated, optional): _
Enter due date (YYYY-MM-DD HH:MM, optional): _
```

**Success Message**:
```
✓ Task created successfully!

Task Details:
  ID: 1
  Title: Buy groceries
  Description: Get milk, eggs, bread
  Priority: Medium
  Status: Pending
  Tags: shopping, personal
  Due Date: 2025-12-30 18:00
  Created: 2025-12-29 10:00
```

**Error Message** (example):
```
✗ Error: Title cannot be empty. Please enter a title.
```

**Example**:
```python
ui.handle_add_task()
# User is prompted for each field
# Task is created or error is displayed
```

---

### `handle_view_all_tasks(self) -> None`

**Purpose**: Display all tasks in table format

**Parameters**: None

**Returns**: None

**Behavior**:
1. Call `manager.view_all_tasks()`
2. If empty: display "No tasks found"
3. If not empty: display tasks in table format

**Empty State**:
```
No tasks found. Add your first task to get started!
```

**Table Format** (with rich library):
```
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Priority ┃ Status ┃ Due Date       ┃ Tags       ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1  │ Buy groceries  │ Medium   │ ✗      │ 2025-12-30     │ shopping   │
│ 2  │ Team meeting   │ High     │ ✗      │ 2025-12-30     │ work       │
│ 3  │ Review PR      │ High     │ ✗      │ 2025-12-29     │ work, code │
└────┴────────────────┴──────────┴────────┴────────────────┴────────────┘

Total: 3 tasks
```

**Table Format** (without rich, plain text):
```
ID | Title            | Priority | Status | Due Date       | Tags
--------------------------------------------------------------------------------
1  | Buy groceries    | Medium   | ✗      | 2025-12-30     | shopping
2  | Team meeting     | High     | ✗      | 2025-12-30 14  | work
3  | Review PR #123   | High     | ✗      | 2025-12-29 17  | work, code

Total: 3 tasks
```

**Field Display Rules**:
- ID: Integer as-is
- Title: Truncate to 30 chars if longer (append "...")
- Priority: Title case (High, Medium, Low)
- Status: ✓ for completed, ✗ for pending
- Due Date: "YYYY-MM-DD HH:MM" or "-" if None
- Tags: Comma-separated, truncate to 20 chars if longer

**Example**:
```python
ui.handle_view_all_tasks()
# Displays table or "No tasks found"
```

---

### `handle_delete_task(self) -> None`

**Purpose**: Guide user through deleting a task with confirmation

**Parameters**: None

**Returns**: None

**Behavior**:
1. Prompt for task ID
2. Validate ID is an integer
3. Show task details and prompt for confirmation
4. If confirmed: call `manager.delete_task()`
5. If cancelled or error: display message and return

**Prompts**:
```
Enter task ID to delete: _
```

**Confirmation Prompt**:
```
You are about to delete:
  ID: 2
  Title: Team meeting

Are you sure? (yes/no): _
```

**Success Message**:
```
✓ Task ID 2 deleted successfully.
```

**Cancelled Message**:
```
Deletion cancelled.
```

**Error Message** (example):
```
✗ Error: Task ID 999 not found
```

**Validation**:
- If user enters non-integer: `"Invalid ID. Please enter a number."`
- If user enters yes/y/YES/Y: Proceed with deletion
- If user enters no/n/NO/N: Cancel deletion
- If user enters anything else for confirmation: Treat as "no"

**Example**:
```python
ui.handle_delete_task()
# User enters ID: 2
# Confirmation shown
# User confirms: yes
# Task deleted
```

---

### `display_welcome(self) -> None`

**Purpose**: Show welcome message at startup

**Parameters**: None

**Returns**: None

**Output**:
```
╔════════════════════════════════════════╗
║   TODO APP - BASIC LEVEL (PHASE I)    ║
║   Manage your tasks with ease          ║
╚════════════════════════════════════════╝
```

**Example**:
```python
ui.display_welcome()
```

---

### `display_goodbye(self) -> None`

**Purpose**: Show goodbye message on exit

**Parameters**: None

**Returns**: None

**Output**:
```
Thank you for using Todo App!
Goodbye! 👋
```

**Example**:
```python
ui.display_goodbye()
```

---

## Private Methods (Internal Use Only)

### `_format_task_table(self, tasks: list[dict]) -> None`

**Purpose**: Format and display tasks as a table

**Parameters**:
- `tasks` (list[dict]): List of TodoItem dictionaries

**Returns**: None (prints to stdout)

**Behavior**:
- If `rich` available: Use rich.table.Table
- Otherwise: Use plain text formatting with borders

---

### `_format_priority(self, priority: str) -> str`

**Purpose**: Format priority for display

**Returns**: "High", "Medium", or "Low" (title case)

---

### `_format_status(self, completed: bool) -> str`

**Purpose**: Format completion status for display

**Returns**: "✓" if completed, "✗" if pending

---

### `_format_due_date(self, due_date: Optional[datetime]) -> str`

**Purpose**: Format due date for display

**Returns**: "YYYY-MM-DD HH:MM" or "-" if None

---

### `_format_tags(self, tags: list[str], max_length: int = 20) -> str`

**Purpose**: Format tags for display

**Returns**: Comma-separated string, truncated with "..." if needed

---

### `_get_input(self, prompt: str) -> str`

**Purpose**: Generic input helper with prompt

**Returns**: str - User input (stripped)

---

### `_show_error(self, message: str) -> None`

**Purpose**: Display error message in red (if colorization available)

**Output**: `✗ Error: {message}`

---

### `_show_success(self, message: str) -> None`

**Purpose**: Display success message in green (if colorization available)

**Output**: `✓ {message}`

---

## Menu Flow

```
Start
  ↓
Display Welcome
  ↓
┌─→ Display Menu
│   Get Choice (1-4)
│   ↓
│   ├─ 1: Add Task → handle_add_task() → Display result
│   ├─ 2: View All → handle_view_all_tasks() → Display table
│   ├─ 3: Delete → handle_delete_task() → Display result
│   └─ 4: Exit → Set running = False
│   ↓
└─ If running = True, loop back
  ↓
Display Goodbye
  ↓
End
```

---

## Error Handling

All exceptions from TodoManager MUST be caught in UI methods:

```python
def handle_add_task(self) -> None:
    try:
        title = self._get_input("Enter task title: ")
        description = self._get_input("Enter description (optional, press Enter to skip): ")
        # ... more inputs

        task = self.manager.add_task(
            title=title,
            description=description,
            # ... other params
        )

        self._show_success(f"Task created successfully! (ID: {task['id']})")
        # Display task details

    except ValueError as e:
        self._show_error(str(e))
    except Exception as e:
        self._show_error(f"An unexpected error occurred: {e}")
```

---

## Display Standards

### Color Coding (if available)

- Success messages: Green
- Error messages: Red
- Prompts: White/Default
- Headers: Cyan/Blue
- Table borders: Gray

### Symbols

- Success: `✓`
- Error: `✗`
- Pending status: `✗`
- Completed status: `✓`

### Spacing

- Add blank line before menu
- Add blank line after results
- Clear separation between sections

---

## Example Session

```
╔════════════════════════════════════════╗
║   TODO APP - BASIC LEVEL (PHASE I)    ║
║   Manage your tasks with ease          ║
╚════════════════════════════════════════╝

=== TODO APP - PHASE I ===

1. Add Task
2. View All Tasks
3. Delete Task
4. Exit

Choose option (1-4): 1

Enter task title: Buy groceries
Enter description (optional, press Enter to skip): Get milk, eggs, bread
Enter priority (high/medium/low, default: medium):
Enter tags (comma-separated, optional): shopping, personal
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-12-30 18:00

✓ Task created successfully!

Task Details:
  ID: 1
  Title: Buy groceries
  Description: Get milk, eggs, bread
  Priority: Medium
  Status: Pending
  Tags: shopping, personal
  Due Date: 2025-12-30 18:00
  Created: 2025-12-29 10:00

=== TODO APP - PHASE I ===

1. Add Task
2. View All Tasks
3. Delete Task
4. Exit

Choose option (1-4): 2

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Priority ┃ Status ┃ Due Date       ┃ Tags            ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy groceries  │ Medium   │ ✗      │ 2025-12-30 18  │ shopping, per.. │
└────┴────────────────┴──────────┴────────┴────────────────┴─────────────────┘

Total: 1 task

=== TODO APP - PHASE I ===

1. Add Task
2. View All Tasks
3. Delete Task
4. Exit

Choose option (1-4): 4

Thank you for using Todo App!
Goodbye! 👋
```

---

## Constitutional Alignment

- ✅ **Principle II (Agent-Driven)**: Clear interface for UI agent
- ✅ **Principle IV (Code Quality)**: User-friendly messages, error handling, clean prompts
- ✅ **Success Criteria**: Intuitive menu, immediate feedback, clear table format

---

## Implementation Notes

- Use `try/except` blocks for all manager calls
- Input validation happens in UI before calling manager
- Keep UI layer thin - no business logic
- Graceful degradation if `rich` not available
- Cross-platform compatibility (Windows, Linux, Mac)

# Quickstart Guide: Basic Todo Operations

**Feature**: 001-basic-todo-operations
**Date**: 2025-12-29
**Purpose**: User-facing guide for Basic Level todo operations

## Overview

The Todo App (Phase I - Basic Level) allows you to manage your tasks through a simple console interface. You can add tasks, view your task list, and delete completed or unwanted tasks.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Navigate to project directory**:
   ```bash
   cd TO-DO-LIST
   ```

2. **Install dependencies** (optional, for better display):
   ```bash
   pip install -r requirements.txt
   ```

   Note: The app works without dependencies using plain text output. The `rich` library is optional for enhanced table formatting.

3. **Run the application**:
   ```bash
   python src/main.py
   ```

## Quick Start: 3-Minute Workflow

### Step 1: Launch the App

```bash
python src/main.py
```

You'll see the welcome screen and main menu:

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

Choose option (1-4): _
```

### Step 2: Add Your First Task

Enter `1` to add a task:

```
Choose option (1-4): 1

Enter task title: Buy groceries
Enter description (optional, press Enter to skip): Get milk, eggs, and bread
Enter priority (high/medium/low, default: medium):
Enter tags (comma-separated, optional): shopping, personal
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-12-30 18:00

✓ Task created successfully!

Task Details:
  ID: 1
  Title: Buy groceries
  Description: Get milk, eggs, and bread
  Priority: Medium
  Status: Pending
  Tags: shopping, personal
  Due Date: 2025-12-30 18:00
  Created: 2025-12-29 10:00
```

### Step 3: View All Tasks

Enter `2` to view all tasks:

```
Choose option (1-4): 2

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Priority ┃ Status ┃ Due Date       ┃ Tags            ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy groceries  │ Medium   │ ✗      │ 2025-12-30 18  │ shopping, per.. │
└────┴────────────────┴──────────┴────────┴────────────────┴─────────────────┘

Total: 1 task
```

### Step 4: Delete a Task

Enter `3` to delete a task:

```
Choose option (1-4): 3

Enter task ID to delete: 1

You are about to delete:
  ID: 1
  Title: Buy groceries

Are you sure? (yes/no): yes

✓ Task ID 1 deleted successfully.
```

### Step 5: Exit

Enter `4` to exit:

```
Choose option (1-4): 4

Thank you for using Todo App!
Goodbye! 👋
```

## Feature Guide

### Adding Tasks

**Basic Task** (title only):
```
Enter task title: Call dentist
Enter description (optional, press Enter to skip): [Press Enter]
Enter priority (high/medium/low, default: medium): [Press Enter]
Enter tags (comma-separated, optional): [Press Enter]
Enter due date (YYYY-MM-DD HH:MM, optional): [Press Enter]

✓ Task created successfully!
```

**Full Task** (all fields):
```
Enter task title: Team meeting - Q1 planning
Enter description (optional, press Enter to skip): Discuss goals, priorities, and resource allocation
Enter priority (high/medium/low, default: medium): high
Enter tags (comma-separated, optional): work, meeting, planning
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-12-30 14:00

✓ Task created successfully!
```

**Field Guidelines**:

| Field | Required | Format | Example |
|-------|----------|--------|---------|
| Title | Yes | Max 200 characters | "Buy groceries" |
| Description | No | Max 1000 characters | "Get milk, eggs, bread" |
| Priority | No | high/medium/low | "high" or [Enter] for default |
| Tags | No | Comma-separated | "work,urgent" or "work, urgent" |
| Due Date | No | YYYY-MM-DD HH:MM or YYYY-MM-DD | "2025-12-30 14:00" or "2025-12-30" |

### Viewing Tasks

**View All**:
- Shows all tasks in a formatted table
- Displays: ID, Title, Priority, Status, Due Date, Tags
- Status symbols: ✗ = Pending, ✓ = Completed
- Empty list message: "No tasks found. Add your first task to get started!"

**Table Columns**:
- **ID**: Unique task identifier (use this for deletion)
- **Title**: Task name (truncated to 30 chars if longer)
- **Priority**: High / Medium / Low
- **Status**: ✗ (Pending) or ✓ (Completed)
- **Due Date**: Deadline or "-" if none
- **Tags**: Categories/labels or "-" if none

### Deleting Tasks

**Step-by-Step**:
1. View all tasks to see task IDs
2. Select "Delete Task" from menu
3. Enter the task ID
4. Review task details
5. Confirm deletion (yes/no)

**Example**:
```
Enter task ID to delete: 2

You are about to delete:
  ID: 2
  Title: Team meeting - Q1 planning

Are you sure? (yes/no): yes

✓ Task ID 2 deleted successfully.
```

**Cancellation**:
```
Are you sure? (yes/no): no

Deletion cancelled.
```

## Common Scenarios

### Scenario 1: Daily Task List

```bash
# Morning: Add today's tasks
1. Add Task → "Morning standup" (priority: high, due: 2025-12-29 09:00)
2. Add Task → "Review PRs" (tags: work,code-review)
3. Add Task → "Lunch with team" (due: 2025-12-29 12:00)

# Afternoon: Check progress
1. View All Tasks → See all 3 tasks

# Evening: Clean up
1. Delete Task → Remove completed tasks
```

### Scenario 2: Shopping List

```bash
# Create list
1. Add Task → "Buy groceries" (tags: shopping, description: "milk, eggs, bread")
2. Add Task → "Pick up prescription" (tags: shopping,health, priority: high)
3. Add Task → "Return library books" (tags: errands)

# After shopping
1. View All Tasks → Review what's left
2. Delete Task → Remove completed items
```

### Scenario 3: Work Project

```bash
# Plan project tasks
1. Add Task → "Design API endpoints" (priority: high, due: 2025-12-30)
2. Add Task → "Write unit tests" (priority: high, tags: testing)
3. Add Task → "Update documentation" (priority: medium, tags: docs)

# Track progress
1. View All Tasks → See all project tasks
2. Delete Task → Remove completed tasks as you finish
```

## Tips & Best Practices

### Priority Levels

- **High**: Urgent and important (deadlines, critical tasks)
- **Medium**: Default for regular tasks
- **Low**: Nice-to-have, no immediate deadline

### Tags

- Use lowercase for consistency (app normalizes them)
- Keep tags short and meaningful
- Common tags: work, personal, shopping, health, urgent, meeting

### Task Titles

- Keep concise but descriptive
- Good: "Team meeting - Q1 planning"
- Avoid: "Meeting" (too vague)

### Descriptions

- Add context you'll need later
- Include specific details
- Examples:
  - "Discuss Q1 goals, priorities, and resource allocation"
  - "Get milk (2%), eggs (dozen), bread (wheat)"

## Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Title cannot be empty" | Blank title entered | Enter a non-empty title |
| "Title too long. Maximum 200 characters allowed." | Title > 200 chars | Shorten the title |
| "Description too long. Maximum 1000 characters allowed." | Description > 1000 chars | Shorten the description or remove detail |
| "Invalid priority. Please choose: high, medium, or low." | Invalid priority value | Enter: high, medium, or low |
| "Invalid date format. Please use: YYYY-MM-DD HH:MM" | Wrong date format | Use format: 2025-12-30 14:00 |
| "Task ID X not found" | Non-existent or deleted ID | Check task ID with "View All Tasks" |
| "Invalid option. Please choose 1-4." | Invalid menu choice | Enter a number between 1 and 4 |

## Keyboard Shortcuts & Tips

- **Press Enter** to skip optional fields (uses defaults)
- **Ctrl+C** to cancel current operation (returns to menu)
- **Menu Navigation**: Type number (1-4) and press Enter
- **Case Insensitive**: Priority and tags accept any case (high/HIGH/High all work)

## Data Persistence

⚠️ **Important**: Phase I uses **in-memory storage** only.

- Data is lost when you exit the application
- No file saving or database in Basic Level
- Data persistence will be added in future phases

**What This Means**:
- All tasks deleted on exit
- Start fresh each time you run the app
- Perfect for practice and testing
- Future phases will add file persistence

## Troubleshooting

### App Won't Start

**Error**: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
pip install rich
# OR run without rich (plain text mode)
```

**Error**: `python: command not found`

**Solution**: Use `python3` instead:
```bash
python3 src/main.py
```

### Tasks Not Appearing

**Cause**: Tasks only exist during current session (in-memory storage)

**Solution**: Tasks are cleared when you exit. This is expected behavior for Phase I.

### Cannot Delete Task

**Error**: "Task ID X not found"

**Cause**: Task already deleted or ID doesn't exist

**Solution**: Run "View All Tasks" to see current task IDs

## Next Steps

### Phase I (Current - Basic Level)
✅ Add tasks
✅ View all tasks
✅ Delete tasks

### Phase II (Intermediate Level - Coming Soon)
⏳ Update existing tasks
⏳ Mark tasks as complete/incomplete
⏳ Better task management

### Phase III (Advanced Level - Future)
⏳ Search tasks by keyword
⏳ Filter tasks by status, priority, tag
⏳ Sort tasks by various criteria
⏳ File persistence

## Support

For issues or questions:
1. Check the error message and this guide
2. Verify Python version: `python --version` (should be 3.10+)
3. Review the constitutional principles in `.specify/memory/constitution.md`
4. Check specs in `specs/001-basic-todo-operations/`

## Example Complete Session

```bash
$ python src/main.py

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

Enter task title: Finish project report
Enter description (optional, press Enter to skip): Complete sections 3-5
Enter priority (high/medium/low, default: medium): high
Enter tags (comma-separated, optional): work, deadline
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-12-30 17:00

✓ Task created successfully! (ID: 1)

=== TODO APP - PHASE I ===
1. Add Task
2. View All Tasks
3. Delete Task
4. Exit
Choose option (1-4): 1

Enter task title: Buy birthday gift
Enter description (optional, press Enter to skip): For Sarah's birthday party
Enter priority (high/medium/low, default: medium):
Enter tags (comma-separated, optional): personal
Enter due date (YYYY-MM-DD HH:MM, optional): 2025-12-31

✓ Task created successfully! (ID: 2)

=== TODO APP - PHASE I ===
1. Add Task
2. View All Tasks
3. Delete Task
4. Exit
Choose option (1-4): 2

┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ ID ┃ Title                ┃ Priority ┃ Status ┃ Due Date       ┃ Tags        ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1  │ Finish project rep.. │ High     │ ✗      │ 2025-12-30 17  │ work, dea.. │
│ 2  │ Buy birthday gift    │ Medium   │ ✗      │ 2025-12-31     │ personal    │
└────┴──────────────────────┴──────────┴────────┴────────────────┴─────────────┘

Total: 2 tasks

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

**Happy task managing! 🎯**

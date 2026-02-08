# Manual Testing Checklist - Phase 1

This is the checklist I use to verify that everything in the Todo App is working correctly.

## Setup
- [ ] Make sure Python 3.10 or newer is installed.
- [ ] (Optional) Run `pip install rich` to get the better looking tables.
- [ ] Start the app with: `python src/main.py`

---

## 1. Testing "Add Task" (User Story 1)

### Test 1: Simple task with just a title
- [ ] Choose option 1 (Add Task)
- [ ] Type a title like "Buy groceries"
- [ ] Just press Enter for the rest of the fields (description, priority, etc.)
- [ ] **Check:** Should verify it was created with ID 1 and default Medium priority.

### Test 2: Task with title and description
- [ ] Choose option 1
- [ ] Title: "Team meeting"
- [ ] Description: "Discuss goals for Q1"
- [ ] Skip the rest
- [ ] **Check:** Confirm the description shows up in the success message.

### Test 3: Setting a High Priority
- [ ] Choose option 1
- [ ] Title: "Review PR"
- [ ] Set Priority to: high
- [ ] **Check:** Verify the task is created with High priority.

### Test 4: Adding a Due Date
- [ ] Choose option 1
- [ ] Title: "Dentist appointment"
- [ ] Due date: 2025-12-30 14:00
- [ ] **Check:** Make sure the date is saved correctly.

### Test 5: Adding Tags
- [ ] Choose option 1
- [ ] Title: "Project work"
- [ ] Tags: work,urgent
- [ ] **Check:** Verify both tags are added (should look like "work, urgent").

---

## 2. Testing "View Tasks" (User Story 2)

### Test 6: Viewing multiple tasks
- [ ] Make sure there are at least 3 tasks added from the previous steps.
- [ ] Choose option 2 (View All Tasks)
- [ ] **Check:** A table should appear showing ID, Title, Priority, Status, etc. All tasks should be there.

### Test 7: Empty list
- [ ] If the list is empty (delete everything first if needed), choose option 2.
- [ ] **Check:** It should say something like "No tasks found" instead of showing an empty table.

### Test 8: Checking Priorities
- [ ] Add tasks with different priorities (High, Medium, Low).
- [ ] Choose option 2.
- [ ] **Check:** Verify that the priorities are capitalized correctly (High, Medium, Low).

### Test 9: Status Symbol
- [ ] View the tasks.
- [ ] **Check:** Since we haven't completed them, they should all show the ✗ symbol.

### Test 10: Tags display
- [ ] View the tasks again.
- [ ] **Check:** Ensure the tags look readable (comma separated).

---

## 3. Testing "Delete Task" (User Story 3)

### Test 11: Delete confirmation
- [ ] Pick a task ID to delete.
- [ ] Choose option 3 (Delete Task).
- [ ] Enter the ID.
- [ ] **Check:** Ideally it should ask "Are you sure?" before actually deleting it.

### Test 12: Confirming deletion
- [ ] Try deleting a task and type "yes" when asked.
- [ ] **Check:** Should say "Task deleted successfully".
- [ ] Verify it's gone by viewing the list again.

### Test 13: Cancelling deletion
- [ ] Try to delete another task but type "no" this time.
- [ ] **Check:** Should say "Deletion cancelled".
- [ ] Verify the task is STILL there.

### Test 14: Deleting a fake ID
- [ ] Try to delete a task ID that doesn't exist (like 999).
- [ ] **Check:** Should show an error saying the ID wasn't found.

### Test 15: Delete logic check
- [ ] Explain: If I have IDs 1, 2, and 3, and I delete #2...
- [ ] Check that 1 and 3 are still there.

---

## 4. Edge Cases & Errors

### Test 16: Empty title
- [ ] Try to add a task but hit Enter without typing a title.
- [ ] **Check:** Should get an error saying title is required.

### Test 17: Weird priority
- [ ] Add a task and type "super urgent" for priority.
- [ ] **Check:** Should error out and ask for High, Medium, or Low.

### Test 18: Bad date format
- [ ] try entering a date like "12/30/25" (wrong format).
- [ ] **Check:** Should ask for YYYY-MM-DD HH:MM format.

### Test 19: Long title
- [ ] Try pasting a super long title (over 200 chars).
- [ ] **Check:** Should get an error about the length.

### Test 20: Long description
- [ ] Same as above but for description (over 1000 chars).
- [ ] **Check:** Should block it.

### Test 21: Bad menu option
- [ ] In the main menu, type "5".
- [ ] **Check:** Should say invalid option.

### Test 22: Exit
- [ ] Choose option 4.
- [ ] **Check:** App should close with a goodbye message.

---

## Summary
Total Tests: 22
Pass/Fail: ___/22

Notes:
- 

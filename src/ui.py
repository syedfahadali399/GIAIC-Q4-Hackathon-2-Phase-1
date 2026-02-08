"""ConsoleUI - User interface for todo application."""

from datetime import datetime
from typing import Optional
from src.todoManager import TodoManager

# Try to import rich for enhanced display, fallback to plain text
try:
    from rich.console import Console
    from rich.table import Table
    USE_RICH = True
except ImportError:
    USE_RICH = False


class ConsoleUI:
    """Console-based user interface for todo application.

    Handles menu display, user input, task display, and error/success messages.
    """

    def __init__(self, manager: TodoManager) -> None:
        """Initialize console UI with TodoManager dependency.

        Args:
            manager: Instance of TodoManager for business logic
        """
        self.manager = manager
        self.running = True

        if USE_RICH:
            self.console = Console()

    def _get_input(self, prompt: str) -> str:
        """Generic input helper with prompt.

        Args:
            prompt: Prompt message to display

        Returns:
            User input (stripped of leading/trailing whitespace)
        """
        return input(prompt).strip()

    def _show_success(self, message: str) -> None:
        """Display success message in green (if colorization available).

        Args:
            message: Success message to display
        """
        if USE_RICH:
            self.console.print(f"✓ {message}", style="bold green")
        else:
            print(f"✓ {message}")

    def _show_error(self, message: str) -> None:
        """Display error message in red (if colorization available).

        Args:
            message: Error message to display
        """
        if USE_RICH:
            self.console.print(f"✗ Error: {message}", style="bold red")
        else:
            print(f"✗ Error: {message}")

    def handle_add_task(self) -> None:
        """Guide user through adding a new task.

        Prompts for all task fields, calls manager.add_task(), and displays result.
        Handles all validation errors with user-friendly messages.
        """
        try:
            # Prompt for all fields
            title = self._get_input("Enter task title: ")
            description = self._get_input("Enter description (optional, press Enter to skip): ")
            priority = self._get_input("Enter priority (high/medium/low, default: medium): ")
            tags = self._get_input("Enter tags (comma-separated, optional): ")
            due_date = self._get_input("Enter due date (YYYY-MM-DD HH:MM, optional): ")

            # Use defaults if empty
            if not priority:
                priority = "medium"

            # Create task
            task = self.manager.add_task(
                title=title,
                description=description,
                priority=priority,
                tags=tags,
                due_date=due_date
            )

            # Display success
            self._show_success(f"Task created successfully! (ID: {task['id']})")
            print("\nTask Details:")
            print(f"  ID: {task['id']}")
            print(f"  Title: {task['title']}")
            if task['description']:
                print(f"  Description: {task['description']}")
            print(f"  Priority: {task['priority'].title()}")
            print(f"  Status: Pending")
            if task['tags']:
                print(f"  Tags: {', '.join(task['tags'])}")
            if task['due_date']:
                print(f"  Due Date: {task['due_date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"  Created: {task['created_at'].strftime('%Y-%m-%d %H:%M')}")
            print()

        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"An unexpected error occurred: {e}")

    def _format_priority(self, priority: str) -> str:
        """Format priority for display.

        Args:
            priority: Priority string (lowercase)

        Returns:
            Priority in title case (High, Medium, Low)
        """
        return priority.title()

    def _format_status(self, completed: bool) -> str:
        """Format completion status for display.

        Args:
            completed: Completion status boolean

        Returns:
            "✓" if completed, "✗" if pending
        """
        return "✓" if completed else "✗"

    def _format_due_date(self, due_date: Optional[datetime]) -> str:
        """Format due date for display.

        Args:
            due_date: Due date datetime or None

        Returns:
            "YYYY-MM-DD HH:MM" or "-" if None
        """
        if due_date is None:
            return "-"
        return due_date.strftime("%Y-%m-%d %H:%M")

    def _format_tags(self, tags: list[str], max_length: int = 20) -> str:
        """Format tags for display.

        Args:
            tags: List of tags
            max_length: Maximum length before truncation

        Returns:
            Comma-separated string, truncated with "..." if needed
        """
        if not tags:
            return "-"

        tags_str = ", ".join(tags)
        if len(tags_str) > max_length:
            return tags_str[:max_length-3] + "..."
        return tags_str

    def _format_task_table(self, tasks: list[dict]) -> None:
        """Format and display tasks as a table.

        Args:
            tasks: List of TodoItem dictionaries

        Displays table using rich.Table if available, else plain text formatting.
        """
        if USE_RICH:
            # Create rich table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("ID", style="cyan", width=4)
            table.add_column("Title", style="white", width=30)
            table.add_column("Priority", width=10)
            table.add_column("Status", width=8)
            table.add_column("Due Date", width=16)
            table.add_column("Tags", width=20)

            for task in tasks:
                # Truncate title if too long
                title = task['title']
                if len(title) > 30:
                    title = title[:27] + "..."

                table.add_row(
                    str(task['id']),
                    title,
                    self._format_priority(task['priority']),
                    self._format_status(task['completed']),
                    self._format_due_date(task['due_date']),
                    self._format_tags(task['tags'])
                )

            self.console.print(table)
        else:
            # Plain text table
            print("ID | Title                          | Priority   | Status | Due Date         | Tags")
            print("-" * 100)

            for task in tasks:
                # Truncate title if too long
                title = task['title']
                if len(title) > 30:
                    title = title[:27] + "..."

                # Format fields with padding
                print(
                    f"{task['id']:<3} | "
                    f"{title:<30} | "
                    f"{self._format_priority(task['priority']):<10} | "
                    f"{self._format_status(task['completed']):<6} | "
                    f"{self._format_due_date(task['due_date']):<16} | "
                    f"{self._format_tags(task['tags'])}"
                )

    def handle_view_all_tasks(self) -> None:
        """Display all tasks in table format.

        Calls manager.view_all_tasks() and displays results.
        Shows "No tasks found" message if list is empty.
        """
        tasks = self.manager.view_all_tasks()

        if not tasks:
            print("\nNo tasks found. Add your first task to get started!\n")
            return

        print()  # Blank line before table
        self._format_task_table(tasks)
        print(f"\nTotal: {len(tasks)} task{'s' if len(tasks) != 1 else ''}\n")

    def handle_delete_task(self) -> None:
        """Guide user through deleting a task with confirmation.

        Prompts for task ID, shows confirmation, and calls manager.delete_task().
        Handles all validation errors with user-friendly messages.
        """
        try:
            # Prompt for task ID
            task_id_str = self._get_input("Enter task ID to delete: ")

            # Validate input is an integer
            try:
                task_id = int(task_id_str)
            except ValueError:
                self._show_error("Invalid ID. Please enter a number.")
                return

            # Find task to show details before deletion
            task = self.manager._find_task_by_id(task_id)
            if task is None:
                self._show_error(f"Task ID {task_id} not found")
                return

            # Show task details and prompt for confirmation
            print(f"\nYou are about to delete:")
            print(f"  ID: {task['id']}")
            print(f"  Title: {task['title']}")
            print()

            confirmation = self._get_input("Are you sure? (yes/no): ").lower()

            if confirmation in ['yes', 'y']:
                # Delete task
                self.manager.delete_task(task_id)
                self._show_success(f"Task ID {task_id} deleted successfully.")
            else:
                print("\nDeletion cancelled.\n")

        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"An unexpected error occurred: {e}")

    def display_welcome(self) -> None:
        """Show welcome message at startup."""
        print()
        print("╔════════════════════════════════════════╗")
        print("║   TODO APP - BASIC LEVEL (PHASE I)    ║")
        print("║   Manage your tasks with ease          ║")
        print("╚════════════════════════════════════════╝")
        print()

    def display_goodbye(self) -> None:
        """Show goodbye message on exit."""
        print()
        print("Thank you for using Todo App!")
        print("Goodbye! 👋")
        print()

    def display_menu(self) -> None:
        """Show main menu options."""
        print("=== TODO APP - PHASE I ===")
        print()
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Delete Task")
        print("4. Exit")
        print()

    def get_menu_choice(self) -> int:
        """Capture and validate menu selection.

        Returns:
            Valid menu choice (1-4)

        Prompts repeatedly until valid input is received.
        """
        while True:
            try:
                choice = input("Choose option (1-4): ").strip()
                choice_int = int(choice)

                if 1 <= choice_int <= 4:
                    return choice_int
                else:
                    self._show_error("Invalid option. Please choose 1-4.")
            except ValueError:
                self._show_error("Invalid option. Please enter a number.")

    def run(self) -> None:
        """Start the main application loop.

        Displays welcome, then loops: menu → get choice → execute action.
        Continues until user selects Exit (option 4).
        """
        self.display_welcome()

        while self.running:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.handle_add_task()
            elif choice == 2:
                self.handle_view_all_tasks()
            elif choice == 3:
                self.handle_delete_task()
            elif choice == 4:
                self.running = False
                self.display_goodbye()

            # Add spacing between operations (except after exit)
            if self.running:
                print()

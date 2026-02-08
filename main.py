from datetime import datetime
from typing import Optional, TypedDict

class TodoItemDict(TypedDict):
    id: int                      # Unique identifier (auto-generated, sequential)
    title: str                   # Task title (required, max 200 chars)
    description: str             # Task details (optional, max 1000 chars)
    completed: bool              # Completion status (default: False)
    priority: str                # Priority level: "high", "medium", "low"
    tags: list[str]              # Category labels (optional)
    created_at: datetime         # Creation timestamp (auto-generated)
    updated_at: datetime         # Last modification timestamp (auto-generated)
    due_date: Optional[datetime] # Optional deadline


class TodoManager:

    def __init__(self) -> None:
        self.tasks: list[dict] = []
        self._next_id: int = 1

    def _validate_title(self, title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty. Please enter a title.")
        if len(title) > 200:
            raise ValueError("Title too long. Maximum 200 characters allowed.")

    def _validate_description(self, description: str) -> None:
        if len(description) > 1000:
            raise ValueError("Description too long. Maximum 1000 characters allowed.")

    def _validate_priority(self, priority: str) -> str:
        valid_priorities = ["high", "medium", "low"]
        if priority.lower() not in valid_priorities:
            raise ValueError("Invalid priority. Please choose: high, medium, or low.")
        return priority.lower()

    def _parse_tags(self, tags: str) -> list[str]:
        if not tags or not tags.strip():
            return []

        tag_list = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]

        seen = set()
        unique_tags = []

        for tag in tag_list:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags

    def _parse_due_date(self, due_date: str) -> Optional[datetime]:
        if not due_date or not due_date.strip():
            return None

        try:
            if len(due_date.strip()) == 10:  # Just date
                return datetime.fromisoformat(f"{due_date.strip()} 00:00")
            else:
                return datetime.fromisoformat(due_date.strip())
        except ValueError:
            raise ValueError("Invalid date format. Please use: YYYY-MM-DD HH:MM")

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: str = "",
        due_date: str = ""
    ) -> dict:
        self._validate_title(title)
        self._validate_description(description)
        validated_priority = self._validate_priority(priority)
        parsed_tags = self._parse_tags(tags)
        parsed_due_date = self._parse_due_date(due_date)

        now = datetime.now()

        task: dict = {
            "id": self._next_id,
            "title": title.strip(),
            "description": description,
            "completed": False,
            "priority": validated_priority,
            "tags": parsed_tags,
            "created_at": now,
            "updated_at": now,
            "due_date": parsed_due_date
        }

        # Add to list and increment ID
        self.tasks.append(task)
        self._next_id += 1

        return task

    def view_all_tasks(self) -> list[dict]:
        return self.tasks

    def _find_task_by_id(self, task_id: int) -> Optional[dict]:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def delete_task(self, task_id: int) -> None:
        task = self._find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task ID {task_id} not found")

        self.tasks.remove(task)

    def mark_complete(self, task_id: int) -> dict:
        task = self._find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task ID {task_id} not found")

        task["completed"] = True
        task["updated_at"] = datetime.now()

        return task

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> dict:
        task = self._find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task ID {task_id} not found")

        if title is not None:
            self._validate_title(title)
            task["title"] = title.strip()

        if description is not None:
            self._validate_description(description)
            task["description"] = description

        if priority is not None:
            validated_priority = self._validate_priority(priority)
            task["priority"] = validated_priority

        if tags is not None:
            parsed_tags = self._parse_tags(tags)
            task["tags"] = parsed_tags

        if due_date is not None:
            parsed_due_date = self._parse_due_date(due_date)
            task["due_date"] = parsed_due_date

        task["updated_at"] = datetime.now()

        return task


try:
    from rich.console import Console
    from rich.table import Table
    USE_RICH = True
except ImportError:
    USE_RICH = False


class ConsoleUI:

    def __init__(self, manager: TodoManager) -> None:
        self.manager = manager
        self.running = True

        if USE_RICH:
            self.console = Console()

    def _get_input(self, prompt: str) -> str:
        return input(prompt).strip()

    def _show_success(self, message: str) -> None:
        if USE_RICH:
            self.console.print(f"✓ {message}", style="bold green")
        else:
            print(f"✓ {message}")

    def _show_error(self, message: str) -> None:
        if USE_RICH:
            self.console.print(f"✗ Error: {message}", style="bold red")
        else:
            print(f"✗ Error: {message}")

    def handle_add_task(self) -> None:
        try:
            # Prompt for all fields
            title = self._get_input("Enter task title: ")
            description = self._get_input("Enter description (optional, press Enter to skip): ")
            priority = self._get_input("Enter priority (high/medium/low, default: medium): ")
            tags = self._get_input("Enter tags (comma-separated, optional): ")
            due_date = self._get_input("Enter due date (YYYY-MM-DD HH:MM, optional): ")

            if not priority:
                priority = "medium"

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
        return priority.title()

    def _format_status(self, completed: bool) -> str:
        return "✓" if completed else "✗"

    def _format_due_date(self, due_date: Optional[datetime]) -> str:
        if due_date is None:
            return "-"
        return due_date.strftime("%Y-%m-%d %H:%M")

    def _format_tags(self, tags: list[str], max_length: int = 20) -> str:
        if not tags:
            return "-"

        tags_str = ", ".join(tags)
        if len(tags_str) > max_length:
            return tags_str[:max_length-3] + "..."
        return tags_str

    def _format_task_table(self, tasks: list[dict]) -> None:
        if USE_RICH:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("ID", style="cyan", width=4)
            table.add_column("Title", style="white", width=30)
            table.add_column("Priority", width=10)
            table.add_column("Status", width=8)
            table.add_column("Due Date", width=16)
            table.add_column("Tags", width=20)

            for task in tasks:
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
            print("ID | Title                          | Priority   | Status | Due Date         | Tags")
            print("-" * 100)

            for task in tasks:
                title = task['title']
                if len(title) > 30:
                    title = title[:27] + "..."

                print(
                    f"{task['id']:<3} | "
                    f"{title:<30} | "
                    f"{self._format_priority(task['priority']):<10} | "
                    f"{self._format_status(task['completed']):<6} | "
                    f"{self._format_due_date(task['due_date']):<16} | "
                    f"{self._format_tags(task['tags'])}"
                )

    def handle_view_all_tasks(self) -> None:
        tasks = self.manager.view_all_tasks()

        if not tasks:
            print("\nNo tasks found. Add your first task to get started!\n")
            return

        print() 
        self._format_task_table(tasks)
        print(f"\nTotal: {len(tasks)} task{'s' if len(tasks) != 1 else ''}\n")

    def handle_delete_task(self) -> None:
        try:
            task_id_str = self._get_input("Enter task ID to delete: ")

            try:
                task_id = int(task_id_str)
            except ValueError:
                self._show_error("Invalid ID. Please enter a number.")
                return

            task = self.manager._find_task_by_id(task_id)
            if task is None:
                self._show_error(f"Task ID {task_id} not found")
                return

            print(f"\nYou are about to delete:")
            print(f"  ID: {task['id']}")
            print(f"  Title: {task['title']}")
            print()

            confirmation = self._get_input("Are you sure? (yes/no): ").lower()

            if confirmation in ['yes', 'y']:
                self.manager.delete_task(task_id)
                self._show_success(f"Task ID {task_id} deleted successfully.")
            else:
                print("\nDeletion cancelled.\n")

        except ValueError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"An unexpected error occurred: {e}")

    def display_welcome(self) -> None:
        print()
        print("==========================================")
        print("   TODO APP - BASIC LEVEL (PHASE I)    ")
        print("   Manage your tasks with ease          ")
        print("==========================================")
        print()

    def display_goodbye(self) -> None:
        print()
        print("Thank you for using Todo App!")
        print("Goodbye!")
        print()

    def display_menu(self) -> None:
        print("=== TODO APP - PHASE I ===")
        print()
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Delete Task")
        print("4. Exit")
        print()

    def get_menu_choice(self) -> int:
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

            if self.running:
                print()


def main() -> None:
    manager = TodoManager()

    ui = ConsoleUI(manager)

    ui.run()


if __name__ == "__main__":
    main()

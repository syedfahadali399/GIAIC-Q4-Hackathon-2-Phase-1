from datetime import datetime
from typing import Optional
from src.models import TodoItemDict


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

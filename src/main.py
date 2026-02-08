from src.todoManager import TodoManager
from src.ui import ConsoleUI


def main() -> None:
    manager = TodoManager()

    ui = ConsoleUI(manager)

    ui.run()


if __name__ == "__main__":
    main()

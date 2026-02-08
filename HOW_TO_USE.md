# How to Run the App

Here is a quick guide on how to use the Todo Application.

## Getting Started

1. **Open your terminal** (Command Prompt on Windows or Terminal on Mac/Linux).
2. **Go to the project folder:**
   ```bash
   cd C:\Users\hamza\Desktop\TO-DO-PHASE-01-
   ```
   *(Note: Make sure this path matches where you actually put the folder)*

3. **Run the app:**
   ```bash
   python src/main.py
   ```

---

## How it Works

The app has a simple menu. Just type the number you want and hit Enter.

### 1. Adding a Task
- Choose option `1`.
- Type a title for your task (this is the only thing required).
- You can add a description, priority, tags, and due date if you want, or just press **Enter** to skip them.
- **Tip:** For priority, you can just type `h`, `m`, or `l` instead of typing out "high", "medium", or "low".

### 2. Viewing Tasks
- Choose option `2`.
- This shows a table with all your tasks.
- If you installed `rich` (see below), it will look nicer with colors and borders.
- Check the **ID** number here if you want to delete a task later.

### 3. Deleting a Task
- Choose option `3`.
- Enter the ID of the task you want to remove.
- It will ask "Are you sure?" - type `yes` to confirm.

### 4. Exiting
- Choose option `4` to close the program.

---

## Common Issues / Troubleshooting

**"Python is not recognized"**
- Try using `python3 src/main.py` instead.
- Make sure you installed Python and checked the "Add to PATH" box during installation.

**"ModuleNotFoundError: No module named 'rich'"**
- The app uses a library called `rich` for the nice tables.
- You can install it by running: `pip install rich`
- If you don't want to install it, the app should still work but won't look as cool.

**"File not found"**
- Make sure you are in the right folder. Type `dir` (Windows) or `ls` (Mac/Linux) to see if `src` is there.

---

## Shortcuts
- **Ctrl+C**: Force quit if it gets stuck.
- **Up Arrow**: In the terminal, this brings back the last command you typed.

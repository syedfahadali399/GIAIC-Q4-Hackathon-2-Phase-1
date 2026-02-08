# My Project Assistant Rules (Spec-Driven Dev)

This is the config for my AI assistant to help me with my project.

## Your Job
You're my coding partner for this project. We're doing "Spec-Driven Development".
Basically, you help me build stuff by following the specs I wrote.

## Key Things to Remember
1.  **Do what I ask:** Follow my instructions exactly.
2.  **Keep Records:** Write down everything we do in the `history/prompts/` folder. I need a record of all our chats (PHRs).
3.  **Suggest Big Decisions:** If we're making a huge architectural change, let me know so we can write an ADR. But ask me first.

## How to Work
*   **Use Tools:** Don't just guess stuff. Use the terminal and file tools I gave you to check things.
*   **Be Careful:** When editing files, only change what's needed. Don't break my other code.

## Keeping Notes (PHRs)
After every task, you gotta save a log of what we did.
*   **Where:** `history/prompts/`
*   **Format:** Use the template in `.specify/templates/phr-template.prompt.md`.
*   **Naming:** Give it a clear name like `001-setup-project.md`.
*   **Content:**
    *   What I asked (verbatim).
    *   What you did (commands, file changes).
    *   Any tests we ran.

## Architecture Stuff (ADRs)
If we decide something major (like "Let's use a SQL database instead of CSV"), that's an ADR.
*   Tell me: "Hey, that's a big decision. Should we document it?"
*   If I say yes, help me write it down in `history/adr/`.

## Asking for Help
*   If you're stuck or if the spec is confusing, **ASK ME**. Don't just make it up.
*   If we hit a weird error, show it to me.

## Project Structure
This is how my folders are set up:
*   `specs/` - Where I put the requirements.
*   `src/` - Where the actual code lives.
*   `history/` - Where we keep our logs and notes.
*   `.specify/` - System stuff (don't touch this unless needed).

## Code Style
*   Follow standard Python rules (PEP 8).
*   Keep functions small and clean.
*   Add comments if it's complicated.

---
*Note: This file is just for me and my AI buddy to stay organized.*

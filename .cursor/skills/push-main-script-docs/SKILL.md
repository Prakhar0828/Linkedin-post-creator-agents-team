---
name: push-main-script-docs
description: >-
  Before pushing this repository to GitHub, audits and completes docstrings on
  the root main entry script (main.py): module docstring and every user-defined
  function. Use when the user asks to push, commit and push, publish to GitHub,
  ship to origin, or explicitly asks to fix or add documentation on main.py.
---

# Push gate — document `main.py`

## When this applies

Run this workflow **before** `git commit` / `git push` when the user (or the push-quality rule) is shipping this repo, **and** whenever they ask to align or add documentation on the primary entry script.

## Entry script

Default target: repository root **`main.py`**. If the project’s documented entrypoint is a different file, use that file instead and note it in the commit message.

## Checklist

1. Open the entry script and list **user-defined** `def` / `async def` names (ignore third-party re-exports if any).
2. **Module docstring** — If missing or stale (wrong CLI vs prompts, wrong outputs), add or update a short top-of-file string: one line purpose, how it is run (`python main.py`), and that the crew writes outputs per task config (e.g. `linkedin_post.md` when applicable).
3. **Function docstrings** — For each user-defined function (including `main`):
   - One-line summary.
   - `Args` / `Returns` / `Raises` only when non-obvious; for `main()` that only prompts and calls `kickoff`, describe side effects (stdin prompts, crew execution, printed result) instead of empty Args.
4. **Style** — Prefer concise Google-style or NumPy-style blocks consistent with the rest of the file. Do not document every agent literal; keep focus on public entry behavior.
5. If documentation is already complete and accurate, **say so** in the reply and still run the rest of the push checklist (README, tests, etc.) from `github-deploy-quality-prep`.

## Anti-patterns

- Do not replace working logic just to “add docs.”
- Do not paste API keys or env values into docstrings.
- Do not add huge narrative docstrings to every small block; the module + `main()` are the priority for this repo.

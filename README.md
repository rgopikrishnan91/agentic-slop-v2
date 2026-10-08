# Task 1 rerun (Claude run): orchestration workspace

- `package/`: the handover package as received (unchanged).
- `log/`: orchestrator log (sessions, dispatched and reported models, script runs).
- `work/`: outputs collected from role sessions and script outputs.

Each role session runs in a fresh cloud session on its own branch `orch/<step>-<role>[-<family>]`, which holds only that session's clean folder.

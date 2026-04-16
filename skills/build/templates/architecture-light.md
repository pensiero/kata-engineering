# Architecture Template — Light Tier

Scaffold for `ARCHITECTURE.md` in light-tier projects. Keep it short. The narrative principle still applies — order by understanding dependency — but a simple project needs only a few sections.

Copy the content inside the code block below and adapt it to the project. Everything outside the code block is guidance for the agent, not part of the output.

---

```markdown
---
project_tier: light
---

# [Project Name]

## The Story

[A few sentences of prose. Define what this IS, not what it does — who is it for, why does it exist. Write it so that someone encountering this project for the first time knows immediately whether they're in the right place.]

## How It Works

[Brief description of how the code is organized and what the key pieces are. For a simple project, this might be a paragraph and a tree view. The reader should know where to look for what.]

```
project/
  src/             # [what's here]
  tests/           # [what's here]
  ARCHITECTURE.md  # This file
```

## The Decisions

[Record non-obvious choices. Why this language, this library, this approach. One or two entries is fine. Future-you will thank you.]

- [Decision and rationale]

## Working With This Project

```bash
# How to run
[command]

# How to test
[command]
```
```

---

## Notes for the agent

- This doc exists and describes the project clearly
- Tests exist and pass (at minimum: happy path)
- No formal contracts required
- If complexity grows beyond what this doc can describe, upgrade to standard tier

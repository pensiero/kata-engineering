# Light Tier — Architecture Template

Use this as a guide for light-tier projects. Keep it short. The narrative principle still applies — order by understanding dependency — but a simple project needs only a few sections.

---

```markdown
---
project_tier: light
---

# [Project Name]

## What This Is

[A few sentences of prose. What does this do, why does it exist, who is it for. Write it so that someone encountering this project for the first time knows immediately whether they're in the right place.]

## How It Works

[Brief description of how the code is organized and what the key pieces are. For a simple project, this might be a paragraph and a tree view. The reader should know where to look for what.]

```
project/
  src/           # [what's here]
  tests/         # [what's here]
```

## Decisions

[Record non-obvious choices. Why this language, this library, this approach. One or two entries is fine. Future-you will thank you.]

- [Decision and rationale]

## Running

```bash
# How to run
[command]

# How to test
[command]
```
```

---

## Light tier expectations

- This doc exists and describes the project clearly
- Tests exist and pass (at minimum: happy path)
- No formal contracts required
- If complexity grows beyond what this doc can describe, upgrade to standard tier

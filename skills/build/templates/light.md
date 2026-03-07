# Light Tier — Architecture Template

Use this as a guide when bootstrapping a light-tier project. Adapt to the project — don't copy verbatim.

---

```markdown
---
project_tier: light
---

# [Project Name]

[One or two sentences: what this is and why it exists.]

## Structure

[Brief description of how code is organized. For simple projects, a few lines is enough.]

```
project/
  src/           # Source code
  tests/         # Tests
  README.md
  ARCHITECTURE.md
```

## Key Decisions

[Record non-obvious choices. Why this language/library/approach? Future-you will thank you.]

- [Decision 1 and rationale]
- [Decision 2 and rationale]

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

- Tests exist and pass (at minimum: happy path)
- Architecture doc describes what the project is and how it's organized
- No formal contracts or invariants required — this is a lightweight project
- If complexity grows, upgrade to standard tier

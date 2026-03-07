# Coding Rules

Read this before writing code.

---

## First Principle

The simplest solution that works is not a compromise — it is the goal.

Complexity is debt. Every abstraction, every indirection, every extra file is a choice to make the system harder to understand. Sometimes that cost is justified. Usually it isn't.

Before adding anything, ask: does this earn its existence? Not "could this be useful someday" — but does the system need this, right now, to work correctly?

A well-built system has a natural shape. When you find it, the code feels inevitable — like it couldn't have been written any other way. When you miss it, you feel the friction: things that should be simple aren't, names that should be obvious aren't, changes that should be local aren't.

Seek the natural shape. Remove what obscures it.

---

## Before You Write Code

### Understand the scope
- Read the project's `ARCHITECTURE.md` and `CONTRACTS.md` (or equivalent)
- Understand what you're changing and what boundaries exist around it
- If the task has a contract (`{TASK}_CONTRACT.md`), read it — it defines when you're done

### Clarify before implementing
- If the task scope is ambiguous, ask NOW — not after building the wrong thing
- If you're unsure which approach to take, research FIRST in a separate step
- Do not mix exploration with implementation — decide the approach, then build with clean focus

### After context compaction
- Re-read the task scope and the files most relevant to your current work
- Do not rely on memory of what you read earlier — verify by re-reading

---

## While Writing Code

### Minimal changes
- Do the least that solves the problem
- Touch the fewest files possible
- Every line you add is a line someone must maintain

### No premature abstraction
- Do not create abstractions until you have two concrete use cases
- No base classes for single implementations
- No interfaces/protocols for single consumers
- No configuration systems where a constant would do
- If you're building it "for future flexibility" — stop. Build it when the future arrives

### Schema-first
- Define data structures (types, schemas, interfaces) BEFORE implementing logic
- If data flows through a boundary (API, storage, module interface), define its shape explicitly
- Schemas are contracts — they make boundaries visible and testable

### Follow existing patterns
- Read similar code in the project before writing new code
- Match naming conventions, file organization, and style exactly
- If the project uses a pattern, follow it — even if you'd prefer a different one
- If you believe the existing pattern is wrong, say so and propose a migration — don't create a second pattern

### Keep files focused
- One concern per file
- If a file does two unrelated things, split it
- If a function is hard to name, it probably does too much

### Write tests alongside code
- See `rules/testing.md` for testing practices
- Tests are not a follow-up task — they're part of writing the code
- If you can't test it, the design is probably wrong

---

## After Writing Code

### Verify before declaring done
- Run the project's existing test suite — all tests must pass
- Run any new tests you wrote
- If the project has named invariants in `CONTRACTS.md`, verify each one that your changes could affect

### System-wide impact check
Before declaring a task complete, ask yourself:

1. **What fires when this runs?** Callbacks, middleware, hooks, event handlers — trace at least two levels from your change
2. **Can failure leave broken state?** If you persist state before calling something that can fail, what happens on failure? Is retry safe?
3. **What other interfaces expose this?** Alternative entry points, similar APIs, shared mixins. If parity is needed, add it now
4. **Do error strategies align?** Retry logic + fallback + framework error handling — do they conflict?

Skip this check only for leaf-node changes with no callbacks, no state persistence, and no parallel interfaces.

### Co-evolve documentation
- If your changes affect architecture or boundaries, update `ARCHITECTURE.md` in the same commit
- If your changes add, remove, or modify an invariant, update `CONTRACTS.md` in the same commit
- Code and docs ship together — no silent drift

### Commit discipline
- Commit when a logical unit is complete and tests pass
- Commit message describes a complete, valuable change — not "WIP" or "partial X"
- Stage only files related to the logical unit — not `git add .`

---

## Anti-Stagnation

### Two-strike rule
If your current approach has failed twice, **stop**. Do not retry the same approach.

1. State what failed and why
2. List at least 3 alternative approaches with tradeoffs
3. Recommend one, explain why
4. Wait for approval before proceeding

### Challenge your own assumptions
- Is there a simpler way to do this?
- Am I adding complexity because it's needed, or because it's interesting?
- Would a new person understand this without explanation?

---

## Context Discipline

### Load only what you need
- Don't read every project file during orient — read architecture docs and the files relevant to your task
- Don't carry exploration context into implementation — if you researched alternatives, start fresh for the build

### Stay focused on the goal
- Every change should trace back to the stated task
- If you discover something unrelated that needs fixing, note it — don't fix it now
- Scope creep is the silent killer of quality

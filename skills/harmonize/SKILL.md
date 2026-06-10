---
name: harmonize
description: Sweep the project's filenames and folder layout for product-readability. Form independent assumptions first, then propose or apply renames that survive a fresh-eyes test.
---

# Harmonize Skill

Use to make the repo legible to someone who knows the **product** but not the implementation. Names should map to product concepts, not to engineering verbs or historical accidents.

NOT for: refactoring code internals, changing public APIs, restructuring modules for runtime reasons. This skill only touches names, paths, imports, and the docs that reference them.

---

## Modes

```
PROPOSE   → produce a plan only, no renames applied
APPLY     → execute renames, update imports + doc refs, verify tests
REVIEW    → fresh-eyes pass over a plan or applied diff produced by another agent
```

Always start in PROPOSE if you have not yet earned the user's trust on naming choices. The plan is the cheap object — the rename is the expensive one.

---

## Workflow

### Step 1 — Build independent assumptions FIRST

Before reading any prior plan, prior agent output, or commit message that proposes renames:

1. List the source tree at depth 4. Note file sizes.
2. For each top-level domain area (e.g. `engine/`, `intake/`, `studio/`), open 1–3 anchor files to ground yourself in what the product actually does.
3. Form your own rename list, grouped by:
   - **High value** — name actively misleads or undersells what the file owns.
   - **Medium value** — generic but harmless; rename only if it materially improves clarity.
   - **Splits/regroups** — file owns two distinct concerns; consider splitting OR renaming to acknowledge plurality.
   - **Leave alone** — already aligned with product language.

Write this list down before reading anyone else's. Otherwise you will anchor on their framing and lose the fresh-eyes signal that makes this skill valuable.

### Step 2 — Compare with prior work (REVIEW mode only)

If a prior agent produced a plan or applied a diff:

- Where do you agree? Note it briefly — that is signal that the choice was sound.
- Where do you disagree? State the disagreement with reasoning, not just preference.
- Where did the prior agent miss something? Common gaps:
  - Test files renamed inconsistently with their source
  - Imports updated, comments not (provenance notes like `extracted from X`, headers that name the file)
  - Build/test scripts (e.g. `package.json`, `Makefile`) referencing old paths
  - Stale references in docs (`CONTRACTS.md`, `ARCHITECTURE.md`, test-suite indices)
  - Decisions silently dropped that the user explicitly approved in plan comments
- Where did the prior agent over-reach? If user comments pushed back on splits or folder regrouping, respect that signal.

### Step 3 — Apply naming principles

1. **Product nouns over engineering verbs.** `mutation-applier.ts` beats `applier.ts`. `deployed-artifacts.ts` beats `artifacts.ts`.
2. **Avoid catch-all names.** `judge.ts`, `studio-write.ts`, `helpers.ts` undersell what the file owns.
3. **Keep canonical product terms** even if they sound technical — these are the words the team uses.
4. **Asymmetry is OK.** A frontend file may take the UI tab name (`progress.js`) while the backend keeps the domain term (`convergence.ts`). Document the asymmetry.
5. **Plurality matters.** A file with three distinct evaluators is `evaluators.ts`, not `judge.ts`. A file that writes two different artifact families is `*-writes.ts`, not `*-write.ts`.
6. **Don't force consistency.** Renaming every file to match a pattern is churn, not clarity.

### Step 4 — Anti-patterns

Watch for and resist:

- **Microfile trap.** Splitting a 150-line file with 3 functions into 3 files. For LLM-navigated repos this raises navigation cost without raising clarity. Compromise: rename the single file to acknowledge plurality.
- **Thin folders.** Creating `foo/` to hold one file. If grouping by folder would yield only 1–2 files, prefer a suffix on the filename instead (`foo-bar.ts`).
- **Backwards-compat renames.** Adding aliases or re-exports "for safety" — just update the imports and move on.
- **Doc-only echoes.** Renaming a file but leaving its old name in `CONTRACTS.md`, `package.json`, ownership headers, or test-suite indices.
- **Over-naming.** `runtime-deploy-service.ts` adds nothing if there is only one deploy service in the directory. Length without disambiguation is noise.

### Step 5 — Apply (APPLY mode only)

For each rename, in this order:

1. `git mv <old> <new>` — preserves history.
2. Grep for the old basename across source, config, and doc files (adjust extensions to the project's languages). Update every import, script reference, doc mention, and comment.
3. If the file is a test, also update test-runner scripts (e.g. `package.json`) and any test-suite index doc.
4. If a comment in the file mentions it by name (e.g. `extracted from X.ts`), update those references too.
5. Run the test suite. Tests must pass before commit.
6. If the rename uncovered stale docs (e.g. references to a concept that no longer exists in code), clean those in the same pass — but **separately confirm** with the user if the staleness is non-trivial.

### Step 6 — Output

In PROPOSE mode, produce a `FILE_NAMING_AND_ORGANIZATION_PLAN.md` (or similar) with:

- One-sentence recommendation up top.
- Naming principles you applied.
- Tables grouped by High value / Medium value / Splits / Leave alone.
- Explicit list of what you would NOT do, with reasoning.
- Sequencing — which renames first, which last, which depend on user judgement calls.

In APPLY mode, end with:
- Summary of renames executed (old → new).
- List of files whose imports/refs were updated.
- Test result.
- Any decisions deferred to the user (e.g. "deploy-service.ts kept as-is because no ambiguity in the directory").

In REVIEW mode, end with:
- Where you agreed with the prior agent.
- Where you disagreed and why.
- Gaps you found that the prior agent missed.
- Recommended next actions.

---

## Verifying the cleanup is real

After APPLY, this grep should return nothing relevant:

```bash
grep -rn "<old-basename>" --include="*.ts" --include="*.js" --include="*.json" --include="*.md" -n . \
  | grep -v node_modules | grep -v .git/
```

Adjust the `--include` patterns to the project's languages and build files.

If anything returns, the rename is incomplete.

Also run the project's test command. A passing test suite is the minimum bar — type checks alone will not catch broken script paths in `package.json`.

---

## Principles

### Fresh eyes are the product
The whole point of this skill is independent assumptions. If you read a prior plan first, you cannot un-read it. Form your view, write it down, **then** compare.

### Names are interfaces
A filename is a contract with the next reader. A bad filename costs every reader who opens the directory listing — including the LLM. Treat naming churn as a real cost, but treat misleading names as a higher one.

### Respect the no-rename
Files already aligned with the product are wins, not gaps. List them explicitly so the user can see the decision was deliberate.

### Anchor in the user's pushback
If the user has commented on a prior plan ("don't split for the sake of microfiles", "this folder would only hold 1 file"), those comments are the strongest signal in the conversation. Apply them as constraints, not suggestions.

### Tests are the safety net
Renames look trivial. They are not. A missed import in a script path can break deploys silently. Always run the test suite before declaring done.

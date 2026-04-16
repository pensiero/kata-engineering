# Skill: kata-init

Initialize a new project or update an existing one with the Kata Engineering framework.

## Usage

Invoke with an absolute path to the target project:

```
/kata-init /absolute/path/to/target-project
```

---

## What Gets Deployed

**From this repo → target project:**

| Source (kata-engineering/) | Destination (target/.claude/) |
|---|---|
| `skills/` | `.claude/skills/` |
| `rules/` | `.claude/rules/` |
| `AGENTS-patch.md` | `CLAUDE.md` (see below) |

---

## Execution

### Step 1 — Resolve paths

- **Source root:** the directory containing this skill file, going up three levels (i.e. the kata-engineering project root)
- **Target root:** the absolute path provided as the argument

Verify the target path exists. If it does not, stop and tell the user.

### Step 2 — Deploy skills

For each directory inside `<source>/skills/`:

1. Check if `<target>/.claude/skills/<skill-name>/` exists
2. If it does **not** exist: copy the entire skill directory as-is
3. If it **does** exist: replace it entirely (skills are replaced 1:1 — they have no per-project customisation)

Create `<target>/.claude/skills/` if it does not exist.

### Step 3 — Deploy rules

For each file inside `<source>/rules/`:

1. Check if `<target>/.claude/rules/<filename>` exists
2. If it does **not** exist: copy it
3. If it **does** exist: replace it entirely (rules are also replaced 1:1)

Create `<target>/.claude/rules/` if it does not exist.

### Step 4 — Patch CLAUDE.md

The content from `AGENTS-patch.md` is injected into the target's `CLAUDE.md` inside a clearly delimited block:

```
<!-- KATA-ENGINEERING:START -->
...content from AGENTS-patch.md (excluding the first comment block at the top)...
<!-- KATA-ENGINEERING:END -->
```

The "first comment block" to exclude is the lines from the top of `AGENTS-patch.md` starting with `#` and `>` that explain what the file is — only inject the content starting from `---` onwards.

**If `<target>/CLAUDE.md` does not exist:**
Create it with only the marked block.

**If `<target>/CLAUDE.md` exists and already contains the markers:**
Replace only the content between `<!-- KATA-ENGINEERING:START -->` and `<!-- KATA-ENGINEERING:END -->` (inclusive of the markers) with the fresh injected block. Leave everything else in the file untouched.

**If `<target>/CLAUDE.md` exists but has no markers:**
Append the marked block to the end of the file, preceded by a blank line.

### Step 5 — Report

Print a summary:
- Which skills were added vs updated
- Which rules were added vs updated
- What happened to CLAUDE.md (created / markers updated / block appended)
- Any files skipped or errors

---

## Notes

- Never modify files outside `<target>/.claude/` and `<target>/CLAUDE.md`
- Do not overwrite `<target>/.claude/settings.json` or `<target>/.claude/settings.local.json` if they exist
- If the target project is the kata-engineering project itself, stop and tell the user

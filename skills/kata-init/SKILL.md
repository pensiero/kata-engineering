---
name: kata-init
description: Initialize this computer with the Kata Engineering framework for Codex and/or Claude.
---

# Skill: kata-init

Initialize this computer with the Kata Engineering framework for Codex and/or Claude.

## Usage

Invoke from the cloned `kata-engineering` repository:

```
/kata-init
```

If the user names a specific agent, configure only that agent. Otherwise,
configure every supported agent that appears to be installed on the machine.

---

## Supported Agents

| Agent | Global skills directory | Global instruction file |
|---|---|---|
| Codex | `~/.codex/skills` | `~/.codex/AGENTS.md` |
| Claude | `~/.claude/skills` | `~/.claude/CLAUDE.md` |

The same repository files are used for both agents:

| Source (kata-engineering/) | Destination |
|---|---|
| `skills/kata-init/` | `<global-skills-dir>/kata-init` |
| `skills/build/` | `<global-skills-dir>/build` |
| `skills/review/` | `<global-skills-dir>/review` |
| `skills/project-kickoff/` | `<global-skills-dir>/project-kickoff` |
| `skills/harmonize/` | `<global-skills-dir>/harmonize` |
| `skills/knowledgebase-kickoff/` | `<global-skills-dir>/knowledgebase-kickoff` |
| `AGENTS-patch.md` | loaded from the global instruction file (mechanism differs per agent — see Step 4) |

Do not copy Kata skills or rules into individual projects. Global symlinks make
every project read the latest version from this repository.

---

## Execution

### Step 1 - Resolve source root

Resolve the Kata Engineering repository root dynamically. Use the current
working directory when it is the repository root; otherwise locate the nearest
parent directory containing `AGENTS-patch.md`, `skills/`, and `rules/`.

In shell examples, use:

```bash
KATA_ENGINEERING_HOME="$(pwd -P)"
```

Do not hardcode user-specific absolute paths in reusable repo instructions.

### Step 2 - Select target agents

Configure:

- Codex if the user requested Codex or `~/.codex` exists
- Claude if the user requested Claude or `~/.claude` exists
- both if both global directories exist

If neither agent directory exists and the user did not specify an agent, ask
which agent to configure.

### Step 3 - Create skill symlinks

For each selected agent, create its global skills directory if needed.

For each selected agent (`<dir>` is `~/.codex` or `~/.claude`):

```bash
mkdir -p <dir>/skills
for s in kata-init build review project-kickoff harmonize knowledgebase-kickoff; do
  ln -sfn "$KATA_ENGINEERING_HOME/skills/$s" <dir>/skills/$s
done
```

If a destination already exists as a real file or directory (not a symlink),
move it to a timestamped backup under the agent's backup directory before
creating the symlink:

- Codex backups: `~/.codex/backups/`
- Claude backups: `~/.claude/backups/`

Do not delete existing user content.

### Step 4 - Patch global instruction files

The loading mechanism differs per agent. Claude Code expands `@path` includes
natively; Codex does not (open feature request: openai/codex#6038), so a bare
`@path` line in `~/.codex/AGENTS.md` is inert text. Never use the `@` include
form for Codex.

**Claude** — add this include line to `~/.claude/CLAUDE.md` exactly once:

```md
@${KATA_ENGINEERING_HOME}/AGENTS-patch.md
```

Edits to `AGENTS-patch.md` are picked up automatically on the next session.

**Codex** — paste the full content of `AGENTS-patch.md` into
`~/.codex/AGENTS.md` between managed markers, prefixed with the resolved
repository root so relative rule paths can be resolved:

```md
<!-- BEGIN KATA ENGINEERING (managed by kata-init — do not edit between markers) -->
Kata Engineering home: ${KATA_ENGINEERING_HOME}

...content of AGENTS-patch.md...
<!-- END KATA ENGINEERING -->
```

If the markers already exist, replace everything between them with the current
content. If an old bare `@.../AGENTS-patch.md` line exists, remove it — it does
nothing in Codex. Because the content is pasted, edits to `AGENTS-patch.md`
reach Codex only when `kata-init` is re-run — remind the user of this in the
final report.

For both agents: create the global instruction file if it does not exist.
Preserve all existing content. Do not add duplicate global instructions such
as RTK if they are already configured.

### Step 5 - Report

Print a summary:

- Which agents were configured
- Which skill symlinks were created or refreshed
- Which existing directories were backed up, if any
- Whether each global instruction file was updated or already current (Claude: include line; Codex: marker block)
- For Codex: remind the user that future `AGENTS-patch.md` edits require re-running `kata-init`

---

## Notes

- Project-level `AGENTS.md` and `CLAUDE.md` files should stay focused on
  project-specific constraints.
- `AGENTS-patch.md` resolves rule files from the Kata Engineering repository
  root, so projects do not need local copies of `rules/`.

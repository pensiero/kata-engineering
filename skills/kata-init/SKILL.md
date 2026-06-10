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

| Agent | Global skills directory | Global instruction file (legacy cleanup only) |
|---|---|---|
| Codex | `~/.codex/skills` | `~/.codex/AGENTS.md` |
| Claude | `~/.claude/skills` | `~/.claude/CLAUDE.md` |

Setup is symlinks only — global instruction files are never patched. Skills
route themselves through their descriptions and point to the central `rules/`.
Every skill directory under `skills/` is symlinked into each agent's global
skills directory under its own name.

Do not copy Kata skills or rules into individual projects. Global symlinks make
every project read the latest version from this repository.

---

## Execution

### Step 1 - Resolve source root

Resolve the Kata Engineering repository root dynamically. Use the current
working directory when it is the repository root; otherwise locate the nearest
parent directory containing both `skills/` and `rules/`.

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
for s in "$KATA_ENGINEERING_HOME"/skills/*/; do
  ln -sfn "${s%/}" <dir>/skills/"$(basename "$s")"
done
```

Every skill in the repository is linked — new skills added to the repository
are picked up on the next `kata-init` run. Verify with `file`, not `ls`:
macOS Finder aliases look like files and are not followed by agents.

If a destination already exists as a real file or directory (not a symlink),
move it to a timestamped backup under the agent's backup directory before
creating the symlink:

- Codex backups: `~/.codex/backups/`
- Claude backups: `~/.claude/backups/`

Do not delete existing user content.

### Step 4 - Clean up legacy wiring

Earlier versions of Kata Engineering patched global instruction files with an
`AGENTS-patch.md` routing section. That file no longer exists — skills route
themselves. If present, remove these leftovers:

- In `~/.claude/CLAUDE.md`: any `@.../kata-engineering/AGENTS-patch.md` include line
- In `~/.codex/AGENTS.md`: any block between `<!-- BEGIN KATA ENGINEERING ... -->`
  and `<!-- END KATA ENGINEERING -->` markers, and any bare
  `@.../kata-engineering/AGENTS-patch.md` line

Remove only the Kata leftovers. Preserve all other content in those files.

### Step 5 - Report

Print a summary:

- Which agents were configured
- Which skill symlinks were created or refreshed
- Which existing directories were backed up, if any
- Which legacy wiring was removed from global instruction files, if any

---

## Notes

- Project-level `AGENTS.md` and `CLAUDE.md` files should stay focused on
  project-specific constraints.
- Skills resolve `rules/` from the Kata Engineering repository root (two
  levels above their real, symlink-resolved location), so projects do not
  need local copies of `rules/`.

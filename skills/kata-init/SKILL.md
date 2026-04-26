# Skill: kata-init

Initialize this computer with the Kata Engineering framework for Codex and/or
Claude.

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
| `AGENTS-patch.md` | included from the global instruction file |

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

For Codex:

```bash
mkdir -p ~/.codex/skills
ln -sfn "$KATA_ENGINEERING_HOME/skills/kata-init" ~/.codex/skills/kata-init
ln -sfn "$KATA_ENGINEERING_HOME/skills/build" ~/.codex/skills/build
ln -sfn "$KATA_ENGINEERING_HOME/skills/review" ~/.codex/skills/review
ln -sfn "$KATA_ENGINEERING_HOME/skills/project-kickoff" ~/.codex/skills/project-kickoff
```

For Claude:

```bash
mkdir -p ~/.claude/skills
ln -sfn "$KATA_ENGINEERING_HOME/skills/kata-init" ~/.claude/skills/kata-init
ln -sfn "$KATA_ENGINEERING_HOME/skills/build" ~/.claude/skills/build
ln -sfn "$KATA_ENGINEERING_HOME/skills/review" ~/.claude/skills/review
ln -sfn "$KATA_ENGINEERING_HOME/skills/project-kickoff" ~/.claude/skills/project-kickoff
```

If a destination already exists as a real directory, move it to a timestamped
backup under the agent's backup directory before creating the symlink:

- Codex backups: `~/.codex/backups/`
- Claude backups: `~/.claude/backups/`

Do not delete existing user content.

### Step 4 - Patch global instruction files

For each selected agent, add this include exactly once:

```md
@${KATA_ENGINEERING_HOME}/AGENTS-patch.md
```

Target files:

- Codex: `~/.codex/AGENTS.md`
- Claude: `~/.claude/CLAUDE.md`

Create the global instruction file if it does not exist. Preserve all existing
content. Do not add duplicate global instructions such as RTK if they are
already configured.

### Step 5 - Report

Print a summary:

- Which agents were configured
- Which skill symlinks were created or refreshed
- Which existing directories were backed up, if any
- Whether each global instruction file was updated or already contained the include

---

## Notes

- Project-level `AGENTS.md` and `CLAUDE.md` files should stay focused on
  project-specific constraints.
- `AGENTS-patch.md` resolves rule files from the Kata Engineering repository
  root, so projects do not need local copies of `rules/`.

# AI Agent Toolkit

A collection of powerful agent skills for task automation and orchestration. This repository follows the [Agent Skills](https://agentskills.io) open standard.

## About This Repository

This repository contains skills that extend AI agent capabilities for handling complex workflows. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata.

## Skill Sets

| Skill | Description |
|-------|-------------|
| [distributed-task-orchestrator](./skills/distributed-task-orchestrator) | Decompose complex tasks into parallel sub-agents |
| [scheduled-task](./skills/scheduled-task) | Create and manage scheduled tasks with Claude CLI |

## Try in Claude Code

You can register this repository as a Claude Code Plugin marketplace:

```bash
/plugin marketplace add YOUR_GITHUB_USERNAME/ai-agent-toolkit
```

Then install the skills:

```bash
/plugin install agent-skills@ai-agent-toolkit
```

## Directory Structure

```
ai-agent-toolkit/
├── .claude-plugin/
│   └── marketplace.json       # Plugin marketplace configuration
├── skills/
│   ├── distributed-task-orchestrator/
│   │   ├── SKILL.md           # Main skill file (required)
│   │   ├── references/        # Reference documentation
│   │   └── ...
│   └── scheduled-task/
│       ├── SKILL.md           # Main skill file (required)
│       ├── scripts/           # Executable scripts
│       └── references/        # Reference documentation
└── README.md
```

## Creating New Skills

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here]

## Examples
- Example usage 1
- Example usage 2
```

The frontmatter requires:
- `name` - A unique identifier (lowercase, hyphens for spaces, max 64 chars)
- `description` - What the skill does and when to use it (max 1024 chars)

Optional fields:
- `license` - License name or reference
- `compatibility` - Environment requirements
- `metadata` - Additional key-value pairs

For more details, see [Agent Skills Specification](https://agentskills.io/specification).

## License

Apache-2.0

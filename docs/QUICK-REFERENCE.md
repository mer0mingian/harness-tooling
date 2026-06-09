# Quick Reference: Plugins & Extensions

## What Gets Installed

```
┌─────────────────────┬──────────────┬─────────────────────────────────────┐
│ Module              │ Type         │ Claude Code Slash Commands          │
├─────────────────────┼──────────────┼─────────────────────────────────────┤
│ harness-agents      │ Plugin       │ NONE (agents only)                  │
│                     │              │ → @test-specialist                  │
│                     │              │ → @dev-specialist                   │
│                     │              │ → @arch-specialist                  │
│                     │              │ → @review-specialist                │
│                     │              │ → @qa-specialist                    │
├─────────────────────┼──────────────┼─────────────────────────────────────┤
│ matd (plugin)       │ Plugin       │ /matd-test                          │
│                     │              │ /matd-implement                     │
│                     │              │ /matd-review                        │
│                     │              │ /matd-commit                        │
│                     │              │ /matd-update-docs                   │
│                     │              │ /matd-specify-product-brief         │
│                     │              │ /matd-specify-adr                   │
│                     │              │ /matd-specify-solution-design       │
│                     │              │                                     │
│                     │              │ → @matd-orchestrator                │
│                     │              │ → @matd-architect                   │
│                     │              │ → @matd-qa                          │
│                     │              │ → @matd-dev                         │
│                     │              │ → @matd-specifier                   │
│                     │              │ → @matd-critical-thinker            │
├─────────────────────┼──────────────┼─────────────────────────────────────┤
│ matd (extension)    │ Extension    │ /speckit.matd.test                  │
│                     │ (SpecKit)    │ /speckit.matd.implement             │
│                     │              │ /speckit.matd.review                │
│                     │              │ /speckit.matd.commit                │
│                     │              │ /speckit.matd.update-docs           │
│                     │              │ /speckit.matd.specify-product-brief │
│                     │              │ /speckit.matd.specify-adr           │
│                     │              │ /speckit.matd.specify-solution-design│
│                     │              │                                     │
│                     │              │ (Only if SpecKit initialized)       │
└─────────────────────┴──────────────┴─────────────────────────────────────┘
```

## Installation Commands

```bash
# harness-agents plugin
claude plugin install harness-agents --scope project

# matd plugin
claude plugin install matd --scope project

# matd extension (requires SpecKit)
specify init . --integration claude --force
specify extension add matd --dev ./harness-tooling/speckit-extensions/matd
```

## When You Type...

```
/matd-test feat-123
└─→ matd PLUGIN command
    └─→ Spawns @matd-qa agent internally
        └─→ Writes failing tests

/speckit.matd.test feat-123
└─→ matd EXTENSION command (SpecKit variant)
    └─→ Uses SpecKit templates + .specify/ artifacts
        └─→ Same workflow, different artifact format

@test-specialist
└─→ harness-agents agent
    └─→ Direct agent spawn (no workflow)

@matd-qa
└─→ matd plugin agent
    └─→ Direct agent spawn (or used by /matd-* commands)
```

## Most Common Setup

```bash
# For most users (Claude Code + optional SpecKit)
claude plugin install matd --scope project

# Result:
# ✓ /matd-test, /matd-implement, etc.
# ✓ @matd-architect, @matd-qa, etc.
```

## Full Installation (Everything)

```bash
# All agents + all commands + SpecKit
claude plugin install harness-agents --scope project
claude plugin install matd --scope project
specify init . --integration claude --force
specify extension add matd --dev ./speckit-extensions/matd

# Result:
# ✓ @test-specialist, @dev-specialist, etc. (harness-agents)
# ✓ @matd-*, /matd-* (matd plugin)
# ✓ /speckit.matd.* (matd extension)
```

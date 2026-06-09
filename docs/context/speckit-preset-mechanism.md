# SpecKit Preset Mechanism

## Source
Grilling session 2026-06-09
SpecKit research findings on command override mechanism

## Context
The SpecKit extension needs to override default SpecKit commands with MATD-specific implementations. Understanding the preset mechanism ensures clean override without conflicts.

## Details

### Priority-Based Resolution

SpecKit resolves commands using priority order:
1. **Project extensions** (highest priority)
2. **Preset extensions** (middle priority)
3. **Core SpecKit** (lowest priority)

When multiple sources provide the same command, highest priority wins.

### Override Syntax

**In extension.yml:**
```yaml
commands:
  - name: specify
    description: "MATD-specific specification workflow"
    replaces: "speckit.specify"  # Override core command
    script: ./commands/specify.sh
```

**Key field: `replaces`**
- Value format: `"<namespace>.<command>"`
- Examples:
  - `"speckit.specify"` - Override core specify command
  - `"speckit.plan"` - Override core plan command
  - `"speckit.implement"` - Override core implement command

### Installation with Priority

**Project-level (priority 3):**
```bash
specify extension add /workspace/submodules/harness-tooling/spec-kit-multi-agent-tdd --priority 3
```

**Preset-level (priority 4):**
```bash
specify extension add /workspace/presets/matd --priority 4
```

### Use Cases

**MATD Extension:**
- Overrides `specify`, `plan`, `implement` with multi-agent workflows
- Installed at project priority (3) to ensure precedence
- Core SpecKit commands become fallback (not removed)

**Team Preset:**
- Company-specific templates and conventions
- Installed at preset priority (4)
- Overridden by project-level customizations

## References
- SpecKit Documentation: https://github.com/speckit/speckit (if applicable)
- MATD Extension: /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/spec-kit-multi-agent-tdd/
- Extension Structure: /home/minged01/repositories/test/harness-sandbox-stony/SPECKIT_EXTENSION_STRUCTURE.md

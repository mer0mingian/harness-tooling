# SpecKit Extension Patterns

**Source:** spec-kit watching repo (synthesized 2026-06-10)
**Purpose:** Quick reference for MATD extension development

## Key Patterns

- **Manifest schema**: `extension.yml` with schema_version 1.0, strict validation rules
- **Naming convention**: Extension ID `^[a-z0-9-]+$`, commands `^speckit\.[a-z0-9-]+\.[a-z0-9-]+$`
- **Directory structure**: Self-contained in `.specify/extensions/{id}/` with commands/, scripts/, docs/
- **Command format**: Universal Markdown with YAML frontmatter, converted to agent-specific formats
- **Configuration layers**: defaults → project → local → env vars (precedence order)
- **Hook system**: Before/after hooks with priority ordering (lower number = runs first)
- **Catalog system**: Dual catalog (default + community), multi-catalog stack with priority
- **Multi-agent support**: Single universal format → 15+ agent formats (Claude, Copilot, Gemini, etc.)

## Extension Manifest Structure

### Minimal Valid Manifest

```yaml
schema_version: "1.0"

extension:
  id: "my-ext"                    # Required: ^[a-z0-9-]+$
  name: "My Extension"            # Required
  version: "1.0.0"                # Required: semantic version
  description: "Brief description" # Required
  author: "Author Name"           # Required
  repository: "https://github.com/author/spec-kit-my-ext" # Required
  license: "MIT"                  # Required

requires:
  speckit_version: ">=0.1.0"      # Required: version specifier

provides:
  commands:
    - name: "speckit.my-ext.cmd"  # Required: at least one
      file: "commands/cmd.md"     # Required
      description: "Command desc" # Required
```

### Full Manifest Fields

Source: `extensions/EXTENSION-API-REFERENCE.md`

```yaml
schema_version: "1.0"

extension:
  id: string                      # ^[a-z0-9-]+$
  name: string
  version: string                 # X.Y.Z
  description: string             # <200 chars
  author: string
  repository: string              # Valid URL
  license: string                 # SPDX identifier
  homepage: string                # Optional, valid URL

requires:
  speckit_version: string         # ">=X.Y.Z", ">=X.Y.Z,<Y.0.0"
  tools:                          # Optional
    - name: string
      version: string             # Optional
      required: boolean           # Optional, default: false
      install_url: string         # Optional
      check_command: string       # Optional
  commands:                       # Optional: core commands needed
    - string                      # e.g., "speckit.tasks"
  scripts:                        # Optional: core scripts needed
    - string

provides:
  commands:                       # Required: at least one
    - name: string                # speckit.{ext-id}.{cmd-name}
      file: string                # Relative path
      description: string
      aliases: [string]           # Optional, same pattern
  config:                         # Optional
    - name: string
      template: string
      description: string
      required: boolean           # Default: false

hooks:                            # Optional
  event_name:                     # Single mapping
    command: string
    priority: integer             # Optional, >=1, default 10
    optional: boolean             # Default: true
    prompt: string                # For optional hooks
    description: string
    condition: string             # Optional
  another_event:                  # List of mappings
    - command: string
      priority: integer
    - command: string
      priority: integer

tags: [string]                    # Optional, 2-10 recommended

defaults:                         # Optional
  key: value                      # Any YAML structure

config_schema:                    # Optional, JSON Schema
  type: object
  properties: {...}
```

## Naming Conventions

### Extension ID Pattern

```
^[a-z0-9-]+$

Valid:
- jira
- my-ext
- tool-123

Invalid:
- MyExt (uppercase)
- my_ext (underscore)
- my ext (space)
```

### Command Name Pattern

```
^speckit\.[a-z0-9-]+\.[a-z0-9-]+$

Format: speckit.{extension-id}.{command-name}

Valid:
- speckit.jira.specstoissues
- speckit.my-ext.hello

Invalid:
- jira.specstoissues (missing prefix)
- speckit.hello (no extension namespace)
- speckit.myext.CreateIssues (uppercase)
```

### Version Pattern

```
Semantic versioning: X.Y.Z

Valid:
- 1.0.0
- 0.1.0
- 2.5.3

Invalid:
- 1.0 (missing patch)
- v1.0.0 (v prefix)
- 1.0.0-beta (pre-release tag)
```

## Directory Structure

### Standard Extension Layout

```
.specify/extensions/{ext-id}/
├── extension.yml               # Manifest (required)
├── {ext-id}-config.yml         # Project config (committed)
├── {ext-id}-config.local.yml   # Local overrides (gitignored)
├── {ext-id}-config.template.yml # Template reference
├── commands/                   # Command files
│   └── *.md
├── scripts/                    # Helper scripts
│   ├── bash/
│   └── powershell/
├── docs/                       # Documentation
└── README.md
```

### Repository Root Layout

```
spec-kit-my-ext/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── .extensionignore            # Exclude dev files from install
├── extension.yml
├── commands/
├── scripts/
├── docs/
└── tests/                      # Not copied during install
```

## Command File Format

### Universal Command Structure

Source: `extensions/EXTENSION-DEVELOPMENT-GUIDE.md`

```markdown
---
description: "Command description"     # Required
tools:                                 # Optional: MCP tools
  - 'mcp-server/tool_name'
scripts:                               # Optional: helper scripts
  sh: ../../scripts/bash/helper.sh
  ps: ../../scripts/powershell/helper.ps1
---

# Command Title

Command documentation in Markdown.

## Prerequisites

1. Requirement 1
2. Requirement 2

## User Input

$ARGUMENTS

## Steps

### Step 1: Description

Instruction text...

\`\`\`bash
# Shell commands
\`\`\`

### Step 2: Another Step

More instructions...

## Configuration Reference

Information about configuration options.

## Notes

Additional notes and tips.
```

### Frontmatter Fields

```yaml
description: string        # Required, brief command description
tools: [string]           # Optional, MCP tools required (e.g., 'jira-mcp/create')
scripts:                  # Optional, helper scripts
  sh: string              # Bash script path (relative to repo root)
  ps: string              # PowerShell script path
```

### Special Variables

- `$ARGUMENTS` - Placeholder for user-provided arguments
- Extension context automatically injected during registration:
  ```markdown
  <!-- Extension: {extension-id} -->
  <!-- Config: .specify/extensions/{extension-id}/ -->
  ```

### Script Path Rewriting

**In extension** (relative to repo root):
```yaml
scripts:
  sh: ../../scripts/bash/helper.sh
```

**After registration** (relative to project root):
```yaml
scripts:
  sh: .specify/scripts/bash/helper.sh
```

## Configuration Management

### Configuration File Hierarchy

Source: `extensions/RFC-EXTENSION-SYSTEM.md`

```
1. Extension defaults (extension.yml → defaults)
2. Project config ({ext-id}-config.yml)
3. Local overrides ({ext-id}-config.local.yml, gitignored)
4. Environment variables (SPECKIT_{EXT}_*)
```

### Configuration Example

**Extension defaults** (`extension.yml`):
```yaml
defaults:
  project:
    key: null
  hierarchy:
    issue_type: "subtask"
```

**Project config** (`.specify/extensions/jira/jira-config.yml`):
```yaml
project:
  key: "PROJ"

hierarchy:
  issue_type: "subtask"
```

**Local overrides** (`.specify/extensions/jira/jira-config.local.yml`, gitignored):
```yaml
project:
  key: "MYTEST"  # Override for local testing
```

**Environment variables** (highest precedence):
```bash
export SPECKIT_JIRA_PROJECT_KEY="DEVTEST"
```

### Environment Variable Pattern

Format: `SPECKIT_{EXTENSION}_{KEY}`

Examples:
- `SPECKIT_JIRA_PROJECT_KEY`
- `SPECKIT_LINEAR_API_KEY`
- `SPECKIT_GITHUB_TOKEN`

## Hook System

### Hook Definition

Source: `extensions/EXTENSION-API-REFERENCE.md`

**Single mapping** (one command per event):
```yaml
hooks:
  after_tasks:
    command: "speckit.jira.specstoissues"
    optional: true
    prompt: "Create Jira issues from tasks?"
    description: "Automatically create Jira hierarchy"
    condition: null
```

**List of mappings** (multiple commands per event):
```yaml
hooks:
  after_plan:
    - command: "speckit.my-ext.verify"
      priority: 5
      optional: false
      description: "Verify the plan"
    - command: "speckit.my-ext.report"
      priority: 10
      optional: true
      prompt: "Generate the report?"
      description: "Generate a report from the plan"
```

### Hook Priority Ordering

- Within an event, hooks run by **ascending priority** (lower number = runs first)
- Default priority: 10
- Equal priorities keep authoring order (stable sort)
- Repeated commands within manifest: last wins, moved to end

### Standard Hook Events

Source: `extensions/EXTENSION-API-REFERENCE.md`

Core-defined events:
- `before_specify` / `after_specify`
- `before_plan` / `after_plan`
- `before_tasks` / `after_tasks`
- `before_implement` / `after_implement`
- `before_analyze` / `after_analyze`
- `before_checklist` / `after_checklist`
- `before_clarify` / `after_clarify`
- `before_constitution` / `after_constitution`
- `before_taskstoissues` / `after_taskstoissues`

### Hook Configuration Storage

**In `.specify/extensions.yml`** (project-level):
```yaml
installed:
  - jira
  - linear

settings:
  auto_execute_hooks: true

hooks:
  after_tasks:
    - extension: jira
      command: speckit.jira.specstoissues
      enabled: true
      optional: true
      prompt: "Create Jira issues from tasks?"
      description: "..."
      condition: null
```

## Extension Registration

### Agent Format Rendering

Source: `presets/ARCHITECTURE.md`, `extensions/RFC-EXTENSION-SYSTEM.md`

| Agent | Format | Extension | Arg placeholder |
|-------|--------|-----------|-----------------|
| Claude, Cursor, opencode, Windsurf, etc. | Markdown | `.md` | `$ARGUMENTS` |
| Copilot | Markdown | `.agent.md` + `.prompt.md` | `$ARGUMENTS` |
| Gemini, Qwen, Tabnine | TOML | `.toml` | `{{args}}` |

### Registration Locations

```
.claude/commands/speckit.{ext}.{cmd}.md
.gemini/commands/speckit.{ext}.{cmd}.toml
.github/agents/speckit.{ext}.{cmd}.agent.md + .prompt.md
... (15+ agents supported)
```

### Extension Safety Check

Command names with 3+ dot segments (`speckit.{ext-id}.{cmd-name}`):
- Extract extension ID from command name
- Check if `.specify/extensions/{ext-id}/` exists
- Skip command if extension not installed (prevents orphan files)

Core commands (2 segments like `speckit.specify`): always registered

## Catalog System

### Dual Catalog Model

Source: `extensions/RFC-EXTENSION-SYSTEM.md`

1. **Default Catalog** (`catalog.json`)
   - Purpose: Curated, approved extensions
   - Default state: Empty (users populate with trusted extensions)
   - `install_allowed: true`
   - Priority: 1 (highest)

2. **Community Catalog** (`catalog.community.json`)
   - Purpose: Discovery of community extensions
   - Active, accepts submissions
   - `install_allowed: false` (discovery only)
   - Priority: 2

### Catalog Stack Resolution

Order (first match wins):
1. `SPECKIT_CATALOG_URL` environment variable (single catalog, backward compat)
2. Project config (`.specify/extension-catalogs.yml`)
3. User config (`~/.specify/extension-catalogs.yml`)
4. Built-in defaults (catalog.json + catalog.community.json)

### Catalog Config Format

**`.specify/extension-catalogs.yml`**:
```yaml
catalogs:
  - name: "default"
    url: "https://raw.githubusercontent.com/github/spec-kit/main/extensions/catalog.json"
    priority: 1
    install_allowed: true
    description: "Built-in catalog of installable extensions"

  - name: "internal"
    url: "https://internal.company.com/spec-kit/catalog.json"
    priority: 2
    install_allowed: true
    description: "Internal company extensions"

  - name: "community"
    url: "https://raw.githubusercontent.com/github/spec-kit/main/extensions/catalog.community.json"
    priority: 3
    install_allowed: false
    description: "Community-contributed extensions (discovery only)"
```

### Catalog Entry Format

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-01-28T14:30:00Z",
  "extensions": {
    "jira": {
      "name": "Jira Integration",
      "id": "jira",
      "description": "Create Jira Epics, Stories, and Issues from spec-kit artifacts",
      "author": "Stats Perform",
      "version": "1.0.0",
      "download_url": "https://github.com/statsperform/spec-kit-jira/releases/download/v1.0.0/spec-kit-jira-1.0.0.zip",
      "repository": "https://github.com/statsperform/spec-kit-jira",
      "homepage": "https://github.com/statsperform/spec-kit-jira/blob/main/README.md",
      "documentation": "https://github.com/statsperform/spec-kit-jira/blob/main/docs/",
      "changelog": "https://github.com/statsperform/spec-kit-jira/blob/main/CHANGELOG.md",
      "license": "MIT",
      "requires": {
        "speckit_version": ">=0.1.0,<2.0.0",
        "tools": [
          {
            "name": "jira-mcp-server",
            "version": ">=1.0.0"
          }
        ]
      },
      "tags": ["issue-tracking", "jira", "atlassian", "project-management"],
      "verified": true,
      "downloads": 1250,
      "stars": 45
    }
  }
}
```

### install_allowed Behavior

Extensions from discovery-only catalogs (`install_allowed: false`):
- Shown in `specify extension search` results
- Cannot be installed directly
- Warning message directs user to add to approved catalog

## Extension Lifecycle

### Installation Process

```bash
specify extension add jira
```

Steps:
1. Resolve extension in catalog
2. Download ZIP from `download_url`
3. Validate manifest schema and compatibility
4. Extract to `.specify/extensions/{ext-id}/`
5. Copy config templates
6. Register commands with AI agent(s)
7. Update `.specify/extensions/.registry`

### Development Installation

```bash
specify extension add --dev /path/to/extension
```

- Installs from local directory (no ZIP)
- No catalog lookup
- Useful for testing during development

### Registry Format

`.specify/extensions/.registry`:
```json
{
  "schema_version": "1.0",
  "extensions": {
    "jira": {
      "version": "1.0.0",
      "source": "catalog",
      "manifest_hash": "sha256...",
      "enabled": true,
      "registered_commands": ["speckit.jira.specstoissues", ...],
      "installed_at": "2026-01-28T14:30:00Z"
    }
  }
}
```

### Update Process

```bash
specify extension update jira
```

Atomic update with rollback:
1. Check catalog for newer version
2. **Backup**: Full extension dir, commands, hooks, registry
3. Download new version
4. Validate compatibility
5. Extract new version (preserve config)
6. Re-register commands
7. Update registry
8. **On failure**: Automatic rollback from backup

### Removal Process

```bash
specify extension remove jira
```

Steps:
1. Confirm with user
2. Unregister commands from AI agent(s)
3. Back up config (optional: `--keep-config`)
4. Remove `.specify/extensions/{ext-id}/`
5. Update registry

## Validation Rules

### Extension ID

```
Pattern: ^[a-z0-9-]+$

✓ Valid: my-ext, tool-123, awesome-plugin
✗ Invalid: MyExt (uppercase), my_ext (underscore), my ext (space)
```

### Extension Version

```
Format: X.Y.Z (semantic versioning)

✓ Valid: 1.0.0, 0.1.0, 2.5.3
✗ Invalid: 1.0 (missing patch), v1.0.0 (prefix), 1.0.0-beta (tag)
```

### Command Name

```
Pattern: ^speckit\.[a-z0-9-]+\.[a-z0-9-]+$

✓ Valid: speckit.my-ext.hello, speckit.tool.cmd
✗ Invalid: my-ext.hello (missing prefix), speckit.hello (no namespace)
```

### Command File Path

```
Must be relative to extension root

✓ Valid: commands/hello.md, commands/subdir/cmd.md
✗ Invalid: /absolute/path.md, ../outside.md
```

## .extensionignore Pattern

### Purpose

Exclude dev-only files from installation (tests, CI configs, docs source).

### Format

`.gitignore`-compatible patterns (powered by `pathspec` library):
- One pattern per line
- `#` for comments
- `*` matches anything except `/` (no directory crossing)
- `**` matches zero or more directories
- `?` matches single character except `/`
- Trailing `/` restricts to directories
- `/` in pattern anchors to extension root
- No `/` matches at any depth
- `!` negates (re-includes)

### Example

```gitignore
# .extensionignore

# Development files
tests/
.github/
.gitignore

# Build artifacts
__pycache__/
*.pyc
dist/

# Documentation source
docs/
CONTRIBUTING.md
```

### Limitations

- Single file at extension root only (no nested `.extensionignore`)
- Cannot re-include files inside excluded directories (dir exclusion prevents recursion)
- Workaround: Exclude directory contents individually instead of directory itself

## Quick Reference

### Manifest Checklist

- [ ] `schema_version: "1.0"`
- [ ] `extension.id` follows `^[a-z0-9-]+$`
- [ ] `extension.version` is semantic (X.Y.Z)
- [ ] `requires.speckit_version` specified
- [ ] At least one command in `provides.commands`
- [ ] Command names follow `speckit.{ext-id}.{cmd-name}`
- [ ] Command files use relative paths
- [ ] Hook commands reference provided commands

### Configuration Checklist

- [ ] Config template created (`{ext-id}-config.template.yml`)
- [ ] Defaults defined in `extension.yml` → `defaults`
- [ ] Config schema provided for validation (optional but recommended)
- [ ] Sensitive values use environment variables
- [ ] `.gitignore` includes `*-config.local.yml`

### Command File Checklist

- [ ] YAML frontmatter with `description`
- [ ] `$ARGUMENTS` placeholder for user input
- [ ] Script paths relative to repo root (will be rewritten)
- [ ] Clear step-by-step instructions
- [ ] Extension context documented

### Hook Checklist

- [ ] Event name is standard (before_*/after_*)
- [ ] Command references valid command from `provides.commands`
- [ ] Priority set appropriately (lower = runs first)
- [ ] Optional hooks have clear prompt text
- [ ] Description explains purpose

### Distribution Checklist

- [ ] README.md with installation instructions
- [ ] LICENSE file
- [ ] CHANGELOG.md with version history
- [ ] `.extensionignore` excludes dev files
- [ ] ZIP archive created for releases
- [ ] Catalog entry prepared (for submission)

## Common Patterns

### Extension with Hooks Example

From `extensions/git/extension.yml`:

```yaml
hooks:
  before_specify:
    command: speckit.git.feature
    optional: false
    description: "Create feature branch before specification"
  
  after_tasks:
    command: speckit.git.commit
    optional: true
    prompt: "Commit task changes?"
    description: "Auto-commit after task generation"
```

### Multiple Commands on Same Event

```yaml
hooks:
  after_plan:
    - command: "speckit.my-ext.verify"
      priority: 5
      optional: false
    - command: "speckit.my-ext.report"
      priority: 10
      optional: true
      prompt: "Generate report?"
```

### Extension with Configuration

```yaml
provides:
  config:
    - name: "jira-config.yml"
      template: "jira-config.template.yml"
      description: "Jira integration configuration"
      required: true

defaults:
  project:
    key: null
  hierarchy:
    issue_type: "subtask"
```

### Tool Requirements

```yaml
requires:
  speckit_version: ">=0.2.0"
  tools:
    - name: git
      required: false
    - name: jira-mcp-server
      required: true
      version: ">=1.0.0"
      install_url: "https://github.com/org/jira-mcp-server"
      check_command: "jira --version"
```

## Python API Reference

### Key Classes

Source: `extensions/EXTENSION-API-REFERENCE.md`

```python
from specify_cli.extensions import (
    ExtensionManifest,      # Manifest parsing and validation
    ExtensionRegistry,      # Registry CRUD operations
    ExtensionManager,       # Install/remove/update
    ExtensionCatalog,       # Catalog fetch and search
    CatalogEntry,           # Single catalog definition
    HookExecutor,           # Hook registration and execution
    CommandRegistrar,       # Command file conversion
)
```

### ExtensionManifest

```python
manifest = ExtensionManifest(Path("extension.yml"))

# Properties
manifest.id                        # str
manifest.version                   # str
manifest.commands                  # List[Dict]
manifest.hooks                     # Dict

# Methods
manifest.get_hash()                # str: SHA256 hash
```

### ExtensionManager

```python
manager = ExtensionManager(project_root)

# Install from directory (dev mode)
manifest = manager.install_from_directory(
    source_dir=Path("/path/to/ext"),
    speckit_version="0.1.0",
    register_commands=True
)

# Install from ZIP
manifest = manager.install_from_zip(
    zip_path=Path("ext.zip"),
    speckit_version="0.1.0"
)

# Remove
success = manager.remove(
    extension_id="jira",
    keep_config=False
)

# List installed
extensions = manager.list_installed()  # List[Dict]
```

### ExtensionCatalog

```python
catalog = ExtensionCatalog(project_root)

# Get active catalog stack
entries = catalog.get_active_catalogs()  # List[CatalogEntry]

# Search across all catalogs
results = catalog.search(
    query="jira",
    tag="issue-tracking",
    verified_only=True
)  # Returns: List[Dict] with _catalog_name, _install_allowed

# Get extension info
info = catalog.get_extension_info("jira")  # Optional[Dict]
```

### CatalogEntry

```python
entry = CatalogEntry(
    url="https://example.com/catalog.json",
    name="default",
    priority=1,
    install_allowed=True,
    description="Built-in catalog"
)
```

## Ambiguities and Gaps

### Clarified

1. **Command registration timing**: Commands registered at **install time**, not resolved through resolution stack at runtime (presets are resolved at runtime, extensions register once)

2. **Hook priority ties**: Equal priorities keep authoring order via stable sort

3. **Extension safety check**: 3+ dot segments trigger extension existence check; 2 segments (core) always register

4. **Catalog merge conflicts**: Higher-priority catalog (lower number) wins when same extension ID appears multiple times

5. **Development mode**: `--dev` installs from local directory, no catalog lookup, useful for testing

### Remaining Gaps

1. **Hook condition evaluation**: Syntax and evaluator for `condition` field not fully documented
   - Examples show string conditions like `"config.project.key is set"`
   - Evaluator implementation unclear

2. **Extension dependencies**: No clear pattern for extension A requiring extension B
   - `requires.commands` lists core commands, but not other extensions

3. **Deprecation handling**: Manifest supports `deprecated` flag but runtime behavior not detailed
   - Should warnings block execution or just log?

4. **Sandboxing/permissions**: Deferred to future, but no clear migration path

5. **Package signatures**: Checksum field exists but verification not enforced

## Recommendations for Spec 013

Based on these patterns, for MATD extension development:

1. **Follow strict naming**: Use lowercase-hyphen pattern for extension ID, commands namespace
2. **Provide config template**: Always include `{ext-id}-config.template.yml` with sensible defaults
3. **Use hooks strategically**: Wire into before/after events that match MATD workflow phases
4. **Support multi-agent**: Universal Markdown format ensures broad compatibility
5. **Document clearly**: Command files should be self-documenting with clear prerequisites and steps
6. **Version carefully**: Follow semantic versioning strictly for compatibility
7. **Test locally first**: Use `--dev` flag for testing before packaging
8. **Exclude dev files**: Use `.extensionignore` to keep ZIP clean
9. **Provide examples**: Include example configs in docs/ for common scenarios
10. **Consider catalog**: For team distribution, create project catalog in `.specify/extension-catalogs.yml`

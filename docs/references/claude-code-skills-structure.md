# Claude Code Skills Structure

**Source:** Official Agent Skills specification (agentskills.io) and Claude Code implementation (retrieved 2026-06-10)  
**Purpose:** Authoritative reference for marketplace skill development

## Overview

Skills are modular, self-contained packages that extend Claude Code's capabilities by providing specialized knowledge, workflows, and tools. They act as "onboarding guides" for specific domains or tasks, transforming Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

**Official Specification:** https://agentskills.io/specification  
**Claude Cookbook Examples:** https://github.com/anthropics/anthropic-cookbook/tree/main/skills

## Directory Structure

### Minimal Skill Structure

```
skill-name/
└── SKILL.md          # Required: Frontmatter + instructions
```

### Complete Skill Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown body
├── scripts/          # Optional: Executable code (Python/Bash/JS)
│   └── processor.py
├── references/       # Optional: Documentation loaded on demand
│   └── api-docs.md
└── assets/           # Optional: Templates, images, data files
    └── template.xlsx
```

### Key Principles

- **Name must match directory**: If the skill is in `pdf-processing/`, the `name` field must be `pdf-processing`
- **SKILL.md is required**: Must contain valid YAML frontmatter followed by Markdown content
- **Subdirectories are optional**: Only include `scripts/`, `references/`, or `assets/` if needed

## SKILL.md Format

### Required Frontmatter

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Optional Frontmatter Fields

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
license: Apache-2.0
compatibility: Requires pdfplumber and pypdf packages
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(python:*) Read Write
---
```

### Frontmatter Field Specifications

| Field | Required | Constraints | Purpose |
|-------|----------|-------------|---------|
| `name` | Yes | 1-64 chars, lowercase, hyphens only, no leading/trailing/consecutive hyphens | Skill identifier (must match directory name) |
| `description` | Yes | 1-1024 chars, non-empty | What the skill does AND when to use it (primary triggering mechanism) |
| `license` | No | Short string | License name or reference to bundled license file |
| `compatibility` | No | Max 500 chars | Environment requirements (intended product, packages, network access) |
| `metadata` | No | Key-value map | Additional properties (author, version, etc.) |
| `allowed-tools` | No | Space-delimited list | Pre-approved tools (experimental) |

### Name Field Rules

**Valid examples:**
```yaml
name: pdf-processing
name: data-analysis
name: code-review
```

**Invalid examples:**
```yaml
name: PDF-Processing  # uppercase not allowed
name: -pdf            # cannot start with hyphen
name: pdf--processing # consecutive hyphens not allowed
```

**Validation rules:**
- Must be 1-64 characters
- Only unicode lowercase alphanumeric characters and hyphens (a-z and -)
- Must not start or end with `-`
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name exactly

### Description Field Best Practices

The `description` field is the **primary triggering mechanism** for your skill. It determines when Claude Code loads and activates the skill.

**Good example:**
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**Poor example:**
```yaml
description: Helps with PDFs.
```

**Requirements:**
- Must be 1-1024 characters
- Should describe WHAT the skill does AND WHEN to use it
- Should include specific keywords that help agents identify relevant tasks
- Include all "when to use" information here (not in the body, as the body is only loaded after triggering)

### Body Content

The Markdown body after the frontmatter contains the skill instructions. There are no format restrictions.

**Recommended sections:**
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases
- References to bundled resources

**Important guidelines:**
- Keep under 500 lines (<5000 tokens recommended)
- Use imperative/infinitive form for instructions
- Move detailed reference material to separate files
- Consider progressive disclosure for complex skills

## Optional Subdirectories

### scripts/ - Executable Code

Contains executable code that agents can run. Use when:
- The same code is being rewritten repeatedly
- Deterministic reliability is needed
- Token efficiency is critical

**Supported languages:** Python, Bash, JavaScript (depends on agent implementation)

**Best practices:**
- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully
- Test scripts before packaging

**Example:**
```
scripts/
├── rotate_pdf.py
└── merge_pdfs.sh
```

**Note:** Scripts may still need to be read by Claude for patching or environment-specific adjustments.

### references/ - Documentation Loaded on Demand

Contains additional documentation that agents read when needed. Use for:
- Database schemas
- API documentation
- Domain knowledge
- Company policies
- Detailed workflow guides

**Benefits:**
- Keeps SKILL.md lean
- Loaded only when Claude determines it's needed
- Reduces context window usage

**Best practices:**
- Keep individual reference files focused
- For files >100 lines, include a table of contents
- Avoid deeply nested references (one level deep from SKILL.md)
- For files >10k words, include grep search patterns in SKILL.md

**Example:**
```
references/
├── REFERENCE.md      # Detailed technical reference
├── FORMS.md          # Form templates or structured data
├── finance.md        # Domain-specific knowledge
└── api_docs.md       # API specifications
```

**From SKILL.md, reference like this:**
```markdown
See [the API reference](references/api_docs.md) for complete method documentation.

For financial schemas, consult [finance.md](references/finance.md).
```

### assets/ - Static Resources

Contains static resources used in output (not loaded into context). Use for:
- Templates (document templates, configuration templates)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)
- Boilerplate code
- Fonts, icons, brand assets

**Benefits:**
- Separates output resources from documentation
- Enables Claude to use files without loading them into context
- Zero token cost for assets

**Example:**
```
assets/
├── logo.png
├── slides.pptx
├── frontend-template/
│   ├── index.html
│   └── styles.css
└── font.ttf
```

## Progressive Disclosure Architecture

Skills use a three-level loading system to manage context efficiently:

### Level 1: Metadata (Always Loaded)
- `name` + `description` fields
- ~100 tokens
- Always in context for all skills
- Determines skill triggering

### Level 2: SKILL.md Body (Loaded When Triggered)
- Instructions and core guidance
- <5000 tokens recommended
- Loaded when Claude decides to activate the skill

### Level 3: Bundled Resources (Loaded as Needed)
- Scripts can be executed without reading into context
- References loaded only when Claude determines they're needed
- Assets used in output (never loaded into context)
- Unlimited size (but scripts/references should be focused)

### Progressive Disclosure Patterns

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](references/FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](references/REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md) for common patterns
```

**Pattern 2: Domain-specific organization**

For skills with multiple domains, organize by domain to avoid loading irrelevant context:
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

**Pattern 3: Framework-specific organization**

For skills supporting multiple frameworks or variants:
```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

**Pattern 4: Conditional details**
```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](references/DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
**For OOXML details**: See [OOXML.md](references/OOXML.md)
```

## Discovery and Loading

### How Claude Code Discovers Skills

1. **At startup**: Claude Code scans configured directories for skills
2. **Metadata loading**: Reads `name` and `description` from all SKILL.md frontmatter
3. **Triggering**: When user request matches a skill's description, Claude decides to activate it
4. **Body loading**: SKILL.md body is loaded when skill is activated
5. **Resource loading**: References/scripts loaded on demand when Claude determines they're needed

### Skill Installation Locations

Skills can be installed in multiple locations:

#### User-Global Skills
- **Location**: `~/.claude/skills/`
- **Scope**: Available to all projects for this user
- **Use case**: Personal workflow preferences, frequently-used skills

#### Project-Local Skills
- **Location**: `.claude/skills/` (in project root)
- **Scope**: Available only to this project
- **Use case**: Project-specific skills, team-shared workflows

#### Plugin-Bundled Skills
- **Location**: `.claude-plugin/<plugin-name>/skills/` (via plugin system)
- **Scope**: Installed when plugin is installed
- **Use case**: Marketplace-distributed skills, bundled skill collections

### Symlink Patterns for Marketplace Skills

In the harness-tooling marketplace:

```
.agents/plugins/all-my-skills/
├── .claude-plugin/
│   └── marketplace.json
├── skills -> ../../skills  # Symlink to shared skills directory
├── agents -> ../../agents  # Symlink to shared agents directory
└── commands -> ../../commands  # Symlink to shared commands directory
```

This pattern allows:
- Single source of truth for skills in `.agents/skills/`
- Multiple plugins to reference same skills via symlinks
- Container-safe bind mounting (symlinks point to container-absolute paths)

## Skills vs Agents vs Commands

### Skills
- **Definition**: Procedural knowledge packages with instructions, scripts, and resources
- **Location**: `.claude/skills/` or `.agents/skills/`
- **Format**: Directory with SKILL.md + optional resources
- **Loading**: Description-based triggering, progressive disclosure
- **Use case**: Domain expertise, specialized workflows, tool integrations

### Agents
- **Definition**: Specialized Claude instances with pre-configured system prompts
- **Location**: `.claude/agents/` or `.agents/agents/`
- **Format**: AGENT.md with configuration
- **Invocation**: Explicitly spawned as subagents for specific tasks
- **Use case**: Multi-agent orchestration, role-based task delegation

### Commands
- **Definition**: Slash commands that extend CLI functionality
- **Location**: `.claude/commands/` or `.agents/commands/`
- **Format**: Executable scripts or configuration files
- **Invocation**: User types `/command-name` in CLI
- **Use case**: Workflow shortcuts, custom CLI actions

**Hierarchy in Claude Code:**
```
User Request
    ↓
Commands (if /command used)
    ↓
Skills (if description matches)
    ↓
Agents (if explicitly spawned)
```

## Plugin Integration

### Plugin Manifest Format

Plugins are defined in `.claude-plugin/marketplace.json`:

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "owner-name"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./path/to/plugin",
      "description": "Plugin description",
      "version": "1.0.0",
      "keywords": ["keyword1", "keyword2"],
      "category": "development"
    }
  ]
}
```

### Plugin Directory Structure

```
.agents/plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/           # Skills bundled with this plugin
│   └── my-skill/
│       └── SKILL.md
├── agents/           # Agents bundled with this plugin
│   └── my-agent.md
└── commands/         # Commands bundled with this plugin
    └── my-command
```

### How Skills Fit Into Plugin System

1. **Plugin declaration**: Plugin manifest lists available plugins
2. **Installation**: User installs plugin via CLI or marketplace
3. **Skill discovery**: Claude Code scans plugin's `skills/` directory
4. **Metadata loading**: All skill metadata loaded at startup
5. **Triggering**: Skills trigger based on description match
6. **Progressive loading**: Body and resources loaded as needed

### Marketplace Overlay System

The harness-tooling marketplace uses a manifest-based overlay system:

**Three-layer merge:**
1. Workspace defaults (`.harness.yaml` in workspace template)
2. Committed project config (`.harness.yaml` in project root)
3. Private local overrides (`.harness.local.yaml`, gitignored)

**Manifest structure:**
```yaml
# .harness.yaml or .harness.local.yaml

# Which agent CLIs to populate (default: all three)
clis:
  - claude
  - opencode
  - gemini

# Named bundles (expanded first)
bundles:
  - pries-core
  - essentials

# Direct asset references
skills:
  - code-graph-context
  - architecture-wiki

plugins:
  - matd
  - harness-cgc-skill

# Subtraction (applied after all unions)
exclude:
  skills:
    - unwanted-skill
```

**Resolution:**
- Lists merge additively (union semantics)
- Later layers augment earlier ones
- Named bundles expand to concrete asset lists before exclusion
- Container-absolute symlinks for bind-mount safety

## Best Practices

### 1. Concise is Key

The context window is a public good. Skills share the context window with:
- System prompt
- Conversation history
- Other skills' metadata
- User request

**Default assumption: Claude is already very smart.**

Only add context Claude doesn't already have. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### 2. Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions):**
- Multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

**Medium freedom (pseudocode or scripts with parameters):**
- Preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior

**Low freedom (specific scripts, few parameters):**
- Operations are fragile and error-prone
- Consistency is critical
- Specific sequence must be followed

### 3. Progressive Disclosure

Keep SKILL.md body under 500 lines to minimize context bloat. Split content into separate files when approaching this limit.

**When splitting:**
- Reference them clearly from SKILL.md
- Describe when to read them
- Ensure the reader knows they exist and when to use them

### 4. Avoid Deeply Nested References

Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.

**Good:**
```
SKILL.md → references/finance.md
SKILL.md → references/sales.md
```

**Bad:**
```
SKILL.md → references/overview.md → finance/schemas.md
```

### 5. Structure Longer Reference Files

For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.

### 6. Avoid Duplication

Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill.

### 7. Don't Create Extraneous Documentation

A skill should only contain essential files that directly support its functionality. Do NOT create:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain information needed for an AI agent to do the job at hand.

### 8. Test Scripts Before Packaging

Scripts must be tested by actually running them to ensure there are no bugs and that the output matches what is expected.

### 9. Use Imperative/Infinitive Form

Write instructions using imperative/infinitive form:
- "Extract text from PDF"
- "Create a new document"
- "Use pdfplumber for text extraction"

Avoid:
- "You should extract text from PDF"
- "The agent extracts text from PDF"

## API Usage (For Skills in Claude API)

Skills can also be used in the Claude API with code execution capabilities.

### Required Beta Headers

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="your-api-key",
    default_headers={
        "anthropic-beta": "code-execution-2025-08-25,files-api-2025-04-14,skills-2025-10-02"
    }
)
```

**Required headers:**
- `code-execution-2025-08-25` - Enables code execution for Skills
- `files-api-2025-04-14` - Required for downloading generated files
- `skills-2025-10-02` - Enables Skills feature

### Using Skills in Messages

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
    }]
)
```

### Built-in Skills (API Only)

| Skill | ID | Description |
|-------|----|----|
| Excel | `xlsx` | Create and manipulate Excel workbooks with formulas, charts, and formatting |
| PowerPoint | `pptx` | Generate professional presentations with slides, charts, and transitions |
| PDF | `pdf` | Create formatted PDF documents with text, tables, and images |
| Word | `docx` | Generate Word documents with rich formatting and structure |

## Validation

Use the official `skills-ref` library to validate your skills:

```bash
# Install
pip install skills-ref

# Validate
skills-ref validate ./my-skill
```

**Validation checks:**
- YAML frontmatter format
- Required fields (name, description)
- Naming conventions
- Directory structure
- File references

**Source:** https://github.com/agentskills/agentskills/tree/main/skills-ref

## Examples from Official Sources

### Example 1: Minimal Skill

```
grill-me/
└── SKILL.md
```

**SKILL.md:**
```yaml
---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

### Example 2: Skill with References

```
dev-tdd/
├── SKILL.md
├── deep-modules.md
├── interface-design.md
├── mocking.md
├── refactoring.md
└── tests.md
```

**SKILL.md** contains core TDD workflow and references the other files for detailed guidance.

### Example 3: Skill with Scripts and References

```
manage-skill-creator/
├── SKILL.md
├── scripts/
│   ├── init_skill.py
│   └── package_skill.py
└── references/
    ├── workflows.md
    └── output-patterns.md
```

## Comparison with Harness-Tooling Structure

### Alignment

Our harness-tooling structure aligns well with official Agent Skills specification:

**Matches:**
- SKILL.md format with YAML frontmatter
- Directory structure (scripts/, references/, assets/)
- Progressive disclosure principle
- Name/description as primary triggering mechanism
- Validation with skills-ref

**Extensions:**
- Marketplace overlay system (.harness.yaml)
- Multi-CLI support (Claude Code, OpenCode, Gemini)
- Plugin system with symlink-based skill sharing
- Bundle-based skill collections
- Three-layer manifest merge (workspace → project → local)

### Differences

**Official specification:**
- Focused on single CLI (Claude Code)
- Direct skill installation
- Simple discovery model

**Harness-tooling:**
- Multi-CLI coordination
- Marketplace-based distribution
- Manifest-driven overlay system
- Symlink-based skill sharing across plugins
- Named bundles for workflow-based collections

### Recommendations for Alignment

1. **Keep SKILL.md format exactly as specified** - Don't extend frontmatter beyond official fields
2. **Maintain directory structure conventions** - scripts/, references/, assets/ only
3. **Follow naming conventions strictly** - Lowercase, hyphens only, no consecutive hyphens
4. **Validate with skills-ref** - Ensure all skills pass official validation
5. **Document harness-specific extensions separately** - Keep marketplace-configuration.md for overlay system
6. **Test cross-CLI compatibility** - Ensure skills work in Claude Code, OpenCode, Gemini
7. **Avoid skill-specific README files** - Keep documentation in SKILL.md and references/

## Summary

The Claude Code skills structure is well-specified and standardized through the Agent Skills specification (agentskills.io). Key takeaways:

1. **SKILL.md is mandatory** with YAML frontmatter (name + description)
2. **Progressive disclosure** keeps context window efficient (metadata → body → resources)
3. **Description is the trigger** - Must describe what AND when
4. **Three optional subdirectories** - scripts/, references/, assets/
5. **Validation is available** via skills-ref library
6. **Multiple installation locations** - user global, project local, plugin bundled
7. **Marketplace integration** via plugin system and manifest overlays

The harness-tooling implementation extends the official specification with multi-CLI support and marketplace distribution while maintaining full compatibility with the core Agent Skills format.

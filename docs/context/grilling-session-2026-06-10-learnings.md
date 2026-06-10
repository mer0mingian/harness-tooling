# Grilling Session Learnings - 2026-06-10

**Session:** Spec 002-013 grilling for implementation readiness
**Date:** 2026-06-10
**Focus:** SpecKit extension patterns, config architecture, terminology clarification

---

## Key Architectural Decisions

### 1. SpecKit Extension Config Location (Spec 013)

**Decision:** matd-config.yml MUST be at `.specify/extensions/matd/matd-config.yml`

**Rationale:**
- SpecKit extension system requires configs in `.specify/extensions/{ext-id}/`
- Enables multi-extension isolation (each extension owns its config namespace)
- Supports layered config pattern (template → user → local → env)

**Pattern:**
```
.specify/extensions/matd/
├── matd-config.yml              # User-editable project config
├── matd-config.local.yml        # Gitignored local overrides
└── config-template.yml          # Reference template (read-only)
```

**Config Resolution Order (highest priority last):**
1. Extension defaults (from `extension.yml` → `defaults` section)
2. Project config (`matd-config.yml`)
3. Local overrides (`matd-config.local.yml`, gitignored)
4. Environment variables (`SPECKIT_MATD_*`)

**Source:** `/submodules/harness-tooling/docs/references/speckit-extension-patterns.md` (lines 250-310)

---

### 2. SpecKit Extension Naming Conventions

**Strict Validation Rules:**
- **Extension ID:** `^[a-z0-9-]+$` (lowercase, hyphens only)
  - Valid: `matd`, `v-model`, `agent-assign`
  - Invalid: `MATD`, `matd_tdd`, `matd tdd`
  
- **Command names:** `^speckit\.[a-z0-9-]+\.[a-z0-9-]+$`
  - Format: `speckit.{extension-id}.{command-name}`
  - Valid: `speckit.matd.test`, `speckit.matd.specify-prd`
  - Invalid: `matd.test`, `speckit.test`, `speckit.matd.createIssue`

- **Version:** Semantic versioning `X.Y.Z` (no prefixes, no pre-release tags in manifest)

**Source:** `/submodules/harness-tooling/docs/references/speckit-extension-patterns.md` (lines 180-220)

---

### 3. Universal Markdown Command Format

**Discovery:** SpecKit uses Universal Markdown that works across 15+ agent formats

**Supported targets:**
- Claude Code, Copilot, Gemini, Cursor, Windsurf, Aider, Cline, Void, PearAI, OpenCode, Cody, DevOps GPT, GitHub Models, GitLab Duo, Tabnine

**Single source → multiple consumers:**
```markdown
# Command: speckit.matd.test

## Prerequisites
- matd-qa agent installed
- Test framework configured

## Steps
1. Load test strategy
2. Generate failing tests
3. Validate RED state
```

This single file is discovered and loaded by all 15+ agent formats without conversion.

**Implication:** No need for separate command formats per CLI tool. Write once, works everywhere.

**Source:** `/submodules/harness-tooling/docs/references/speckit-extension-patterns.md` (lines 70-150)

---

### 4. Terminology Clarification: Skills vs Extensions vs Commands

**Official Definitions:**

| Concept | What It Is | Where It Lives | Invocation |
|---------|-----------|----------------|------------|
| **Skill** | Procedural knowledge package (instructions + resources) | `.claude/skills/`, `~/.claude/skills/` | Auto-triggered by description match |
| **Agent** | Specialized Claude instance with role-based system prompt | `.claude/agents/`, `.agents/` | Explicit delegation (`Agent` tool) |
| **Extension** | SpecKit modular package (commands + config + hooks) | `.specify/extensions/{ext-id}/` | `specify extension install` |
| **Command** | SpecKit executable workflow step | `.specify/extensions/{ext-id}/commands/` | `specify {ext-id}:{cmd}` |

**Critical Clarification (2026-06-10):**
For **Claude Code specifically**, commands and skills are the **same mechanism**:
- Claude Code reads SpecKit extension `commands/*.md` files
- Claude understands them as skills/commands (interchangeable)
- Universal Markdown format works across all 15+ agent CLIs
- **SpecKit commands** can be delivered as skills to Claude Code

**Other agent CLIs:** May have different mechanisms, but Universal Markdown format ensures broad compatibility.

**Architecture Pattern:**
```
harness-tooling/
├── .claude/                              # Claude Code plugin
│   └── skills/                           # Skills (symlinked from .agents/skills/)
│       └── my-skill/SKILL.md
├── .agents/                              # Marketplace canonical source
│   └── skills/                           # Skills (flat structure)
│       └── my-skill/SKILL.md
└── spec-kit-multi-agent-tdd/             # SpecKit extension
    └── commands/                         # Commands (NOT skills)
        └── specify-prd.md
```

**Sources:**
- `/submodules/harness-tooling/docs/references/claude-code-skills-structure.md` (lines 100-150)
- `/submodules/harness-tooling/docs/references/speckit-extension-patterns.md` (lines 40-70)

---

### 5. Progressive Disclosure (3-Level Loading)

**Pattern for Skills:**
- **Level 1: Metadata** (~100 tokens, always loaded)
  - Frontmatter: `name`, `description`
  - Used for triggering and discovery
  
- **Level 2: Instructions** (<5000 tokens, loaded when triggered)
  - SKILL.md body content
  - Full procedural instructions
  
- **Level 3: Resources** (loaded on demand or executed without context)
  - `scripts/` - Executable helpers
  - `references/` - Deep domain knowledge
  - `assets/` - Static files

**Why It Matters:**
- Keeps context window clean (only load what's needed)
- Descriptions are primary triggering mechanism (must be specific)
- Keep SKILL.md body under 500 lines (<5000 tokens)

**Source:** `/submodules/harness-tooling/docs/references/claude-code-skills-structure.md` (lines 200-250)

---

### 6. Multi-Catalog System (SpecKit Extensions)

**Pattern:** Dual catalog model with priority-based resolution

**Example:**
```yaml
# .specify/extension-catalogs.yml
catalogs:
  - name: "stepstone-internal"
    url: "https://artifacts.stepstone.com/speckit/catalog.json"
    priority: 1                    # Highest priority
    install_allowed: true
    
  - name: "default"
    url: "https://github.com/github/spec-kit/.../catalog.json"
    priority: 2
    install_allowed: true
    
  - name: "community"
    url: "https://.../catalog.community.json"
    priority: 3
    install_allowed: false         # Discovery only
```

**Conflict Resolution:**
- Lower priority number = higher precedence (1 > 2 > 3)
- First match wins (search stops at first catalog with matching extension)
- `install_allowed: false` = discovery only (cannot install, only browse)

**Use Case:** Corporate + public + community catalogs operating in parallel

**Source:** `/submodules/harness-tooling/docs/references/speckit-extension-patterns.md` (lines 650-720)

---

### 7. Preset vs Extension (When to Use Which)

| Aspect | Preset | Extension |
|--------|--------|-----------|
| **Purpose** | Template variants + config defaults | New commands + workflows + hooks |
| **Lifecycle** | Selected at `specify init`, override per-file | Installed once, always active |
| **Composition** | Runtime (template resolution stack) | Install-time (command registration) |
| **Scope** | Templates + settings only | Commands + config + scripts + hooks |
| **Examples** | `python-fastapi`, `typescript-react` | `matd`, `v-model`, `agent-assign` |

**Decision Rule:**
- Need different **templates**? → Preset
- Need new **commands/workflows**? → Extension
- Both? → Extension with preset field (spec 009)

**Source:** `/submodules/harness-tooling/docs/references/speckit-preset-and-workflow-patterns.md` (lines 50-100)

---

### 8. Symlink Pattern for Marketplace Skills

**Harness-Specific Pattern:**
```
.agents/skills/                   # Canonical source (flat)
  └── my-skill/SKILL.md

.claude/skills/                   # Claude Code plugin (symlinks)
  └── my-skill -> ../../.agents/skills/my-skill
```

**Why:**
- Single source of truth (`.agents/skills/`)
- Automatic updates (edit once, all sessions see changes)
- Multi-CLI support (OpenCode reads `.agents/`, Claude Code reads `.claude/`)
- No duplication

**Validation:**
- Symlink target must exist
- Directory name must match skill name
- SKILL.md must be at symlink target root

**Source:** harness-tooling README.md + claude-code-skills-structure.md (section 7)

---

## Impact on Spec 013 (Enhanced Workspace Structure)

### Required Changes:

1. **Config location** → Update to `.specify/extensions/matd/matd-config.yml`
2. **Phase 1.2** → Create config in SpecKit extension directory, not workspace root
3. **Phase 4** → Update SpecKit **commands** (not skills)
4. **extension.yml** → Add `provides.config` section
5. **Documentation** → Update all references to config path

### Validation:

- Extension ID: `matd` ✅ (matches pattern)
- Command names: `speckit.matd.*` ✅ (matches pattern)
- Config naming: `matd-config.yml` ✅ (matches `{ext-id}-config.yml`)
- Universal Markdown ✅ (already using)

---

## Gaps Identified

### SpecKit Extension System:
1. Extension dependency graph (A requires B) not documented
2. Hook condition syntax incomplete
3. Preset composition edge cases (multiple wraps) unclear

### Claude Code Skills:
1. Plugin system integration details sparse in official docs
2. Marketplace distribution patterns harness-specific
3. Multi-CLI coordination harness-specific

### MATD Workspace:
1. PRD/SD/Spec numbering mechanism not specified (manual vs auto-increment?)
2. Traceability validation tooling (Tier 4) out of scope for spec 013
3. Migration rollback procedure needs detail

---

## References Created This Session

1. `/docs/references/speckit-extension-patterns.md` (938 lines)
   - Extension manifest, commands, config, hooks, catalogs, validation

2. `/docs/references/speckit-preset-and-workflow-patterns.md` (774 lines)
   - Presets, workflows, template resolution, state management

3. `/docs/references/claude-code-skills-structure.md` (755 lines)
   - Skills format, progressive disclosure, discovery, best practices

4. `/docs/context/grilling-session-2026-06-10-learnings.md` (this file)
   - Session insights, architectural decisions, patterns discovered

---

## Next Steps for Grilling Session

### Spec 013 (Enhanced Workspace Structure):
- ✅ Config location confirmed (`.specify/extensions/matd/`)
- ✅ Naming patterns validated
- ⏭️ Q5: PRD/SD/SPEC numbering mechanism (auto-increment vs manual?)
- ⏭️ Q6: Migration script language (bash vs Python?)
- ⏭️ Q7: Backward compatibility duration (how long support flat files?)

### Specs 002-004 (Three-Input DESIGN Model):
- ⏭️ Schema format (JSON Schema vs YAML schema?)
- ⏭️ Grill-me integration points
- ⏭️ MCP tool dependencies
- ⏭️ Traceability chain validation

### Specs 006-011 (Remaining Stubs):
- ⏭️ Prioritization (which to grill first after 013 → 002-004?)
- ⏭️ Dependencies between specs
- ⏭️ Story point estimation alignment

---

## Spec 002 Grilling Results (Product Brief)

### Resolved Questions (OQ-B1 through OQ-B12)

**Two-Tier Schema Architecture:**
- **Tier A (≤3 components)**: Lightweight 8-section template
- **Tier B (≥4 components)**: Full Charter 9-section business-focused template
- **Trigger:** Stonehenge component count query (via MCP)
- **Rationale:** Component count knowable at Product Brief time; Story Points measure implementation complexity (unknown until solution design)

**Content Boundary (Business Invariants Only):**
- **Included:** Vision, Scope, Investment, Stakeholders, Risks, Compliance governance, Success Metrics, Policies
- **Excluded:** Section 3 (Solution Approach - ADRs, tech choices) → Solution Design
- **Excluded:** Section 8 (Quality & NFRs) → System Constitution
- Maintains three-input model separation: Business invariants (Brief) vs Technical decisions (Constitution/Design)

**Schema Implementation:**
- Two separate YAML schemas (not conditional)
  - `product-brief-simple-schema.yml` (Tier A)
  - `product-brief-charter-schema.yml` (Tier B)
- Command selects schema based on Stonehenge query result
- Two-layer validation: structural (required sections) + semantic (LLM rubric: "business invariants only?")

**Integration Dependencies:**
- **Stonehenge MCP**: Already exists (`mcp__stonehenge-mcp__execute_query` at `https://stonehenge-mcp.ds.daas.stepstone.com/mcp`)
- **Query pattern**: `SELECT COUNT(*) FROM stonehenge WHERE kind = 'Component' AND [system_filter]`
- **Fallback**: Manual user input if MCP unavailable

**Confluence Publishing:**
- **v1**: Manual copy/paste
- **Future**: Automated markdown macro embed

### Needs Clarification (Blocks Implementation)

**OQ-B7-B9: Stonehenge/EA Maps Integration**
1. System name → Stonehenge entity mapping (which field to filter?)
2. EA Maps fallback mechanism (when/how?)
3. MCP tool deployment in MATD workspaces (auto-installed or manual?)

**Status:** Spec 002 design-complete, pending MCP integration clarification. Core schema/templates can start while integration details finalized. Fallback (manual component count) allows v1 to ship.

---

**Status:** Spec 002 grilling complete (design-complete, pending clarification)
**Next:** Grill spec 003 (System Constitution), spec 004 (Solution Design)

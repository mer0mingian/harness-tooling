# Enhanced Workspace Structure

---
spec_id: SPEC-0013
title: Enhanced Workspace Structure
status: design-complete
created: 2026-06-10
updated: 2026-06-10
story_points: 6
---

## Problem

Current MATD workspace structure has limitations:

1. **Flat spec files** - Specifications are single files in `specs/` with no co-located artifacts
2. **No traceability chain** - Missing explicit linkage between PRDs → Solution Designs → Specs
3. **No dependency tracking** - Unclear which specs depend on others, blocking parallel work
4. **Scattered artifacts** - Plans, tasks, and designs have no standard home per-spec
5. **Hard to archive** - Moving completed specs to archive requires manual coordination

This makes it difficult to:
- Understand the full context of a specification
- Track implementation dependencies
- Maintain audit trail from requirements to code
- Generate test coverage reports
- Archive completed work cleanly

## Solution

Implement a specs-as-folders pattern with configuration-driven paths and complete traceability metadata.

### Core Components

1. **Specs-as-Folders Pattern**
   - Each spec lives in `specs/SPEC-XXXX/` folder
   - Contains: `spec.md`, `plan.md`, `tasks.md`, `dependency-map.md`
   - Optional `design/` subfolder for spec-specific diagrams/architecture

2. **Configuration File (`matd-config.yml`)**
   - **Location:** `.specify/extensions/matd/matd-config.yml` (SpecKit extension convention)
   - Defines all MATD paths (prds, solution-designs, specs, tests, adrs)
   - Configures numbering format (prefix, zero-padding width)
   - **Numbering mechanism:** Auto-increment (scan active + archived directories, find max ID, increment)
   - Specifies spec folder structure conventions
   - Allows per-project customization
   - Layered resolution: defaults (extension.yml) → project → local → env vars

3. **Traceability Frontmatter**
   - PRD files: `prd_id`, `title`, `created`
   - Solution Design files: `sd_id`, `title`, `prd`, `requirements`, `adrs`
   - Spec files: `spec_id`, `title`, `solution_design`, `prd`, `status`, `created`

4. **Dependency Mapping**
   - Each spec has `dependency-map.md` listing:
     - Dependencies (specs this one requires)
     - Blocks (specs waiting on this one)
     - Related (specs in same domain)

### Folder Structure

```
project-root/
├── .specify/
│   └── extensions/
│       └── matd/
│           ├── matd-config.yml              # Path and numbering configuration
│           ├── matd-config.local.yml        # Gitignored local overrides
│           └── config-template.yml          # Reference template
├── prds/
│   ├── PRD-001.md              # Product requirement documents
│   └── PRD-002.md
├── solution-designs/
│   ├── SD-001.md               # Solution designs (links to PRD via frontmatter)
│   └── SD-002.md
├── specs/
│   ├── SPEC-0001/
│   │   ├── spec.md             # Main specification
│   │   ├── plan.md             # Implementation plan
│   │   ├── tasks.md            # Task breakdown
│   │   ├── dependency-map.md   # Dependencies
│   │   └── design/             # Optional spec-specific designs
│   ├── SPEC-0002/
│   └── ...
├── specs_archive/
│   └── SPEC-0042/              # Entire archived spec folder
├── tests/
│   └── ...                     # Tests link to specs via markers
└── adrs/
    └── ...                     # Architecture decision records
```

## Scope (v1)

**Target:** workspace-template only (new projects going forward)
**Approach:** Breaking cutover - no migration script, no backward compatibility

### In Scope

1. **Implement specs-as-folders pattern in workspace-template**
   - Define folder structure standard for new projects
   - Update spec template to use folders
   - Document structure for new workspace initialization

2. **Create matd-config.yml schema**
   - Define configuration schema at `.specify/extensions/matd/matd-config.yml`
   - Document all configuration options
   - Provide default values in template

3. **Add traceability frontmatter to templates**
   - Update PRD template with metadata (prd_id, title, created)
   - Update Solution Design template with metadata (sd_id, prd, requirements, adrs)
   - Update Spec template with metadata (spec_id, solution_design, prd, status, created)
   - Document cross-reference conventions

4. **Update workspace-template structure**
   - Add `.specify/extensions/matd/matd-config.yml` template
   - Create `prds/`, `solution-designs/` directories in workspace-template
   - Update `AGENT.md` and `CONTEXT.md` to document new structure
   - Add example spec folder showing structure

### Out of Scope (v1)

1. **Migration of existing projects** - Breaking change, manual update required if needed
2. **Harness-tooling repo migration** - Repo's own specs can diverge from target structure
3. **Backward compatibility layer** - Old flat structure no longer supported in new projects
4. **Automated dependency map generation** - Tier 3 command, future work
5. **Test coverage reporting** - Tier 4 command, requires test discovery tooling
6. **Traceability validation** - Tier 4 command, requires metadata validation engine
7. **IDE integrations** - Future enhancement

## Dependencies

### Upstream Dependencies
- **Workspace-template structure** (exists at `/workspace-template/`)
- **Context doc** `matd-enhanced-structure.md` (exists)
- **SpecKit extension system** (patterns documented in `/docs/references/speckit-extension-patterns.md`)
  - Config must be at `.specify/extensions/matd/matd-config.yml` (not workspace root)
  - Naming: `{ext-id}-config.yml` pattern
  - Layering: defaults → project → local → env vars
- **Extension manifest** (`spec-kit-multi-agent-tdd/extension.yml`)
  - Must add `provides.config` section for matd-config.yml
  - Config template registration required

### Downstream Consumers (Blocked Until Spec 013 Complete)
- **SPEC-002**: Product Brief command (needs `product/` path config)
- **SPEC-003**: Constitution command (needs `architecture/` path config)
- **SPEC-004**: Solution Design command (needs `solution-designs/` path config)
- **SpecKit extension commands** (will need updates):
  - `speckit.matd.specify-prd` (create PRD folders)
  - Extension planning commands (write to `plan.md`)
  - Extension task commands (write to `tasks.md`)

## Acceptance Criteria

1. **Configuration Schema**
   - `matd-config.yml` schema is documented with all fields
   - Default configuration file exists in workspace-template
   - Schema supports path customization

2. **Spec Folder Creation**
   - New specs can be created as folders via SpecKit
   - Folder contains all required files (spec.md, plan.md, tasks.md, dependency-map.md)
   - Optional design/ folder can be created

3. **Traceability Metadata**
   - All PRD, SD, and Spec templates include frontmatter
   - Cross-references use standard field names (prd, solution_design)
   - Frontmatter is YAML-valid

4. **Migration Script**
   - Script successfully converts flat specs to folders
   - Original spec content is preserved in `spec.md`
   - Script creates placeholder `dependency-map.md`
   - Script documents manual steps for traceability

5. **Documentation**
   - Enhanced structure is documented
   - Migration guide exists
   - Examples show traceability chain
   - Configuration reference is complete

## Implementation Notes

### Critical Finding (2026-06-10 Grilling Session)
**Config location must follow SpecKit extension conventions:**
- ❌ NOT workspace root (`matd-config.yml`)
- ✅ MUST be `.specify/extensions/matd/matd-config.yml`
- Required: Add `provides.config` section to `extension.yml`
- Pattern documented in `/docs/references/speckit-extension-patterns.md`

### Reference Documentation
- Full design in `docs/context/matd-enhanced-structure.md`
- SpecKit patterns in `docs/references/speckit-extension-patterns.md`
- Align with existing workspace-template paths
- Consider backward compatibility during migration

### Testing Strategy
- Test with 1-2 example specs first
- Validate YAML frontmatter parsing
- Verify folder structure creation
- Test migration script on sample data

### Configuration Defaults
The `matd-config.yml` will default to:
- PRD prefix: "PRD", width: 3 (PRD-001)
- SD prefix: "SD", width: 3 (SD-001)
- Spec prefix: "SPEC", width: 4 (SPEC-0001)
- Standard folder names (prds, solution-designs, specs, specs_archive, tests, adrs)
- **Auto-increment scans both active + archive directories** to prevent ID collisions

### Breaking Change Notice
- **No migration script provided** - Breaking cutover for workspace-template
- Existing projects on old structure can continue using it (no forced upgrade)
- New projects from `harness init` get enhanced structure only
- Manual update required if existing project wants new structure

## Success Metrics

1. **Adoption**: 90%+ of new specs use folder structure within 2 weeks
2. **Traceability**: Every spec can be traced to PRD/SD via frontmatter
3. **Migration**: Existing specs migrated with <5% requiring manual fixes
4. **Configuration**: Default matd-config.yml requires zero customization for 80% of projects

## References

- Design: `docs/context/matd-enhanced-structure.md`
- Workspace template: `workspace-template/`
- SpecKit commands: Skills in `skills/speckit-*/`

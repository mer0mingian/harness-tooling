# Enhanced Workspace Structure

---
spec_id: SPEC-0012
title: Enhanced Workspace Structure
status: design-complete
created: 2026-06-10
story_points: 8
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
   - Defines all MATD paths (prds, solution-designs, specs, tests, adrs)
   - Configures numbering format (prefix, zero-padding width)
   - Specifies spec folder structure conventions
   - Allows per-project customization

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
├── matd-config.yml              # Path and numbering configuration
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

### In Scope

1. **Implement specs-as-folders pattern**
   - Define folder structure standard
   - Update spec template to use folders
   - Document migration from flat structure

2. **Create matd-config.yml schema**
   - Define configuration schema
   - Document all configuration options
   - Provide default values

3. **Add traceability frontmatter**
   - Update PRD template with metadata
   - Update Solution Design template with metadata
   - Update Spec template with metadata
   - Document cross-reference conventions

4. **Update workspace-template**
   - Add matd-config.yml to workspace-template
   - Create prds/ and solution-designs/ directories
   - Update documentation to reference new structure

5. **Migration script**
   - Script to convert existing flat specs to folders
   - Preserve spec content
   - Generate placeholder artifacts
   - Document manual steps

### Out of Scope (v1)

1. **Automated dependency map generation** - Tier 3 command, future work
2. **Test coverage reporting** - Tier 4 command, requires test discovery tooling
3. **Traceability validation** - Tier 4 command, requires metadata validation engine
4. **IDE integrations** - Future enhancement
5. **Automated spec numbering** - Already handled by existing SpecKit commands

## Dependencies

### Upstream Dependencies
- Workspace-template structure (exists)
- Context doc `matd-enhanced-structure.md` (exists)

### Downstream Consumers
- SpecKit specify commands (will need updates to create folders)
- SpecKit plan command (will write to `plan.md`)
- SpecKit tasks command (will write to `tasks.md`)

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

### Reference Documentation
- Full design in `docs/context/matd-enhanced-structure.md`
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
- Standard folder names (prds, solution-designs, specs, tests, adrs)

### Migration Considerations
- Preserve git history during migration
- Support incremental migration (not all-at-once)
- Document rollback procedure
- Provide validation script to check migration success

## Success Metrics

1. **Adoption**: 90%+ of new specs use folder structure within 2 weeks
2. **Traceability**: Every spec can be traced to PRD/SD via frontmatter
3. **Migration**: Existing specs migrated with <5% requiring manual fixes
4. **Configuration**: Default matd-config.yml requires zero customization for 80% of projects

## References

- Design: `docs/context/matd-enhanced-structure.md`
- Workspace template: `workspace-template/`
- SpecKit commands: Skills in `skills/speckit-*/`

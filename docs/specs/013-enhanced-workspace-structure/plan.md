# Implementation Plan: Enhanced Workspace Structure

## Phase 1: Configuration Schema and Documentation

### 1.1 Define matd-config.yml Schema
**Effort**: 1 SP

Create the configuration schema with:
- Path configuration for all MATD directories
- Numbering configuration (prefix, width)
- Spec folder structure definitions
- Test marker configuration

**Files**:
- Create `docs/schemas/matd-config-schema.yml` (JSON Schema)
- Document all configuration options

### 1.2 Create Default Configuration
**Effort**: 0.5 SP

**Files**:
- Create `workspace-template/matd-config.yml` with defaults
- Add inline comments documenting each option

**Validation**:
- YAML is valid
- All required fields present
- Comments are clear

## Phase 2: Template Updates

### 2.1 Update PRD Template
**Effort**: 0.5 SP

Add frontmatter to PRD template:
```yaml
---
prd_id: PRD-XXX
title: [Product Name]
created: YYYY-MM-DD
status: draft
---
```

**Files**:
- Update template used by `speckit-matd-specify-prd` skill

### 2.2 Update Solution Design Template
**Effort**: 0.5 SP

Add frontmatter to SD template:
```yaml
---
sd_id: SD-XXX
title: [Solution Name]
prd: PRD-XXX
requirements: [R1, R2, R3]
adrs: [ADR-001]
created: YYYY-MM-DD
status: draft
---
```

**Files**:
- Update template used by `speckit-matd-specify-solution-design` skill

### 2.3 Update Spec Template
**Effort**: 0.5 SP

Add frontmatter to spec template:
```yaml
---
spec_id: SPEC-XXXX
title: [Feature Name]
solution_design: SD-XXX
prd: PRD-XXX
status: design-complete
created: YYYY-MM-DD
story_points: X
---
```

**Files**:
- Update template in `skills/speckit-specify/`

### 2.4 Create Dependency Map Template
**Effort**: 0.5 SP

**Files**:
- Create `templates/dependency-map-template.md`:
  ```markdown
  # Dependencies for SPEC-XXXX
  
  ## Depends On
  - [List specs this one requires]
  
  ## Blocks
  - [List specs waiting on this one]
  
  ## Related
  - [List specs in same domain]
  ```

## Phase 3: Workspace Template Updates

### 3.1 Add New Directories
**Effort**: 0.5 SP

**Changes**:
- Create `workspace-template/prds/` with `.gitkeep`
- Create `workspace-template/solution-designs/` with `.gitkeep`
- Verify `workspace-template/specs/` and `workspace-template/specs_archive/` exist

### 3.2 Update Workspace Documentation
**Effort**: 1 SP

**Files**:
- Update `workspace-template/CONTEXT.md` to reference enhanced structure
- Update `workspace-template/AGENT.md` to document spec folder conventions
- Add examples of traceability chain

## Phase 4: SpecKit Command Updates

### 4.1 Update speckit-specify Skill
**Effort**: 1.5 SP

Modify to create spec folders instead of flat files:
- Detect if spec already exists (folder or flat file)
- Create `specs/SPEC-XXXX/` folder
- Write `spec.md` with frontmatter
- Create placeholder `plan.md`, `tasks.md`, `dependency-map.md`

**Files**:
- `skills/speckit-specify/skill.md`
- Test with example spec creation

### 4.2 Update speckit-plan Skill
**Effort**: 0.5 SP

Write plan to `specs/SPEC-XXXX/plan.md` instead of separate file.

**Files**:
- `skills/speckit-plan/skill.md`

### 4.3 Update speckit-tasks Skill
**Effort**: 0.5 SP

Write tasks to `specs/SPEC-XXXX/tasks.md` instead of separate file.

**Files**:
- `skills/speckit-tasks/skill.md`

## Phase 5: Migration Script

### 5.1 Create Migration Script
**Effort**: 1.5 SP

**Script**: `scripts/migrate-specs-to-folders.sh`

**Logic**:
1. Find all flat spec files: `specs/*.md`
2. For each spec:
   - Extract spec ID from filename
   - Create `specs/SPEC-XXXX/` folder
   - Move file to `specs/SPEC-XXXX/spec.md`
   - Create placeholder `dependency-map.md`
   - Generate `plan.md` if spec has plan section
   - Generate `tasks.md` if spec has tasks section
3. Report success/failures

**Safety**:
- Dry-run mode (`--dry-run`)
- Backup option (`--backup`)
- Validation checks

### 5.2 Create Migration Documentation
**Effort**: 0.5 SP

**Files**:
- Create `docs/guides/migrate-to-enhanced-structure.md`

**Content**:
- Prerequisites
- Step-by-step migration guide
- Rollback procedure
- Validation checklist
- Manual steps (adding frontmatter)

## Phase 6: Documentation and Examples

### 6.1 Create Enhanced Structure Guide
**Effort**: 1 SP

**Files**:
- Create or update `docs/guides/enhanced-workspace-structure.md`

**Content**:
- Overview of structure
- Traceability chain examples
- Configuration reference
- Best practices

### 6.2 Create Example Specs
**Effort**: 1 SP

Create 2 example specs demonstrating:
- Complete traceability (PRD → SD → Spec)
- Dependency mapping
- All required files

**Files**:
- Example specs in workspace-template or docs/examples/

## Phase 7: Testing and Validation

### 7.1 Test Spec Creation Workflow
**Effort**: 0.5 SP

1. Use updated SpecKit commands to create new spec
2. Verify folder structure
3. Verify all files created
4. Verify frontmatter validity

### 7.2 Test Migration Script
**Effort**: 0.5 SP

1. Create test specs in flat format
2. Run migration script
3. Validate conversion
4. Check git history preservation

### 7.3 Validate Configuration
**Effort**: 0.5 SP

1. Test matd-config.yml parsing
2. Verify all paths resolve correctly
3. Test with custom configuration

## Rollout Plan

1. **Merge to main**: After Phase 1-6 complete and tested
2. **Documentation**: Update harness-sandbox-stony docs to reference enhanced structure
3. **Migration**: Run migration script on existing specs
4. **Validation**: Manual review of migrated specs
5. **Announcement**: Document new structure in project README

## Risk Mitigation

1. **Backward compatibility**: Support both flat files and folders during transition
2. **Migration safety**: Require backup before migration, provide rollback
3. **Validation**: Provide script to validate folder structure
4. **Testing**: Test with example specs before production migration

## Success Criteria

- [ ] matd-config.yml schema documented
- [ ] All templates updated with frontmatter
- [ ] Workspace template includes new directories
- [ ] SpecKit commands create spec folders
- [ ] Migration script successfully converts test data
- [ ] Documentation complete with examples
- [ ] At least 2 example specs demonstrate full traceability

## Total Effort: 8 Story Points

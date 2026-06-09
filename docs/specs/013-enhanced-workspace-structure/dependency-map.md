# Dependencies for SPEC-0012

## Depends On

### External Dependencies
- **Workspace-template structure** (exists)
  - Location: `/workspace-template/`
  - Required directories: `specs/`, `specs_archive/`, `tests/`, `product/`
  - Status: Available

- **Context documentation** (exists)
  - File: `docs/context/matd-enhanced-structure.md`
  - Contains: Full design specification, folder structure, examples
  - Status: Available

### SpecKit Dependencies
- **speckit-specify skill** (will need updates)
  - Currently creates flat spec files
  - Needs modification to create spec folders
  - Impact: Medium (core workflow change)

- **speckit-plan skill** (will need updates)
  - Currently creates plan files in separate location
  - Needs modification to write to `specs/SPEC-XXXX/plan.md`
  - Impact: Low (path change only)

- **speckit-tasks skill** (will need updates)
  - Currently creates tasks files in separate location
  - Needs modification to write to `specs/SPEC-XXXX/tasks.md`
  - Impact: Low (path change only)

## Blocks

- **SPEC-0013**: Dependency visualization command (Tier 3)
  - Requires: `dependency-map.md` format defined by this spec
  - Waiting on: Completion of Phase 5 (Migration Script)

- **SPEC-0014**: Test coverage reporting (Tier 4)
  - Requires: Test marker configuration in `matd-config.yml`
  - Waiting on: Completion of Phase 1 (Configuration Schema)

- **SPEC-0015**: Traceability validation command (Tier 4)
  - Requires: Frontmatter schema defined by this spec
  - Waiting on: Completion of Phase 2 (Template Updates)

## Related

### Same Domain (MATD Tooling)
- **SPEC-0001**: SpecKit MATD specify PRD
  - Will use PRD frontmatter defined here
  - Templates will be updated by this spec

- **SPEC-0002**: SpecKit MATD specify product brief
  - Related workflow, separate artifact type
  - May adopt similar frontmatter pattern

- **SPEC-0003**: SpecKit MATD specify constitution
  - Related workflow, separate artifact type
  - May adopt similar frontmatter pattern

- **SPEC-0004**: SpecKit MATD specify solution design
  - Will use SD frontmatter defined here
  - Templates will be updated by this spec

- **SPEC-0007**: Split Claude Code MATD plugin
  - May require updates to reference new structure
  - Low coupling (plugin wrapper)

- **SPEC-0008**: Split SpecKit MATD extension
  - May require updates to reference new structure
  - Medium coupling (core SpecKit logic)

### Workflow Impact
- **SPEC-0009**: MATD preset specify override
  - May need updates to handle folder-based specs
  - Impact: Low (override mechanism orthogonal to storage)

- **SPEC-0010**: Determine change level skill
  - Uses git diff to determine spec change level
  - May need updates to handle folder structure
  - Impact: Low (git operations unchanged)

- **SPEC-0011**: Estimate complexity skill
  - Reads spec content to estimate complexity
  - Path changes required to read from `specs/SPEC-XXXX/spec.md`
  - Impact: Low (path change only)

## Implementation Order

**Critical Path**:
1. This spec (SPEC-0012) must complete Phases 1-2 before:
   - SPEC-0001, SPEC-0004 (template updates)
   - Any new spec creation

2. Phase 4 (SpecKit updates) enables:
   - New spec creation with folder structure
   - Automated plan/tasks generation in correct location

3. Phase 5 (Migration) unblocks:
   - Converting existing flat specs
   - Full adoption of enhanced structure

**Parallel Work**:
- Documentation (Phase 6) can proceed alongside Phases 1-5
- Testing (Phase 7) runs incrementally after each phase

## Migration Impact

### Low Impact (Path changes only)
- Skills reading spec content
- Skills generating plans/tasks
- Test discovery tools (when implemented)

### Medium Impact (Logic changes)
- speckit-specify (folder creation)
- Migration script (new tool)
- Workspace template updates

### High Impact (Workflow changes)
- Spec archival process (move entire folder)
- Dependency tracking (new file to maintain)
- Traceability queries (new frontmatter fields)

## Notes

- All dependencies are internal to harness-tooling repository
- No external API or service dependencies
- Migration can be incremental (phased rollout)
- Backward compatibility maintained during transition

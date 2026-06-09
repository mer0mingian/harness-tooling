# Workspace Template Structure

## Source
Grilling session 2026-06-09
Reference documentation for SpecKit extension alignment

## Context
The SpecKit MATD extension must align with the workspace template's folder hierarchy. This document provides the canonical structure that extensions must respect.

## Details

### Canonical Reference
Full documentation: [/home/minged01/repositories/test/harness-sandbox-stony/docs/WORKSPACE_TEMPLATE.md](/home/minged01/repositories/test/harness-sandbox-stony/docs/WORKSPACE_TEMPLATE.md)

### Key Folder Paths

**Specifications:**
- `specs/` - Active specifications (MATD agents write here)
- `specs_archive/` - Archived/superseded specifications

**Product Documentation:**
- `product/` - Product briefs, vision, user journeys
- `product/brief.md` - Template for product vision (created by harness init)

**Architecture:**
- `architecture/decisions/` - ADRs (Architecture Decision Records)
- `architecture/design/` - System design documents
- `architecture/c4/` - C4 diagrams (Litho output, generated)

**Tests:**
- `tests/unit/` - Unit tests (matd-dev writes here)
- `tests/integration/` - Integration tests
- `tests/system/` - System tests
- `tests/acceptance/` - Acceptance tests (matd-qa writes E2E tests here)
- `tests/uat/` - User acceptance tests
- `tests/synthetic/` - Property-based/fuzz tests

**Planning:**
- `plans/` - Implementation plans, roadmaps (flat structure, numbered)

**Research:**
- `research/` - Research artifacts, spikes (flat structure)

**Components:**
- `components/` - Git submodules for application code

### SpecKit Path Mapping

From `spec-kit-multi-agent-tdd/extension.yml`:
```yaml
paths:
  specification: specs/
  specification_archive: specs_archive/
  plan: plans/
  research: research/
  architecture: architecture/decisions/
  design: architecture/design/
  product: product/
  test_unit: tests/unit/
  test_integration: tests/integration/
  test_system: tests/system/
  test_acceptance: tests/acceptance/
  test_uat: tests/uat/
  test_synthetic: tests/synthetic/
  component: components/
  c4: architecture/c4/
```

### Extension Alignment Requirements

1. **Respect existing paths** - Don't create new top-level folders
2. **Use artifact type mapping** - Let SpecKit resolve paths from types
3. **Follow flat structure** - plans/ and research/ are NOT hierarchical
4. **Preserve Litho integration** - architecture/c4/ is generated, don't write there
5. **Maintain separation** - Specs (workspace root) vs Code (components/)

## References
- Full Template Documentation: /home/minged01/repositories/test/harness-sandbox-stony/docs/WORKSPACE_TEMPLATE.md
- Extension Structure: /home/minged01/repositories/test/harness-sandbox-stony/SPECKIT_EXTENSION_STRUCTURE.md
- MATD Extension: /home/minged01/repositories/test/harness-sandbox-stony/submodules/harness-tooling/spec-kit-multi-agent-tdd/

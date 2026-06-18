# MATD Template Schemas Usage Guide

This directory contains YAML schema definitions for MATD (Multi-Agent Test-Driven Development) document templates. Each schema drives both interactive "grill" interviews and automated validation.

## Available Schemas

### 1. prd-schema.yml (Product Requirements Document)
**Purpose**: Guide product managers through writing comprehensive PRDs
**Sections**: 12 sections covering problem framing, goals, hypothesis, metrics, workflows, scope, risks
**Use cases**: New feature development, product changes, business initiatives

### 2. service-reference-schema.yml ⭐ NEW
**Purpose**: Document microservices and components comprehensively
**Sections**: 16 sections covering metadata, APIs, architecture, dependencies, infrastructure, security
**Integrations**: 
- **Stonehenge** (Backstage.io catalog) categories: component type, lifecycle, dependencies, deployment
- **EA Maps** categories: domain, portfolio, capabilities, integration patterns
**Use cases**: Service onboarding, architecture documentation, team handovers, compliance audits

### 3. software-handover-schema.yml ⭐ NEW
**Purpose**: Guide systematic knowledge transfer between teams
**Sections**: 12 sections following StepStone ME team's proven handover methodology
**Phases**:
- **Phase 0**: Context and risks (Why? What if?)
- **Phase 1**: Architecture blueprint and mental model
- **Phase 2**: Local environment setup and debug test
- **Phase 3**: Reverse shadowing (active hands-on)
- **Phase 4**: Artifacts and maintenance
**Use cases**: Team transitions, service ownership changes, contractor offboarding, emergency coverage

## Schema Structure

Each schema follows this consistent pattern:

```yaml
version: "1.0"

sections:
  - id: section_identifier
    name: Human-Readable Section Name
    required: true|false
    id_prefix: "PREFIX-"  # For numbered items within section, or null
    
    grill_prompts:
      - "Question 1 to guide content creation?"
      - "Question 2 for this section?"
      # Interactive interview questions
    
    validation_rules:
      - id: SECTION-V001
        severity: CRITICAL|WARNING
        description: "What this rule checks"
        rule: "Technical validation logic"
```

## How Schemas Are Used

### 1. Grill Interview Mode
The `grill_prompts` drive an interactive Q&A session where the AI agent interviews the user to gather all necessary information for each section. This ensures nothing is missed.

**Example workflow**:
```bash
# User invokes the grill process
/matd-specify --template service-reference --grill

# Agent asks questions from each section's grill_prompts
# User provides answers
# Agent generates complete document with all sections populated
```

### 2. Validation Mode
The `validation_rules` enable automated content quality checking:

```bash
# Validate existing document
/matd-validate --schema service-reference-schema.yml --doc my-service.md

# Returns:
# ✓ CRITICAL rules passed (19/19)
# ⚠ WARNING rules: 3 failed
#   - LINKS-V003: API documentation link missing
#   - META-V004: Technology stack not documented
#   - INFRA-V005: Monitoring/observability not documented
```

### 3. Template Generation
Schemas can generate empty templates with all sections:

```bash
# Generate template with placeholder text
/matd-template --schema service-reference-schema.yml --output SERVICE_REFERENCE.md
```

## Validation Rule Severities

### CRITICAL Rules
- **Must pass** before document is considered complete
- Block merge/approval in automated workflows
- Examples:
  - Required frontmatter fields exist
  - Mandatory sections are present and non-empty
  - No [PLACEHOLDER] or TODO residue in production docs

### WARNING Rules
- **Should pass** for high-quality documentation
- Don't block workflows but flag for review
- Examples:
  - Best practices (e.g., linking to diagrams)
  - Completeness checks (e.g., monitoring documented)
  - Format recommendations

## Service Reference Schema Details

### Stonehenge Integration Sections

**Component Metadata** (`component_metadata`):
- Component type (service, library, application, data-pipeline)
- Lifecycle stage (development, production, deprecated)
- System/domain ownership
- Technology stack

**Dependencies & Integrations** (`dependencies_and_integrations`):
- Upstream services (APIs called)
- Downstream consumers (who calls this service)
- Databases and data stores
- Message queues and event streams
- Third-party integrations

**Infrastructure & Deployment** (`infrastructure_and_deployment`):
- Cloud platform and accounts
- Deployment targets (ECS, Lambda, K8s)
- CI/CD pipelines
- Monitoring and observability
- Alerting and on-call procedures

### EA Maps Integration Section

**EA Maps Categorization** (`ea_maps_categorization`):
- EA Domain (Platform, Product, Data, Operations)
- EA Portfolio (auto-mapped from Stonehenge domain)
- Business capabilities supported
- Integration patterns (API Gateway, Event Mesh, Direct)

### Key Technical Sections

**API Endpoints** (`api_endpoints`):
- HTTP methods and paths
- Request/response schemas
- Authentication mechanisms
- Error scenarios

**Data Schemas** (`schemas`):
- API contracts (OpenAPI/Swagger)
- Database models
- Kafka event schemas (Avro)
- Schema versioning strategy

**Architecture Overview** (`architecture_overview`):
- Architecture pattern (microservice, event-driven, batch)
- Component responsibilities
- C4/sequence diagrams
- Key design decisions

## Software Handover Schema Details

### Phase-Based Structure

Follows StepStone ME team's proven methodology for sustainable knowledge transfer:

**Phase 0: Why? What if?** (`phase_0_context_and_risks`)
- Handover rationale and triggers
- Capacity assessment (both teams)
- Technical debt disclosure
- SLAs and blast radius
- Risk identification

**Phase 1: Architectural Blueprint** (`phase_1_architecture`)
- System Context Diagram (C4 Model)
- Data flow analysis (inputs, outputs, transformations)
- Infrastructure overview (Cloud, CI/CD, secrets)
- Environment verification (dev/staging/prod)

**Phase 2: Local Environment & Debug Test** (`phase_2_local_environment`)
- Dependency installation (SDKs, CLI tools, Docker)
- One-command setup verification
- Mock data and staging access
- **Critical**: Incoming team must demonstrate:
  - Setting breakpoints in core components
  - Triggering manual execution
  - Tracing logs entry-to-exit

**Phase 3: Reverse Shadowing** (`phase_3_reverse_shadowing`)
- Incoming team drives, outgoing team navigates
- Activities:
  - Write and test small feature/fix
  - Trigger CI/CD deployment
  - Investigate production bug or simulation
- Monitoring and alerting stack walkthrough

**Phase 4: Artifacts & Maintenance** (`phase_4_artifacts_and_maintenance`)
- Troubleshooting guide (common errors, fixes)
- Credential map (where to find API keys, secrets)
- Key contacts (upstream/downstream stakeholders)
- Stonehenge catalog ownership update

### Validation Emphasis

**Handover Readiness Checklist** (`handover_readiness_checklist`):
- Architecture diagrams updated in Git/Confluence
- Local setup works on clean machine (Windows/Mac/WSL)
- Incoming team pushed ≥1 change to Production/Staging
- Monitoring dashboards explained
- Alerting rules reviewed
- Team ownership transferred in Stonehenge

## Extending Schemas

To add a new section to an existing schema:

1. Add section definition with unique `id`
2. Write 3-7 `grill_prompts` that guide content creation
3. Define at least 1 CRITICAL validation rule
4. Add 2-3 WARNING rules for quality/completeness
5. Update this README with section purpose

**Example**:
```yaml
  - id: my_new_section
    name: My New Section
    required: true
    id_prefix: "NEW-"
    
    grill_prompts:
      - "What is the purpose of this section?"
      - "What information must be captured?"
    
    validation_rules:
      - id: NEW-V001
        severity: CRITICAL
        description: "Section must exist and be non-empty"
        rule: "section 'my_new_section' heading exists with non-empty body"
```

## Best Practices

### Writing Grill Prompts
✅ **DO**:
- Ask one clear question per prompt
- Start with "what", "how", "who", "where" for specificity
- Include examples in parentheses when helpful
- Order from high-level to detailed

❌ **DON'T**:
- Ask compound questions (split into multiple prompts)
- Use vague terms like "describe the system" (be specific)
- Assume domain knowledge (explain abbreviations)

### Writing Validation Rules
✅ **DO**:
- Make CRITICAL rules objective and automatable
- Use WARNING for subjective quality checks
- Write clear `description` that explains the "why"
- Test regex patterns against real content

❌ **DON'T**:
- Make everything CRITICAL (reserve for must-haves)
- Write rules that can't be automatically checked
- Use complex regex that's hard to maintain

## Comparison to Other Template Types

| Schema Type | Interactive Grill | Validation | Use Case |
|-------------|-------------------|------------|----------|
| **YAML schemas** (prd, service-ref, handover) | ✅ Yes | ✅ Automated | Structured documents with quality gates |
| **Markdown templates** (ADR, solution-design) | ❌ No | ⚠️ Manual | Flexible documents, team discretion |
| **Workflow templates** (workflow-summary) | ⚠️ Partial | ❌ No | Process documentation |

## Quick Reference

### Service Reference Schema
- **16 sections** (6 required, 10 optional)
- **38 CRITICAL rules** ensuring completeness
- **45 WARNING rules** for quality
- **Best for**: New service documentation, team onboarding, architecture reviews

### Software Handover Schema
- **12 sections** (9 required, 3 optional)
- **32 CRITICAL rules** ensuring handover success
- **27 WARNING rules** for thoroughness
- **Best for**: Team transitions, ownership changes, knowledge transfer

## Schema Validation Command Reference

```bash
# Validate document against schema
speckit validate \
  --schema templates/service-reference-schema.yml \
  --document docs/SERVICE_REFERENCE.md

# Generate template from schema
speckit template \
  --schema templates/software-handover-schema.yml \
  --output docs/HANDOVER.md

# Run grill interview
speckit grill \
  --schema templates/service-reference-schema.yml \
  --output my-service-reference.md
```

## Related Documentation

- **MATD Workflow**: `../README.md`
- **Speckit CLI**: `../../README.md`
- **Template Examples**: 
  - Service Reference: Example in progress
  - Handover: Based on Confluence ME space
- **Stonehenge Catalog**: https://stonehenge.stepstone.tools
- **EA Maps**: (internal architecture portal)

---

**Created**: 2026-06-16  
**Last Updated**: 2026-06-16  
**Maintainer**: MATD Team

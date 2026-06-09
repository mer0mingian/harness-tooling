# AGENT_SKILL_MATRIX.md

Agent-to-skill mappings for the MATD (Multi-Agent Test-Driven Development) framework.

## 7-Agent MATD Architecture

### 1. matd-product-manager
- **Role:** Business Strategy
- **Owns:** Product Brief, PRD (functional requirements from business view)
- **Skills:**
  - spec-product-requirement-formats
  - general-grill-me
  - general-verification-before-completion
- **MCP:** Jira (scoped inline via agent config)
- **Purpose:** Translates business needs into product requirements

### 2. matd-requirements-engineer
- **Role:** Technical Requirements
- **Owns:** System Constitution (NFRs/tech invariants), Build specs, Contracts
- **Skills:** TBD (NFR-focused skills to be defined)
- **Purpose:** Defines non-functional requirements, technical constraints, and system invariants

### 3. matd-architect
- **Role:** Solution Design
- **Owns:** Solution Design, C4 diagrams, ADRs
- **Skills:**
  - arch-c4-architecture
  - arch-architecture-patterns
  - arch-design-system-patterns
  - arch-mermaid-diagrams
  - arch-smart-docs
  - arch-writing-plans
  - orchestrate-multi-agent-patterns
  - orchestrate-subagent-driven-development
  - general-system-design
  - general-solid
- **Purpose:** Designs technical solutions and architectural decisions

### 4. matd-qa
- **Role:** Design Review for Simplicity & Architectural Correctness
- **Owns:** Test plans, E2E tests
- **Challenges:** PM + Req Engineer + Architect from simplicity/anti-overengineering & architectural correctness perspectives
- **Skills:**
  - review-simplify-complexity
  - review-check-correctness
  - general-solid
  - arch-architecture-patterns
  - arch-design-system-patterns
  - review-e2e-testing-patterns
  - review-webapp-testing
- **Purpose:** Ensures design quality, simplicity, and testability before implementation

### 5. matd-critical-thinker
- **Role:** Red Team Validator / Adversarial Testing
- **Owns:** Security analysis, edge case validation, failure mode analysis
- **Challenges:** ALL artifacts from security, edge cases, failure modes, testability, attack vectors
- **Skills:**
  - review-check-correctness
  - review-systematic-debugging
  - security-review
- **Purpose:** Adversarially validates all work products for robustness and security

### 6. matd-dev
- **Role:** Implementation
- **Owns:** Code, unit tests
- **Skills:**
  - dev-tdd
  - dev-diagnose
  - dev-databases
  - dev-database-migration
  - dev-backend-to-frontend-handoff
  - python-async-patterns
  - python-code-style
  - python-configuration
  - python-design-patterns
  - python-fastapi-templates
  - python-packaging
  - python-testing-uv-playwright
  - docker-expert
  - general-python-environment
  - general-verification-before-completion
- **Purpose:** Implements features following TDD practices

### 7. matd-orchestrator
- **Role:** Cross-framework Coordinator
- **Installed:** For compatibility (not used in Claude Code native workflows)
- **Skills:**
  - orchestrate-multi-agent-patterns
  - orchestrate-subagent-driven-development
  - orchestrate-dispatching-parallel-agents
  - orchestrate-executing-plans
  - orchestrate-finishing-a-development-branch
- **Purpose:** Coordinates multi-agent workflows in non-Claude-Code environments

## Architecture Notes

### Key Changes from 6-Agent Architecture
- **Split matd-specifier** into matd-product-manager (business) + matd-requirements-engineer (technical)
- **QA role expanded** to design review (simplicity/architectural correctness), not just testing
- **Critical-thinker role refined** to adversarial validation across all artifacts (security, edge cases, failure modes)
- **Removed stdd-* skills** (deleted/renamed to dev-tdd)

### MCP Access
- **matd-product-manager** gets Jira MCP scoped inline via agent config
- Other agents do not need Jira access (separation of concerns)

### Skill Access Control
- Use `disallowedTools` in agent config to restrict skill access per-agent
- All agents automatically get project memory (no configuration needed)

### Skill Assignment Philosophy
- **Specialists over generalists:** Each agent has focused skill set matching role
- **Overlap on core skills:** verification-before-completion, solid principles
- **Separation of concerns:** Business (PM) vs Technical (RE) vs Design (Architect) vs Quality (QA) vs Security (Critical-Thinker) vs Implementation (Dev)

## Usage in Claude Code

Agents are invoked via the `Agent` tool with skill filtering:
```
Agent(agentName="matd-architect", prompt="Design X", allowedTools=["arch-*", "orchestrate-*"])
```

Skills are automatically filtered based on agent config and allowed patterns.

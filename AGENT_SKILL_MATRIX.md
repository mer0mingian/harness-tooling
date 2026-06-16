# AGENT_SKILL_MATRIX.md

Agent-to-skill mappings for the MATD (Multi-Agent Test-Driven Development) framework.

## Plugin Marketplace Structure

The marketplace consists of 5 active plugins:

| Plugin                               | Version | Agents | Skills | Commands | Description                                |
|--------------------------------------|---------|--------|--------|----------|--------------------------------------------|
| **matd**                             | 1.9.0   | 6      | 50     | 0        | Core MATD agents and comprehensive skills  |
| **legacy-stdd-skills**               | 2.0.0   | 5      | 6      | 0        | Legacy STDD agents and skills              |
| **generalist-skills**                | 0.3.0   | 0      | 25     | 0        | General-purpose skills (no agents)         |
| **matd-workflow-standalone-commands**| 1.0.0   | 0      | 0      | 10       | Standalone workflow commands               |
| **harness-deepwiki-skill**           | 1.1.0   | 0      | 3      | 0        | DeepWiki context generation skills         |

**Removed plugins** (no longer in marketplace):
- harness-agents (agents migrated to legacy-stdd-skills)
- harness-cgc-skill (functionality merged elsewhere)
- harness-management-tools (deprecated)

## Agent Roles

| Agent | Role | Owns | MCP Access |
|---|---|---|---|
| **matd-product-manager** | Business Strategy | Product Brief, PRD (functional requirements) | Jira (scoped) |
| **matd-requirements-engineer** | Technical Requirements | System Constitution (NFRs/tech invariants), Build specs, Contracts | — |
| **matd-architect** | Solution Design | Solution Design, C4 diagrams, ADRs | — |
| **matd-qa** | Design Review (Simplicity & Correctness) | Test plans, E2E tests | — |
| **matd-critical-thinker** | Red Team Validator / Adversarial Testing | Security analysis, edge case validation, failure mode analysis | — |
| **matd-dev** | Implementation | Code, unit tests | — |
| **matd-orchestrator** | Cross-framework Coordinator (compatibility only) | Workflow coordination | — |

## Skill Permission Matrix

| Skill | PM | Req Eng | Architect | QA | Crit Think | Dev | Orchestrator |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Architecture Skills** ||||||||
| arch-api-design-principles ||||||||
| arch-architecture-patterns |||| ✓ | ✓ ||||
| arch-c4-architecture |||| ✓ ||||
| arch-design-system-patterns |||| ✓ | ✓ ||||
| arch-mermaid-diagrams |||| ✓ ||||
| arch-smart-docs |||| ✓ ||||
| arch-writing-plans |||| ✓ ||||
| **Development Skills** ||||||||
| dev-backend-to-frontend-handoff |||||| ✓ ||
| dev-database-migration |||||| ✓ ||
| dev-databases |||||| ✓ ||
| dev-diagnose |||||| ✓ ||
| dev-tdd |||||| ✓ ||
| **Python Skills** ||||||||
| python-async-patterns |||||| ✓ ||
| python-code-style |||||| ✓ ||
| python-configuration |||||| ✓ ||
| python-design-patterns |||||| ✓ ||
| python-fastapi-templates |||||| ✓ ||
| python-packaging |||||| ✓ ||
| python-testing-uv-playwright |||||| ✓ ||
| **Review Skills** ||||||||
| review-check-correctness |||| ✓ | ✓ |||
| review-e2e-testing-patterns |||| ✓ ||||
| review-simplify-complexity |||| ✓ ||||
| review-systematic-debugging ||||| ✓ |||
| review-webapp-testing |||| ✓ ||||
| **Orchestration Skills** ||||||||
| orchestrate-dispatching-parallel-agents ||||||||✓ |
| orchestrate-executing-plans ||||||||✓ |
| orchestrate-finishing-a-development-branch ||||||||✓ |
| orchestrate-multi-agent-patterns |||| ✓ ||||✓ |
| orchestrate-subagent-driven-development |||| ✓ ||||✓ |
| **General Skills** ||||||||
| general-grill-me | ✓ ||||||
| general-python-environment |||||| ✓ ||
| general-solid |||| ✓ | ✓ |||
| general-system-design |||| ✓ ||||
| general-verification-before-completion | ✓ ||||| ✓ ||
| **Other Skills** ||||||||
| docker-expert |||||| ✓ ||
| security-review ||||| ✓ |||
| spec-product-requirement-formats | ✓ ||||||

## Notes

- **matd-requirements-engineer**: TBD — NFR-focused skills to be defined
- **matd-orchestrator**: Installed for compatibility; not used in Claude Code native workflows
- **Skill Access Control**: Use `disallowedTools` in agent config to restrict skill access per-agent
- **MCP Access**: Only matd-product-manager gets Jira MCP (scoped inline via agent config)

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

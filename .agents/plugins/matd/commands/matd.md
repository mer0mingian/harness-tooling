---
description: Start MATD (Multi-Agent Test-Driven Development) workflow. Orchestrates requirements analysis, architecture design, QA planning, and implementation with specialized agents. Use when starting a new feature with TDD methodology.
disable-model-invocation: true
---

# MATD Workflow

Start the Multi-Agent Test-Driven Development workflow.

Invoke the matd-orchestrator agent to coordinate the full TDD workflow:

```
/agent matd-orchestrator
```

The orchestrator will guide you through:
1. **Requirements** - Specifier agent clarifies and documents requirements
2. **Architecture** - Architect designs technical approach
3. **QA Planning** - QA agent defines test strategy
4. **Implementation** - Dev agent implements with TDD
5. **Critical Review** - Critical thinker validates approach

The workflow uses parallel agent execution where possible and includes approval gates at each phase.

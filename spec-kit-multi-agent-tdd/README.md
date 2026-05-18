# MATD SpecKit Extension

Multi-Agent Test-Driven Development workflow extension for GitHub SpecKit.

## Overview

Adds AI-powered test-driven development workflows to SpecKit with enforced TDD cycles and multi-agent orchestration:

- **RED → GREEN → REFACTOR enforcement** - Constitutional constraints prevent code-before-tests
- **Multi-agent orchestration** - matd-qa, matd-dev, matd-architect, matd-critical-thinker agents
- **Evidence-based commits** - Validation chain ensures test artifacts exist before code
- **Parallel reviews** - Architecture and code reviews run independently with convergence detection
- **10 artifact templates** - Solution designs, ADRs, test strategies, feature specs, review reports
- **Quality gates** - Automatic convergence detection, test coverage validation

## Installation

### Prerequisites

- SpecKit >= 0.1.0
- Python 3.9+ with pytest
- Claude Code or compatible AI agent with matd plugin

### Install the Extension

```bash
# From SpecKit catalog (once published)
specify extension install matd-tdd

# Or from local source
cd /path/to/spec-kit-multi-agent-tdd
specify extension install .
```

### Configure Test Environment

Create `matd-config.yml` in your project root:

```yaml
test_framework: pytest
test_dir: tests/
artifact_dirs:
  test_strategies: .specify/bmad/test-strategies/
  solution_designs: .specify/bmad/solution-designs/
  adrs: .specify/bmad/adrs/
```

## Quick Start

### 1. Specify Product Requirements

```bash
specify matd:specify-product-brief "VTT character management"
```

Creates structured product brief with user stories and acceptance criteria.

### 2. Design Solution

```bash
specify matd:specify-solution-design "character_creation" \
  --product-brief .specify/bmad/product-briefs/vtt-character-management.md
```

Generates solution design with architecture decisions and test strategy.

### 3. Run TDD Cycle

```bash
# RED: Create failing test
specify matd:test character_creation --strategy .specify/bmad/test-strategies/character_creation.md

# GREEN: Implement minimal code
specify matd:implement character_creation

# REFACTOR: Improve code quality
specify matd:review character_creation --type code
```

### 4. Commit with Evidence

```bash
specify matd:commit "Implement character creation" \
  --test-files tests/test_character_creation.py \
  --code-files src/character.py
```

Validates evidence chain before allowing commit.

## Workflow Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `matd:test` | Write/update tests | RED phase enforcement, test strategy alignment |
| `matd:implement` | Implement code | GREEN phase enforcement, test-first validation |
| `matd:review` | Run reviews | Parallel arch + code reviews, convergence detection |
| `matd:commit` | Commit changes | Evidence chain validation, constitutional constraints |
| `matd:update-docs` | Update documentation | C4 diagrams, API docs, ADRs |
| `matd:specify-product-brief` | Create product brief | User stories, acceptance criteria |
| `matd:specify-adr` | Create ADR | Architecture decisions with context |
| `matd:specify-solution-design` | Design solution | Architecture + test strategy |

## Constitutional Constraints

MATD enforces TDD discipline through validation rules:

- **RED Phase**: Only test files may be modified
- **GREEN Phase**: Requires failing test artifacts before code changes
- **REFACTOR Phase**: Must have passing tests before quality improvements
- **Commit**: Requires complete evidence chain (test strategy → tests → code → reviews)

## Multi-Agent Roles

- **matd-qa**: Test strategy, test implementation, test validation
- **matd-dev**: Code implementation, refactoring, integration
- **matd-architect**: Solution design, ADRs, architecture review
- **matd-critical-thinker**: Quality assessment, convergence detection, evidence validation

## Integration with Code Graph Context

MATD artifacts are automatically indexed in CGC for:
- Cross-artifact navigation (test strategies → tests → code)
- Impact analysis (changed code → affected tests)
- Traceability (requirements → design → implementation)

## Documentation

See [USER-GUIDE.md](USER-GUIDE.md) for complete workflow documentation, examples, and troubleshooting.

## Project Structure

```
.specify/bmad/
├── product-briefs/       # Product requirements and user stories
├── solution-designs/     # Architecture and implementation plans
├── test-strategies/      # Test approach for each feature
├── adrs/                 # Architecture Decision Records
├── feature-specs/        # Detailed feature specifications
└── reviews/              # Architecture and code review reports

tests/                    # Test implementations
src/                      # Code implementations (must have tests first)
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

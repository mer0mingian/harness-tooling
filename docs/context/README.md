# Context Documents

Reference materials for grilling sessions and design validation.

## Purpose
This directory contains distilled knowledge from research, subagent investigations, and architectural decisions. Use these documents during grilling sessions to challenge designs against known constraints and established patterns.

## Documents

### Agent Configuration
- **[agent-restrictions-learnings.md](agent-restrictions-learnings.md)** - Priority levels, tool restriction syntax, MCP scoping, memory loading

### SpecKit Extension Design
- **[speckit-preset-mechanism.md](speckit-preset-mechanism.md)** - Command override syntax, priority-based resolution, preset installation

### Workspace Standards
- **[workspace-template-structure.md](workspace-template-structure.md)** - Canonical folder hierarchy, path mappings, extension alignment requirements

### Historical Decisions
- **[stdd-skills-analysis.md](stdd-skills-analysis.md)** - STDD→MATD migration decisions, skill naming conventions, deleted vs renamed skills

## Usage

**During grilling sessions:**
1. Reference relevant context documents when challenging design decisions
2. Quote specific constraints or patterns to ground the discussion
3. Update documents when new learnings emerge from the session

**When designing new features:**
1. Check alignment with workspace template structure
2. Verify agent restrictions match documented patterns
3. Follow naming conventions from historical decisions

## Maintenance
- Update documents when subagent research reveals new information
- Add new context documents for recurring design questions
- Archive outdated documents with clear deprecation notices

Created: 2026-06-09

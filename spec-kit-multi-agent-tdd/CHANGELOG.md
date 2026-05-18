# Changelog

All notable changes to the MATD SpecKit extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-08

### Added
- Initial release of MATD SpecKit extension
- 8 workflow commands: test, implement, review, commit, update-docs, specify-product-brief, specify-adr, specify-solution-design
- RED → GREEN → REFACTOR TDD cycle enforcement
- Evidence chain validation system
- Parallel review system (architecture + code) with convergence detection
- 10 artifact templates for BMAD methodology
- Constitutional constraint system preventing code-before-tests
- Python validation scripts for TDD phase and evidence validation
- Hook-based installation system for SpecKit integration
- Multi-agent orchestration with matd plugin agents (qa, dev, architect, critical-thinker)
- Test strategy configuration with framework-agnostic design
- Artifact path resolution from config
- Quality gates with automatic convergence detection
- Integration with Code Graph Context for artifact indexing

### Features
- **TDD Enforcement**: Constitutional constraints ensure RED → GREEN → REFACTOR discipline
- **Multi-Agent Workflows**: Specialized agents for QA, development, architecture, and critical thinking
- **Evidence-Based Commits**: Validation chain requires test artifacts before code changes
- **Parallel Reviews**: Independent architecture and code reviews with convergence detection
- **Template Library**: 10 artifact templates for product briefs, ADRs, solution designs, test strategies, reviews
- **Configuration**: `matd-config.yml` for test framework and artifact directory customization
- **Validation Scripts**: Python-based phase validation and evidence chain verification

### Documentation
- Comprehensive USER-GUIDE.md with workflow examples
- Config schema with JSON Schema validation
- Extension metadata in extension.yml and extension.json
- Template configuration file: matd-config.yml.template

### Testing
- pytest-based test suite with fixtures
- Integration tests for command workflows
- Validation script tests for TDD phases

## [Unreleased]

### Planned
- Support for additional test frameworks (vitest, mocha, rspec)
- Enhanced hook system integration with pre-commit validation
- Catalog submission to SpecKit marketplace
- Advanced artifact templates (test plan, retrospective, spike report)
- Integration with external tools (CGC, deepwiki, rtk)
- Version migration tooling for config schema updates
- Performance metrics for TDD cycle times
- Custom validation rule framework for team-specific constraints

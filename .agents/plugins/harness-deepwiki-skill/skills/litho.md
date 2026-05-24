---
name: litho
description: Generate comprehensive C4 architecture documentation using litho (deepwiki-rs) engine
---

# Litho Documentation Generator

Use this skill to generate comprehensive documentation for a codebase, including C4 architecture diagrams (Context, Container, Component, Code levels).

## When to Use

- **Initial project documentation** - Generate complete docs for new or undocumented projects
- **Architecture visualization** - Create C4 diagrams showing system structure
- **Large codebase analysis** - Understand complex projects through generated documentation
- **Documentation updates** - Refresh docs after major architectural changes

## Prerequisites

**REQUIRED:** Litho container must be running. Start with:
```bash
harness up --profile litho
```

If you see "container not found" errors, the litho container is not running.

## Usage

### Basic Documentation Generation

Generate docs in default location (`./litho.docs/`):

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs
```

**Note:** `PROJECT_NAME` is set by harness based on your working directory.

### With Model Selection

Choose specific LLMs for different phases:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.docs \
  --model-efficient gpt-4o-mini \
  --model-powerful claude-sonnet-4
```

**Model Options:**
- Efficient (bulk processing): `gpt-4o-mini`, `gpt-3.5-turbo`
- Powerful (complex analysis): `claude-sonnet-4`, `gpt-4o`, `claude-opus-4`

### Skip Preprocessing (If Already Done)

Preprocessing analyzes file structure and dependencies. Skip if you've run litho before and structure hasn't changed:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  --skip-preprocessing
```

### Skip Research Phase (Quick Test)

Research phase calls LLM APIs (expensive/slow). Skip for testing:

```bash
docker exec harness-litho-${PROJECT_NAME} litho \
  -p /workspace/project \
  -o /workspace/project/litho.test \
  --skip-research
```

## Output Structure

Litho generates:
- `litho.docs/architecture/` - C4 diagrams (mermaid format)
- `litho.docs/components/` - Component documentation
- `litho.docs/context/` - System context and domain model
- `litho.docs/decisions/` - Architecture decision records

## Environment Variables

- `PROJECT_NAME` - Auto-set by harness (e.g., `sta2e-agent-workspace`)
- Container name: `harness-litho-${PROJECT_NAME}`

## Troubleshooting

**Error: "container not found"**
- **Cause:** Litho container not running
- **Fix:** Run `harness up --profile litho` from your project directory

**Error: "permission denied" or "no such file"**
- **Cause:** Path mismatch - litho can't access project files
- **Fix:** Check bind mount in `docker-compose.yml` (should mount workspace to `/workspace`)

**Error: SSL certificate verification failed**
- **Cause:** Corporate proxy issues (Cloudflare/Zscaler)
- **Fix:** Ensure using `litho:stony` image variant (has corporate CA certificates)

**Error: API key not found**
- **Cause:** Litho needs LLM API keys (Anthropic/OpenAI)
- **Fix:** Check environment variables in litho container: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`

## Performance Notes

- **Typical runtime:** 10 seconds to 10 minutes (depends on codebase size and LLM API speed)
- **Docker exec overhead:** ~54ms (negligible compared to LLM API calls)
- **Cost:** Varies by model and codebase size (~$0.10-$5.00 per full generation)

## Related

- Quick start guide: `/workspace/project/assets/skill-litho/quick-start.sh`
- CI integration: `/workspace/project/assets/skill-litho/ci-setup.sh`

# Reference: spec-kit-v-model (V-Model Extension Pack for Spec Kit)

> **Source**: https://github.com/leocamello/spec-kit-v-model
> **Inspected**: 2026-06-08 (commit `ebe73ef`, v0.7.2) — plain clone in `submodules/watching/spec-kit-v-model/` (gitignored, NOT a submodule)
> **License**: MIT
> **Purpose of this doc**: Reference for designing a `speckit-matd-specify-prd` command and a V-model-oriented MATD PDLC. Not a usage manual.

---

## 1. What it is and how it relates to GitHub Spec Kit

It is an **extension pack for [GitHub Spec Kit](https://github.com/github/spec-kit)**, distributed via Spec Kit's extension mechanism (`specify extension add v-model --from <zip>`). It declares itself in `extension.yml` (`schema_version: 1.0`), `requires` `speckit_version >=0.1.0` plus the core `speckit.specify` command, and `provides` 17 namespaced commands (`speckit.v-model.*`) and 4 lifecycle hooks. It does **not replace** core Spec Kit — it layers a V-Model discipline on top of the standard `specify → plan → tasks → implement` flow.

Core thesis (`README`, `docs/v-model-overview.md`): *"Every specification paired with its test. Full traceability."* AI-native teams ship fast but produce no traceability; regulated teams have traceability but move slowly. This pack closes the gap by **paired generation** — every left-side development artifact generates its right-side test counterpart simultaneously, with IDs that encode lineage.

**Division of labour** (the design philosophy worth stealing): *"The AI drafts. The human decides. The scripts verify. Git remembers."*
| What | Who |
|------|-----|
| Generate requirements & test plans | AI + human review |
| Coverage calc & matrix generation | **Deterministic scripts** (regex parsers, no AI) |
| Quality evaluation | LLM-as-judge (advisory only) |
| Audit trail | Git (cryptographic hashes) |

---

## 2. The V-Model: left-side artifact → right-side verification mapping

Four nested design↔test levels descend the left arm of the "V" and ascend the right. Each left artifact has a *simultaneously generated* test counterpart and a dedicated traceability matrix.

| Level | Left (Development / Verification) | Right (Test / Validation) | Standards | Matrix |
|-------|-----------------------------------|---------------------------|-----------|--------|
| 1 | **Requirements** (`requirements.md`) | **Acceptance Test Plan** (`acceptance-plan.md`) | IEEE 29148, ISO 25010, INCOSE | **A** — Validation (user view) |
| 2 | **System Design** (`system-design.md`, 4 IEEE 1016 views) | **System Test** (`system-test.md`, named ISO 29119-4 techniques) | IEEE 1016, ISO 29119-4 | **B** — Verification (architectural view) |
| 3 | **Architecture Design** (`architecture-design.md`, IEEE 42010 / Kruchten 4+1 views) | **Integration Test** (`integration-test.md`, 4 named techniques) | IEEE 42010, ISO 29119-4 | **C** — Integration verification |
| 4 | **Module Design** (`module-design.md`, 4 views) | **Unit Test** (`unit-test.md`, 5 white-box techniques) | IEEE 1016 + ISO/IEC 12207, ISO 29119-4 | **D** — Implementation verification |
| X-cut | **Hazard Analysis** (`hazard-analysis.md`, FMEA) | mitigations → REQ/SYS → tests | ISO 14971, ISO 26262-9, IEC 60812 | **H** — Hazard traceability |

**The traceability trick — IDs encode lineage, no lookup table needed.** Reading an ID tells you its full parent chain:
- `SCN-001-A1` → scenario 1 of test case `ATP-001-A` → validates `REQ-001`.
- Full chain: `UTS-001-A1 → UTP-001-A → MOD-001 → ARCH-001 → SYS-001 → REQ-001`.

ID prefixes (from `extension.yml > defaults.id_prefixes`):
`REQ` (+ `REQ-NF`/`REQ-IF`/`REQ-CN` variants), `ATP`/`SCN` (acceptance), `SYS`/`STP`/`STS` (system), `ARCH`/`ITP`/`ITS` (architecture/integration), `MOD`/`UTP`/`UTS` (module/unit), `HAZ` (hazard), `PRF` (peer-review findings, advisory), `WAV` (waivers). `coverage_threshold: 100`, `batch_size: 5`.

`HAZ` is special: it does **not** participate in parent/child encoding. Each HAZ links to `SYS-NNN` (FMEA Component column) and references `REQ`/`SYS` in its Mitigation column, creating a cross-cutting trace: Hazard → Mitigation → Requirement → Test.

---

## 3. Commands it adds (17) + bridge to implementation

Namespaced `speckit.v-model.*`. Grouped by role:

**Specification (left side):** `requirements` · `system-design` · `architecture-design` · `module-design`
**Test planning (right side):** `acceptance` · `system-test` · `integration-test` · `unit-test`
**Cross-cutting:** `hazard-analysis` (FMEA, operational-state aware) · `impact-analysis` (deterministic downward/upward/full traversal of affected artifacts) · `peer-review` (stateless artifact linter)
**Verification:** `trace` (builds matrices A+B+C+D+H, coverage audit, gap detection) · `test-results` (ingest JUnit + Cobertura XML, 100% deterministic) · `audit-report` (release report w/ waiver cross-ref + compliance gating, deterministic)
**Bridge to core implementation:** `plan` · `tasks` · `implement` (each *wraps* the corresponding `spec-kit-core` command with additive V-Model enrichment + gates)

**Lifecycle hooks** (`extension.yml > hooks`, all optional/prompted):
- `after_specify` → offers `requirements` (bridges core specify into the V-Model chain)
- `after_tasks` → offers `trace`
- `before_implement` → `trace` (pre-impl coverage confirmation)
- `after_implement` → `trace` (refresh matrix)

**Two operating modes** (README §Compliance):
- **Compliant mode**: `v-model.plan → v-model.tasks → v-model.implement`, every step runs the V-Model gates + hallucination guard + trace post-hook. Artifacts must carry `**Status**: Approved`.
- **Hybrid mode (prototyping)**: feeding a V-Model `tasks.md` to *core* `/speckit.implement` round-trips but **bypasses all gates** — explicitly "not evidence of compliance."

**Domain overlays**: `commands/overlays/{iec_62304,iso_26262,do_178c}/` each contain per-command overlay markdown + `_domain.yml`. Set `domain: iec_62304` in `v-model-config.yml`; commands load the overlay and prefer its sections over base defaults.

### Templates / schemas shipped (verbatim structure)

**`requirements.md`** (`templates/requirements-template.md`) — four requirement tables (Functional / Non-Functional / Interface / Constraint, empty categories omitted), each row:

```
| ID | Description | Priority | Rationale | Verification Method |
```

Header carries `**Status**: Draft`. Footer carries summary metrics (Total / By Priority P1-P3 / By Verification Method: Test|Inspection|Analysis|Demonstration). Lifecycle tags inline: `[DEPRECATED — Superseded by REQ-NNN]`, `[DEPRECATED — Withdrawn: <reason>]`, `[SUSPECT — Parent X-NNN {deprecated|modified}]`. **IDs are permanent — never renumbered, never deleted, only deprecated.**

**`acceptance-plan.md`** — per requirement: `### Requirement Validation: REQ-001`, then `#### Test Case: ATP-001-A`, then BDD scenarios:

```
* **User Scenario: SCN-001-A1**
  * **Given** [precondition]
  * **When** [action]
  * **Then** [expected outcome]
```

Plus a **Coverage Summary** table (active/deprecated/suspect counts, `Active Requirements with ≥1 ATP`, `Overall Coverage %`) and an **Uncovered Requirements** section *populated by the validation gate script*.

**`traceability-matrix-template.md`** — five matrices (A/B/C/D/H). Each row carries full lineage + a `Status` cell (`⬜ Untested` / `⏳ Pending` / `⬜ Bypassed`). Marked *"Generated by deterministic script — not AI… Do NOT manually edit."* Includes a **Gap Analysis** section enumerating uncovered + orphaned items at every tier, and **Audit Notes** ("Matrix generated by `build-matrix.sh` (deterministic regex parser)").

---

## 4. How it tests / validates artifact compliance

Three distinct enforcement layers — this separation is the most reusable architectural idea.

**(a) In-prompt quality criteria (content gates inside the command).** `requirements.md` enforces the **INCOSE / IEEE 29148 8-criterion checklist** verbatim, each criterion is non-negotiable and includes a "Check" rewrite test: 1 Unambiguous, 2 Testable/Verifiable, 3 Atomic, 4 Complete, 5 Consistent, 6 Traceable, 7 Feasible, 8 Necessary. Plus a **banned-words table** (fast→time threshold, robust→failure behavior, scalable→load target, secure→specific measure, etc.) and an ISO/IEC 25010 quality-characteristics coverage check. The command runs under a **"strict translator constraint"**: extract/formalize from source only — never invent, infer, or gold-plate. Flags `[NEEDS CLARIFICATION]` (max 3), `[CONFLICT]`, `[FEASIBILITY CONCERN]`.

**(b) Deterministic validation scripts (bash + PowerShell parity, no AI).** `scripts/{bash,powershell}/` ship parallel implementations. Regex parsers extract IDs and cross-reference for coverage. Key validators: `validate-requirement-coverage`, `validate-system-coverage`, `validate-architecture-coverage`, `validate-module-coverage`, `validate-hazard-coverage`, `validate-artifact-status` (enforces `Status: Approved` since v0.7.0), `validate-domain-profile`, `validate-core-schema`, `validate-level`, `validate-implements-ids`. Exit codes: `0 = full coverage`, `1 = gaps`.

The orchestrator **`run-v-model-gate.sh <feature-dir>`** runs an **8-stage pre-implementation gate** in order: `validate-artifact-status → validate-domain-profile → build-matrix → validate-requirement-coverage → validate-system-coverage → validate-architecture-coverage → validate-module-coverage → validate-hazard-coverage`. Prints per-stage PASS/FAIL and a final `GATE: PASS` / `GATE: FAIL` (exit 1).

**`validate-implements-ids.sh` — the hallucination guard.** Extracts the canonical V-Model ID set from the source-of-truth artifacts, then scans generated code for `Implements <ID>` comments and fails closed (`GUARD: FAIL`, exit 1, `<file>:<line>: unknown id <X>`) if any cited ID is not canonical. This is how it stops the LLM inventing trace links. (Notably, the V-Model scripts themselves carry `# Implements: REQ-…, SYS-…` headers — the tool dogfoods its own traceability.)

**(c) Stateless AI linter — `peer-review`.** "ESLint/SonarQube for V-Model artifacts." Reviews one artifact against type-specific, standards-based criteria (IEEE 1028:2008 review types + ISO/IEC 20246:2017 defect taxonomy: Missing/Wrong/Superfluous/Incomplete/Inconsistent/Ambiguous). Emits `PRF-{ARTIFACT}-NNN` findings with severity Critical/Major/Minor/Observation. **Stateless** — regenerated each run, output overwritten, no `Status` field ("if it's in the report, it's a current problem"); git diff shows progress. Findings are **advisory-only** — excluded from traceability matrices and coverage. CI mapping: Critical/Major → exit 1 (blocks PR), Minor → exit 2 (warning), clean/Observation → exit 0.

**(d) Test suite proving the tooling itself** (README §Testing): BATS 455 (bash logic), Pester 431 (PowerShell parity), Structural 89 (ID format, template conformance, section completeness), LLM evals 53 (requirements/BDD/traceability quality), E2E 32 (golden-output fixtures). Layout under `tests/{bats,pester,structural,evals,acceptance,integration,system,validators,fixtures}/`. Ships a `examples/github-actions/v-model-validation.yml` CI workflow.

---

## 5. Reusable ideas for `speckit-matd-specify-prd` + V-Model MATD PDLC

The MATD PDLC envisioned (PRD → Solution Design → specs, each with a verification counterpart) maps almost 1:1 onto this pack's left↔right pairing. Concrete things to lift:

1. **Paired generation as a hard rule.** Make `speckit-matd-specify-prd` emit a PRD *and* its verification counterpart (acceptance criteria / PRD validation plan) in one command, with IDs linking them. MATD already has `matd:specify-solution-design` and `matd:specify-adr` — give each left-side spec a right-side verification artifact and a matrix row. Suggested MATD mapping: **PRD ↔ Acceptance/UAT** (Matrix A), **Solution Design ↔ System/Integration tests** (Matrix B/C), **detailed specs ↔ unit tests** (Matrix D).

2. **Self-documenting hierarchical IDs.** Adopt `PRD-NNN → SD-NNN → ...` style where the child ID embeds the parent, so a trace is readable without a lookup table. This is the single highest-leverage idea: traceability falls out of the ID scheme for free.

3. **Three-layer enforcement, cleanly separated**: (a) in-prompt content gates (the INCOSE 8-criterion + banned-words checklist is directly reusable for PRD quality — drop it into `speckit-matd-specify-prd` to force testable, atomic, unambiguous PRD statements); (b) deterministic non-AI coverage/orphan validators that fail closed; (c) a *stateless advisory* AI linter whose findings never pollute the trace chain. Keeping deterministic gates separate from AI judgment is what makes the audit trail trustworthy.

4. **Templates with a `Status` field + lifecycle tags + machine-populated sections.** `**Status**: Draft → Approved` gated by a script; permanent never-renumbered IDs; `[DEPRECATED — Superseded/Withdrawn]` and `[SUSPECT — Parent modified]` tags for evolution; and "Uncovered/Gap" sections that scripts (not the LLM) fill in. This gives MATD artifacts an audit trail and a clean change-propagation story (`impact-analysis` traverses the trace graph to mark suspects).

5. **The hallucination guard + gate orchestrator pattern.** `validate-implements-ids.sh` (code comments must cite a *canonical* ID or the build fails closed) and `run-v-model-gate.sh` (one orchestrator chaining status → schema → matrix → N coverage validators with a single PASS/FAIL) are directly portable to a MATD `matd:commit`/`matd:review` gate. Also worth copying: the **compliant-vs-hybrid mode** distinction (gates leave a git record; bypassing them is explicitly "not evidence of compliance") and **domain overlays** for any team-specific or regulatory profile layered over a generic base command.

---

## Appendix — local clone location

```
submodules/watching/spec-kit-v-model/   # plain clone, gitignored, not a submodule
├── extension.yml                         # manifest: 17 commands, 4 hooks, id_prefixes
├── commands/*.md                         # command prompts (+ overlays/{iec_62304,iso_26262,do_178c}/)
├── templates/                            # requirements / acceptance-plan / traceability-matrix
├── scripts/{bash,powershell,python}/     # deterministic validators + gate orchestrator (parity)
├── docs/v-model-overview.md              # canonical methodology + ID schema reference
└── tests/{bats,pester,structural,evals,...}
```

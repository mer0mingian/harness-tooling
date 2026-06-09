# Confluence Reference: StepStone "Project Charter"

**Research date:** 2026-06-08
**Access:** Confluence Cloud REST API via api.atlassian.com gateway (cloudId `fb2e8688-33a3-4b12-b92d-4a7e7d308e68`), Basic auth `$CONFLUENCE_USERNAME:$CONFLUENCE_API_TOKEN`. CQL searches: `title ~ "Project Charter"` (15 hits) and `text ~ "Project Charter"` (102 hits).

## Source pages

| Role | Page | ID | Space | URL |
| ---- | ---- | -- | ----- | --- |
| **Authoritative template** | Project Charter Template (5+ Story Points) | `170265460` | Marketplace Enablement (ME) | https://eureka.stepstone.com/spaces/ME/pages/170265460/Project+Charter+Template+5+Story+Points |
| **Governing framework** | Inception Principles - Project Canvas & Charter Framework | `170265569` | ME | https://eureka.stepstone.com/spaces/ME/pages/170265569/Inception+Principles+-+Project+Canvas+Charter+Framework |
| Legacy/archived variant | Project Charter Template | `117008480` | Connect Platform (AATSI) | https://eureka.stepstone.com/spaces/aatsi/pages/117008480/Project+Charter+Template |

**Why the ME template is authoritative:** It is live under `Marketplace Enablement Home > Inception Outputs > Inception Process & Templates [WIP]`, is by far the richest (50 KB, 12 sections, 20 tables), and is paired with the explicit principles/framework page `170265569`. The AATSI page `117008480` is a thin 7-section legacy doc located under `Connect Platform Home > 🗿 Archived > To delete > ...` and should be treated as deprecated.

---

## Where the Project Charter lives

- **Space:** Marketplace Enablement (`ME`).
- **Location:** `Inception Outputs > Inception Process & Templates [WIP]`.
- The Charter is one of two paired Inception artifacts (Canvas + Charter). The **Canvas** is an at-a-glance dashboard embedded at the top of the Charter; the **Charter** is the full document. Both are intended to be **living documents** (updated continuously), not write-once archives.

---

## Full section structure (headings verbatim) — Template `170265460`

```
H1  [Initiative Name] - Project Charter
H2  SDP Epic & Related SDPs
H2  Section 0: Canvas Quick Reference
H2  Section 1: Vision & Why
    H3 Purpose
    H3 Business Value
    H3 Success Criteria
H2  Section 2: Scope & Deliverables
    H3 In Scope
    H3 Out of Scope
    H3 Key Deliverables & Owners
    H3 Dependencies
H2  Section 3: Solution Approach
    H3 Technical Approach
    H3 Architecture Involvement
    H3 Key Technical Decisions (ADRs)
    H3 Technology Choices
H2  Section 4: Investment & Cost
    H3 Estimated Cost
    H3 Investment Breakdown
    H3 Timeline & Milestones
H2  Section 5: Stakeholders & RACI
    H3 RACI Matrix
    H3 Core Team Roles
    H3 Accountable (Decision Makers)
    H3 Consulted (Key Contributors)
    H3 Informed (Stakeholders)
    H3 Stakeholder Engagement Plan
H2  Section 6: Risks & Issues
    H3 Risk Register
    H3 Common Risk Categories Checklist
    H3 Issues Log
    H3 Risk Review Schedule
H2  Section 7: Compliance & Governance
    H3 GDPR & Data Privacy
    H3 AI/ML Compliance
    H3 Security Review
    H3 Architecture Review
H2  Section 8: Quality & Non-Functional Requirements (NFRs)
    H3 Critical System Classification
    H3 Testing Strategy
    H3 Monitoring & Observability
    H3 Key Non-Functional Requirements
H2  Section 9: Success Metrics & Measurement
    H3 Key Metrics
    H3 Metric Categories
    H3 Measurement Timeline
    H3 Measurement Responsibility
    H3 Success Evaluation
H2  Section 10: Policies & Processes Affected
    H3 System Registration & Documentation
    H3 Data Contracts
    H3 Documentation Requirements
    H3 Process Changes
H2  Section 11: Relevant Links & Resources
    H3 Systems & Infrastructure / Code & Technical Artifacts / Architecture & Design /
       Data & Contracts / Planning & Collaboration / Testing & Quality / Related Initiatives
H2  Lifecycle & Maintenance
    H3 Document Status Transitions
    H3 Maintenance Schedule
H2  Change Log
H2  Notes & Appendices
    H3 Workshop Outputs / Appendices / Follow-Up Actions
```

### Table / field schema (20 tables)

| # | Section | Column headers |
| - | ------- | -------------- |
| 0 | Key Deliverables & Owners | Deliverable, Description, Owning Team, Target Date, Status |
| 1 | Dependencies | ID, Dependency, Type, Dependent Team/System, Contact, Status, Risk, Notes |
| 2 | Key Technical Decisions | Decision, ADR Link, Status, Date, Owner |
| 3 | Technology Choices | Technology, Purpose, Tech Radar Status, Notes, Approval |
| 4 | Investment Breakdown | Team, Role, Allocation, Duration, Cost, Notes |
| 5 | Timeline & Milestones | Phase, Milestone, Target Date, Status, Key Deliverables, Dependencies |
| 6 | RACI Matrix | Activity/Decision, Product Lead, Tech Lead, EM, Architect, QA, Security, Legal, Other |
| 7 | Core Team Roles | Role, Name(s), Responsibilities, Time Commitment |
| 8 | Accountable | Role, Name, Decision Authority |
| 9 | Consulted | Role, Name, Contribution, Engagement Approach |
| 10 | Informed | Stakeholder, Role/Team, Interest/Concern, Communication Plan |
| 11 | Stakeholder Engagement Plan | Stakeholder, Why Engage, How to Engage, Frequency, Owner |
| 12 | Risk Register | ID, Risk Category, Description, Likelihood, Impact, Risk Score, Treatment, Mitigation Plan, Owner, Status, Last Updated |
| 13 | Issues Log | ID, Issue, Impact, Root Cause, Resolution Plan, Owner, Status, Target Resolution |
| 14 | Testing Strategy | Test Type, Scope, Coverage Target, Tools, Owner, Status |
| 15 | Key NFRs | NFR Category, Requirement, Target, Measurement, Priority, Status |
| 16 | Key Metrics | Metric, Description, Baseline, Target, Measurement Approach, Dashboard Link |
| 17 | Process Changes | Process Name, Type of Change, Impact, Owner, Change Plan Link, Status |
| 18 | Change Log | Date, Section Changed, Change Description, Updated By, Reason |
| 19 | Follow-Up Actions | Action, Owner, Due Date, Status |

### Selected field semantics (from template body text)

- **SDP Epic & Related SDPs** — header linking the Charter to its Jira SDP Epic / SDP tickets (one per contributing team/component).
- **Section 0 Canvas Quick Reference** — embedded "at-a-glance dashboard" macro at the top of the Charter.
- **Business Value** — `Value Type` checkboxes (☐ Revenue Generation | ☐ Cost Savings | ☐ Efficiency Gains | ☐ Strategic Capability), `Quantified Value` (e.g. "€500k additional revenue in 12 months"), and a `Value Realization Timeline` (T+0 / T+3 / T+6 / T+12 months).
- **Success Criteria** — measurable "what does done look like" checklist.
- **Critical System Classification** — ☐ Yes / ☐ No; if Yes the **Critical Systems Policy** applies (higher availability, rigorous testing, enhanced monitoring, incident response).

---

## Business-invariant content captured

The Charter is StepStone's container for the **stable, business-level facts** of an initiative (as opposed to the implementation-level Specification Document / Jira tickets):

- **Why / Vision** — business problem, strategic alignment, quantified business value, value realization timeline.
- **Success definition** — success criteria + measurable success metrics (baseline/target/dashboard) and how success is evaluated.
- **Scope** — explicit In/Out of scope, key deliverables with owning teams, cross-team dependencies.
- **Investment & cost** — estimated cost, per-team/role investment breakdown, timeline & milestones.
- **Stakeholders & governance** — RACI across Product/Tech/EM/Architect/QA/Security/Legal, decision-makers (Accountable), engagement plan.
- **Risk & compliance** — risk register, GDPR/data-privacy, AI/ML compliance, security & architecture review gates.
- **Quality invariants** — Critical System classification, NFRs, testing strategy, monitoring.
- **Policy/process impact** — system registration, data contracts, documentation requirements, affected processes.

### Framework principles (from `170265569`) that constrain the Charter

- **Canvas vs Charter vs Specification** are distinct artifacts: Canvas = quick context dashboard; Charter = business invariants + governance; Specification = implementation detail that translates to tickets.
- **Living documents, not archives** — must be kept current; lifecycle states tracked (draft → active → etc.).
- **Right-size to complexity** — the "5+ Story Points" template is the heavyweight form; smaller initiatives use a lighter canvas-only approach (Initiative Size → Approach → Duration → Output table).
- **Terminology rule:** use "Specifications", NOT "Requirements".
- **Architecture consultation triggers** govern when an Architect must be involved.

---

## Mapping to a "project brief = business invariants" command

A future `/project-brief` (business-invariants) command should mirror the **stable, slow-changing** subset of this Charter and deliberately exclude implementation detail (which belongs in the Specification / tickets):

| Project-brief field | Source in Charter |
| ------------------- | ----------------- |
| Purpose / problem statement | Section 1 Purpose |
| Strategic alignment | Section 1 Purpose → Strategic Alignment |
| Business value (type + quantified + realization timeline) | Section 1 Business Value |
| Success criteria & metrics | Section 1 Success Criteria + Section 9 Key Metrics |
| In / Out of scope | Section 2 In Scope / Out of Scope |
| Key stakeholders & decision-makers | Section 5 Accountable + Core Team Roles |
| Constraints: budget/cost | Section 4 Estimated Cost / Investment |
| Governance & compliance invariants | Section 7 (GDPR, AI/ML, Security, Architecture) |
| Critical-system / NFR invariants | Section 8 Critical System Classification + Key NFRs |

**Guidance for the command:** capture the Canvas-level "quick reference" first (Section 0 + Section 1) as the minimal business brief; treat RACI, risk register, testing strategy, and links as optional depth scaled to initiative size (per the framework's "right-size to complexity" rule). Keep "Specifications" terminology, and treat the brief as a living document with a Change Log.

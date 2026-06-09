# Architecture Designs (Solution Design) — StepStone Enterprise Architecture

> **Source:** https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205793182/Architecture+Designs
> **Space:** ARCH — StepStone Enterprise Architecture (parent: EA Design Authority)
> **Page version:** 47 (last edited 2026-06-03)
> **Fetched:** 2026-06-08 via Confluence Cloud REST API (export_view), converted with pandoc.
> **Status:** Verified — Owner: Kamil Zurawski — Review date 2026/03/31

---

|             |                                                                                                                                                      |                 |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| **Status**  | **Owner**                                                                                                                                            | **Review Date** |
| 🟢 Verified | [Kamil Zurawski](https://stepstone.atlassian.net/wiki/people/557058:6c841205-f557-4c55-929f-13ffb90b61a9?ref=confluence)  | 2026/03/31      |

# What is Solution (Architecture) Design?

Solution Design is a structured approach to planning how we will build a solution before implementation begins. It translates business requirements into a concrete technical plan covering architecture, costs, resources, risks, and key trade-offs.

It acts as a blueprint for construction: defining what we are building, how the components fit together, what resources are required, how much it will cost, and what challenges we may face. Just as construction does not begin without architectural plans, significant technical work should not start without a Solution Design.

Solution Design is intentionally an **umbrellaartefact**. It is broader than traditional “System Design” and spans multiple engineering domains. Depending on the scope, it can be realised through a combination of:

- **System Design:** application architecture, services, APIs, integrations

- **Data Engineering Design:** data models, pipelines, storage, processing

- **Infrastructure Design:** cloud resources, networking, scalability, reliability

- **Frontend Design:** user interfaces, client-side architecture, user experience

By bringing these perspectives together, Solution Design captures system-level thinking and provides a cohesive, end-to-end view of the solution.

This checkpoint ensures a shared understanding across engineering, product, and leadership of what we are building, why we are building it this way, and what we are committing to deliver.  

Template: [Solution Design Template](https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205853106/Solution+Design+Template)

------------------------------------------------------------------------

# When do we need Solution Design?

You **must** create a Solution Design when:

1.  Starting a new objective aligned with top-level OKRs (creating an SDP ticket)

2.  Impact spans multiple teams - the change requires coordination or affects other teams' systems

3.  Substantial investment - the work represents significant time or effort (typically more than 2-3 sprints)

4.  Landscape changes - introducing a new service, component, or external dependency

Optional, but recommended:

You *may* create a Solution Design when:

- Complex technical decisions need to be documented for future reference

- The team sees value in formalising the approach, even for smaller work

- Architectural decisions will set precedents for future work

# Who is responsible?

## Core roles & responsibilities

| Role | Primary Responsibility | Key Activities |
|---|---|---|
| Staff Engineer | Owns the delivery of the Solution Design document and all required outputs | • Creates first draft of solution context (FRs/NFRs)<br>• Leads trade-off analysis<br>• Creates C4 System/Container diagrams<br>• Designs data architecture and flows<br>• Produces cost estimates<br>• Drives team collaboration and synthesis |
| Product Manager | Owns functional requirements and validates scope alignment | • Defines and owns FRs<br>• Understands critical NFRs and their delivery impact<br>• Validates business capability alignment<br>• Balances scope, cost, and delivery commitments |
| Engineering Manager | Ensures quality process and team involvement | • Ensures FR/NFR rigour and completeness<br>• Validates feasibility and scope coherence<br>• Reviews for maintainability and predictability<br>• Ensures healthy team participation |
| Engineering Director | Confirms strategic alignment and resource commitment | • Ensures consistency across teams<br>• Approves critical or risky designs<br>• Makes strategic cost and risk decisions<br>• Confirms resource availability |
| Engineering Team | Contributes technical expertise and validates implementability | • Reviews FRs/NFRs for clarity and feasibility<br>• (LLD) Creates detailed data flows, data models and sequence diagrams<br>• Validates that the architecture is implementable<br>• Flags complexity, constraints, and operational risks<br>• Actively participates in design discussions |
| Principal Engineer / Enterprise Architect | Reviews and approves technical quality and alignment | • Defines enterprise/platform NFRs<br>• Sets architectural direction and standards<br>• Reviews complex or high-risk designs<br>• Mentors Staff Engineers<br>• Resolves cross-team conflicts |

## Collaboration Model

Solution Design is **not a solo activity**. The Staff Engineer drives the process, but:

- **The engineering team** actively contributes implementation insights and challenges assumptions

- **Product Manager** partners closely to clarify requirements and trade-offs

- **Engineering Manager** ensures healthy team participation throughout

- **Principal Engineer** provides mentorship and validates the strategic direction

------------------------------------------------------------------------

# What Gets Produced?

The Solution Design document must include the following artefacts: 

## 1. Solution Context: Functional & Non-Functional Requirements

**What it is**: Clear definition of what the system must do (FRs) and how well it must do it (NFRs)

**Who creates it**:

- **Staff Engineer** produces the first draft and ensures completeness

- **Product Manager** owns FRs

- **Principal Engineer** defines enterprise/platform NFRs

- **Engineering Team** reviews for clarity and feasibility

**Content includes**:

- Functional requirements: user interactions, workflows, data inputs/outputs, integration points

- Non-functional requirements: performance, scalability, availability, security, compliance, data retention

- Critical NFRs that impact scope and timeline are explicitly called out

**Acceptance**: FRs and NFRs are complete, clear, and validated against business needs and technical constraints

**Bonus, Out of Scope**: A dedicated table lists features and requirements that will not be delivered, covering both functional and non-functional items. Each entry uses either a dedicated OOS ID or references the related requirement ID. This sets clear boundaries, prevents scope creep, and makes sure stakeholders agree on what the project will not address.

### Functional Requirements

|                  |                 |                       |           |              |              |               |                 |
|------------------|-----------------|-----------------------|-----------|--------------|--------------|---------------|-----------------|
| **ID**           | **Process**     | **Requirement**       | **Actor** | **Priority** | **Arch**     | **Jira**      | **Jira Status** |
| *{DOMAIN}-{NNN}* | *Business area* | *One clear statement* | *Actor*   | *MoSCoW*     | *✓ or empty* | *Ticket link* | *Live status*   |

#### Column Definitions

|                 |                                                |                                                                                                                                          |
|-----------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| **Column**      | **Description**                                | **Values / Convention**                                                                                                                  |
| **ID**          | Unique requirement identifier                  | `{DOMAIN_PREFIX}-{NNN}` — e.g., `CONF-001`, `SQ-CREATE-001`, `FR-ED-001`. Prefix groups by domain or functional area.                    |
| **Process**     | Groups requirements by business area           | Free text — e.g., “Agent Configuration”, “Creating SQ”, “Display”, “Integration”                                                         |
| **Requirement** | What the system must do                        | One clear, testable statement. Start with “System shall...” or “Recruiter can...”                                                        |
| **Actor**       | Who triggers or benefits from this requirement | `System` / `Recruiter` / `Candidate` / `Admin` / `Customer Service`                                                                      |
| **Priority**    | MoSCoW classification                          | MUST / SHOULD / COULD / WON'T                                                                                                            |
| **Arch**        | Satisfied by current architecture design?      | ✓ = yes, empty = not yet addressed                                                                                                       |
| **Jira**        | Link to Jira story/epic                        | Hyperlinked ticket key (e.g., [PIR-622](https://stepstone.atlassian.net/browse/PIR-622)) or — if no ticket yet |
| **Jira Status** | Current status from Jira                       | `To Do` / `In Progress` / `In Review` / `Done` / `—`                                                                                     |

#### Example

|                |                     |                                                                                                               |           |              |          |                                                                                         |                 |
|----------------|---------------------|---------------------------------------------------------------------------------------------------------------|-----------|--------------|----------|-----------------------------------------------------------------------------------------|-----------------|
| **ID**         | **Process**         | **Requirement**                                                                                               | **Actor** | **Priority** | **Arch** | **Jira**                                                                                | **Jira Status** |
| CONF-001       | Agent Configuration | New jobs use template config with MSQ+GAP+Assessment enabled by default                                       | System    | MUST         | ✓        | [PIR-622](https://stepstone.atlassian.net/browse/PIR-622)     | DISCARDED       |
| LEGACY-001     | Agent Configuration | Existing jobs (pre-activation) do NOT auto-activate SQ agent                                                  | System    | MUST         | ✓        | [NH-6874](https://stepstone.atlassian.net/browse/NH-6874)     | DONE            |
| MULTI-CONF-002 | Agent Configuration | Recruiter can switch off SQ+GAP agent; stops SQ for new applicants; in-progress candidates can still complete | Recruiter | MUST         | ✓        | [PIR-623](https://stepstone.atlassian.net/browse/PIR-623)     | DISCARDED       |
| SQ-CREATE-001  | Creating SQ         | Up to 10 questions per job; hard block with error when limit reached                                          | Recruiter | MUST         | ✓        | —                                                                                       | —               |
| SQ-CREATE-002  | Creating SQ         | Types: Yes/No, MC (single), Multiple Select, Free Text short/long, Numeric, Date, Dropdown                    | Recruiter | MUST         | ✓        | —                                                                                       | —               |
| SQ-TPL-001     | Templates           | Save question sets as named templates; company-scoped (visible to all recruiters in same company account)     | Recruiter | SHOULD       | ✓        | —                                                                                       | —               |
| SQ-DISP-001    | Display             | SQs displayed inline within apply flow (not separate page)                                                    | Candidate | MUST         | ✓        | —                                                                                       | —               |
| SQ-STORE-001   | Collecting Answers  | Answers auto-saved immediately after each question response                                                   | Candidate | MUST         | ✓        | —                                                                                       | —               |
| SQ-CONN-001    | Integration         | Screening answers passed to Talent Assessment via synchronous API call                                        | System    | MUST         | ✓        | [ATSI-6328](https://stepstone.atlassian.net/browse/ATSI-6328) | IN PROGRESS     |
| ACCESS-001     | Access              | Create/modify/disable SQ permitted for any recruiter in same company account                                  | Recruiter | MUST         | ✓        | —                                                                                       | —               |

### Non-functional Requirements

#### Template

|               |                 |                     |                    |                       |
|---------------|-----------------|---------------------|--------------------|-----------------------|
| **ID**        | **Category**    | **Requirement**     | **Target**         | **Status**            |
| *{CAT}-{NNN}* | *Category name* | *Quality attribute* | *Measurable value* | *Confirmation status* |

#### Column Definitions

|                 |                                        |                                                                                                                                                                                                             |
|-----------------|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Column**      | **Description**                        | **Values / Convention**                                                                                                                                                                                     |
| **ID**          | Unique NFR identifier                  | `{CATEGORY_PREFIX}-{NNN}` — e.g., `PERF-001`, `SEC-001`, `AVAIL-001`                                                                                                                                        |
| **Category**    | NFR category                           | `Performance` / `Availability` / `Scalability` / `Security` / `Data Retention` / `Compliance` / `Observability` / `Recoverability` / `Usability` / `Documentation` / `Architecture` / `Resilience` / `Cost` |
| **Requirement** | Quality attribute being specified      | Clear description of what is being measured or constrained                                                                                                                                                  |
| **Target**      | Measurable value or standard reference | e.g., `< 2.5s`, `99.9%`, `OWASP Top 10`, `Enterprise standard`                                                                                                                                              |
| **Status**      | Confirmation level                     | CONFIRMED = validated with team/PE \| ASSUMPTION = needs confirmation \| TBD = unknown                                                                                                                      |

#### Standard Category Prefixes

|            |                                                                               |
|------------|-------------------------------------------------------------------------------|
| **Prefix** | **Category**                                                                  |
| `PERF`     | Performance (latency, throughput, Core Web Vitals)                            |
| `AVAIL`    | Availability (uptime SLA)                                                     |
| `SCALE`    | Scalability (horizontal, capacity, elasticity)                                |
| `SEC`      | Security (auth, encryption, input validation, audit)                          |
| `DATA`     | Data Retention (TTL, backup, ownership)                                       |
| `GDPR`     | Compliance (GDPR, right-to-erasure)                                           |
| `OBS`      | Observability (logging, monitoring, alerting, tracing)                        |
| `REC`      | Recoverability (RTO, RPO, failover)                                           |
| `USA`      | Usability (browser support, mobile, accessibility, i18n)                      |
| `DOC`      | Documentation (API specs, architecture docs)                                  |
| `ARCH`     | Architecture (bounded contexts, communication patterns, extensibility)        |
| `RES`      | Resilience (CAP trade-off, consistency model, failure isolation, idempotency) |
| `COST`     | Cost (optimisation, efficiency)                                               |

#### Example (from MSQ DE)

|           |                |                                  |                                                               |            |
|-----------|----------------|----------------------------------|---------------------------------------------------------------|------------|
| **ID**    | **Category**   | **Requirement**                  | **Target**                                                    | **Status** |
| PERF-001  | Performance    | LCP — candidate-facing page load | \< 2.5s                                                       | CONFIRMED  |
| PERF-002  | Performance    | INP — interaction responsiveness | \< 200ms                                                      | CONFIRMED  |
| PERF-003  | Performance    | CLS — layout stability           | \< 0.1                                                        | CONFIRMED  |
| PERF-004  | Performance    | Auto-save API p95                | \< 300ms                                                      | ASSUMPTION |
| AVAIL-001 | Availability   | Uptime                           | 99.9%                                                         | ASSUMPTION |
| SEC-001   | Security       | Access control                   | Company-account-scoped recruiter role                         | CONFIRMED  |
| SEC-002   | Security       | Input sanitization               | OWASP Top 10                                                  | CONFIRMED  |
| DATA-001  | Data Retention | Draft answers                    | 3 days; deleted on job close or SQ disable                    | CONFIRMED  |
| DATA-002  | Data Retention | Submitted answers                | 5 years                                                       | CONFIRMED  |
| GDPR-001  | Compliance     | Right-to-erasure                 | Existing platform pipeline, account ID scope                  | CONFIRMED  |
| OBS-001   | Observability  | Monitoring                       | DataDog dashboards + PagerDuty alerts per enterprise standard | ASSUMPTION |
| REC-001   | Recoverability | RPO / RTO                        | Enterprise standard                                           | ASSUMPTION |

### Out of scope requirements

#### Template

|                     |                    |
|---------------------|--------------------|
| **ID**              | **Description**    |
| *OOS-NNN or req ID* | *What is excluded* |

#### Example (from MSQ DE)

|             |                                                           |
|-------------|-----------------------------------------------------------|
| **ID**      | **Description**                                           |
| OOS-001     | Multi-language question translation                       |
| OOS-002     | Video response questions                                  |
| OOS-003     | Pre-screening before CV submission                        |
| OOS-004     | Analytics funnel dashboard                                |
| OOS-005     | Support SQ for Feed clients                               |
| SQ-COND-001 | Conditional/branching questions based on previous answers |
| CONF-002    | Feed workspace configuration                              |
| SQ-CONN-002 | Feed-delivered MSQ                                        |

## 2. Business Capability Mapping

**What it is**: Mapping of the solution to business capabilities to identify ownership boundaries and prevent overlap

**Who creates it**:

- **Staff Engineer** creates and validates mappings

- **Product Manager** understands alignment for value delivery

- **Engineering Manager** ensures mappings are correct

- **Engineering Director** resolves ownership conflicts

- **Engineering Team** validates that the mappings reflect real system boundaries

**Content includes**:

- Which business capabilities does this solution support

- Ownership boundaries (who owns what)

- Identified gaps or overlaps with other initiatives

- Dependencies on capabilities owned by other teams

**Acceptance**: Clear capability ownership, no unresolved overlaps, dependencies documented

## 3. High-Level Design (HLD)

**What it is**: System architecture showing major components, interactions, and technology choices

**Who creates it**:

- **Staff Engineer** creates C4 System/Container diagrams

- **Engineering Manager** validates feasibility and coherence

- **Engineering Director** approves critical designs

- **Engineering Team** validates implementability

- **Principal Engineer** sets the architectural direction and reviews

**Content includes**:

- C4 System and Container diagrams

- Major components and their responsibilities

- Technology stack choices with rationale

- Deployment model and infrastructure approach

- Scalability limits and failure modes

- Integration patterns with other systems

**Acceptance**: Architecture addresses all requirements, aligns with standards, and is implementable

## 4. Data Architecture

**What it is**: Design of data domains, flows, ownership, and processing

**Who creates it**:

- **Staff Engineer** designs data domains, flows, and ownership

- **Principal Engineer** defines best practices and reviews complex designs

- **Product Manager** understands dependencies affecting delivery

- **Engineering Manager** ensures standards and documentation

- **Engineering Team** contributes detailed flows and validates correctness

**Content includes**:

a\) Data Model Design

- Conceptual/logical data models

- Entity relationships and constraints

- Data domains and ownership

b\) Data Flows

- How data moves through the system

- Transformation points and logic

- Dependencies on external data sources

c\) Data Processing

- Processing pipelines and transformations

- Batch vs. real-time considerations

- Data quality and validation approach

**Acceptance**: Data architecture is complete, follows organisational standards, and operational risks have been identified

## 5. Interfaces

**What it is**: Detailed definitions of how this solution integrates with other systems

**Who creates it**:

- **Staff Engineer** creates clear, detailed interface definitions

- **Principal Engineer** defines interface standards

- **Product Manager** validates that interfaces support delivery

- **Engineering Manager** ensures interfaces are documented and reviewed

- **Engineering Team** refines API/event contracts and validates integration feasibility

**Content includes**:

- API specifications (REST, GraphQL, etc.)

- Event contracts (producers/consumers)

- Integration patterns (synchronous, asynchronous)

- Versioning and backward compatibility strategy

- Authentication and authorization approach

**Acceptance**: Interfaces are complete, follow standards, and integration risks have been identified

## 6. Technology, Patterns & Core Concepts

**What it is**: Technology choices and architectural patterns with justification

**Who creates it**:

- **Staff Engineer** selects technologies and applies patterns, documents rationale

- **Engineering Manager** participates as an equal partner in technology discussions

- **Product Manager** understands the implications on cost and delivery

- **Engineering Team** validates choices are practical and maintainable

- **Principal Engineer** defines preferred patterns and technology usage

**Content includes**:

- Technology stack (languages, frameworks, platforms)

- Architectural patterns applied (microservices, event-driven, etc.)

- Core concepts utilized: scaling strategies, caching approach, sharding, fault tolerance

- Rationale for technology choices

- Trade-offs and risks of chosen approach

**Acceptance**: Technology choices justified, patterns appropriate, team can implement

## 7. Infrastructure Cost Estimate & Trade-offs

**What it is**: Projected costs and explicit technical trade-offs

**Who creates it**:

- **Staff Engineer** creates estimates and trade-off analysis

- **Product Manager** balances cost with scope and delivery

- **Engineering Manager** ensures trade-offs are documented and understands cost considerations

- **Engineering Director** makes strategic cost decisions

- **Engineering Team** highlights operational cost impacts

- **Principal Engineer** advises on long-term economic trade-offs

**Content includes**:

- Compute resources (servers, containers, functions)

- Storage requirements (databases, file storage, caching)

- Network and data transfer costs

- Third-party services (APIs, platforms, tools)

- Monthly and annual projections

- Trade-off analysis: cost vs. performance, speed vs. quality, build vs. buy

- Technical debt considerations

**Acceptance**: Costs estimated, trade-offs explicit and justified, within budget expectations

## 8. Capacity and Resource Plan

**What it is**: Team composition, effort estimate, and timeline

**Who creates it**:

- **Engineering Manager** identifies required skills and estimates effort and ensures the team can cover requirements consistently

- **Engineering Director** confirms resource availability

- **Engineering Team** validates effort estimates based on implementation complexity

- **Staff Engineer** support EM

**Content includes**:

- Team composition needed (engineers, specialists)

- Estimated effort (in person-weeks or story points)

- Timeline with major milestones

- Dependencies on other teams or systems

- Skill gaps and training needs

**Acceptance**: Resource plan is realistic, capacity confirmed, and dependencies identified

## 9. Risk and Dependency Log

**What it is**: Identified risks, dependencies, and mitigation strategies

**Who creates it**:

- **Staff Engineer** identifies and documents risks

- **Principal Engineer** anticipates future systemic risks

- **Engineering Manager** ensures risks are tracked and visible

- **Engineering Director** focuses on organisation-level risks

- **Product Manager** understands risks affecting delivery

- **Engineering Team** raises implementation constraints and operational risks early

**Content includes**:

- Technical risks (scalability, integration complexity, technology maturity)

- Dependencies on other projects, teams, or external systems

- Regulatory and compliance considerations

- Data availability and quality concerns

- Mitigation strategies for each identified risk

- Contingency plans for critical risks

**Acceptance**: Major risks identified, mitigation plans defined, cross-team dependencies resolved

# Acceptance Criteria

The Solution Design is complete and ready for approval when:

### Design Quality

- All artefacts (FRs/NFRs, HLD, data architecture, interfaces, etc.) are complete

- HLD addresses all functional requirements

- HLD satisfies all non-functional requirements

- Architecture choices are justified with a clear rationale

- Design aligns with organisational technical standards

- Business capability mapping is clear with no unresolved overlaps

- Clarity on used Tenant Model

### Feasibility Confirmation

- Data availability verified (sources, quality, access rights)

- Technology choices validated (proven, supportable, licensed)

- Performance targets are achievable with proposed architecture

- The engineering team confirms architecture is implementable

- No unresolved technical blockers

### Cost and Resource Clarity

- Infrastructure costs estimated with documented assumptions

- Cost projections within budget expectations

- Required team capacity confirmed available

- Timeline realistic given resource constraints

- Trade-offs explicitly documented and accepted

### Risk Management

- Major technical risks identified and documented

- Dependencies on other teams/systems mapped and communicated

- Regulatory and compliance impacts assessed

- Mitigation plans outlined for critical risks

- Operational risks (performance, reliability) flagged by engineering team

### Team Collaboration

- Engineering team actively participated in design process

- Team members contributed implementation insights

- Assumptions were challenged and validated

- Shared ownership of design achieved

- Knowledge transfer to team complete

### Stakeholder Alignment

- Principal Engineer or Enterprise Architect has reviewed and approved

- Engineering Director confirms resource availability and strategic alignment

- Engineering Manager validates feasibility, scope coherence, and process quality

- Product Manager confirms FRs are met and understands NFR impact

- Digital Governance team consulted on compliance considerations (light touch) 

# Phases of Solution Design

Solution Design typically follows this workflow (t*imeline varies based on initiative size and complexity):*

| Phase |  |
|---|---|
| #1 Preparation (Week 1) | • Staff Engineer gathers context from PRD outputs and any PoC findings<br>• Product Manager provides detailed FRs or collaborates to create them<br>• Engineering Team reviews business context and raises initial questions<br>• Staff Engineer creates first draft of solution context (FRs/NFRs) |
| #2 Design (Weeks 1-2) | • Staff Engineer creates HLD, data architecture, capability mapping<br>• Engineering Team actively contributes to design, validates implementability and deliver LLD.<br>• Staff Engineer facilitates design sessions with team participation<br>• Engineering Manager ensures healthy collaboration and challenges assumptions |
| #3 Analysis (Weeks 2-3) | • Staff Engineer produces cost estimates and trade-off analysis<br>• Staff Engineer identifies and documents risks and dependencies<br>• Engineering Team highlights operational concerns<br>• Product Manager validates scope and delivery alignment |
| #4 Review (Week 3) | • Engineering Manager reviews for completeness and predictability<br>• Principal Engineer reviews architectural quality and standards compliance<br>• Engineering Director reviews strategic alignment and resource commitment<br>• Revisions based on feedback |

# Tools and Documentation

|                                                                           |                                                                                                                                                                           |
|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Tool**                                                                  | **Purpose**                                                                                                                                                               |
| **Confluence**                                                            | Solution Design document storage and collaboration: [Solution Design Template](https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205853106/Solution+Design+Template) |
| **Jira**                                                                  | Risk and dependency tracking; SDP ticket management                                                                                                                       |
| [draw.io](http://draw.io) | C4 diagrams, data flow diagrams, sequence diagrams                                                                                                                        |
| **Excel or Confluence**                                                   | Cost estimation models                                                                                                                                                    |

# Expected Timeframe

- **Small/Medium initiatives**: 2-3 weeks

- **Large/Complex initiatives**: 4-6 weeks

- Time includes team collaboration, review cycles, and stakeholder alignment

Changelog

|              |             |                                                   |                                                                                                                                                      |                                                                                                                                                                    |                   |
|--------------|-------------|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| **Date**     | **Version** | **Context of Change (trigger & list of changes)** | **Author**                                                                                                                                           | **Approver**                                                                                                                                                       | **Linked to ADR** |
| 31 Mar 2026  | v1.0        | Initial release of Solution Design DoD            | [Kamil Zurawski](https://stepstone.atlassian.net/wiki/people/557058:6c841205-f557-4c55-929f-13ffb90b61a9?ref=confluence)  | [Antoine Craske](https://stepstone.atlassian.net/wiki/people/712020:23348f5b-cac8-4fbb-9000-05cb465fa26f?ref=confluence)  (in progress) |                   |

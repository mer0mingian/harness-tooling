# Confluence Sources for System Constitution (Technical Invariants)

**Date:** 2026-06-08
**Scope:** READ-ONLY Confluence research to seed a *system constitution* = **technical invariants** (NOT business rules).
**Access used:** Confluence Cloud REST API (`$CONFLUENCE_URL` = `api.atlassian.com/ex/confluence/...`, web base `https://stepstone.atlassian.net/wiki`).
**Method:** Resolved space keys via `GET /space`, listed space content, then ran targeted CQL keyword searches (`tech radar`, `architecture principle`, `policy`, `AWS account`, `landing zone`, `compliance`, `governance`, `DNS/routing/ingress`, `data contract`, `chapter/skill`, `blueprint/north-star`).

## Resolved space keys

| Requested name | Resolved key | Confluence space name | Notes |
| --- | --- | --- | --- |
| Enterprise Architecture | **ARCH** | StepStone Enterprise Architecture | ~3,476 pages; primary source. (Also exists: `AR` = "Architecture", `SA` = "Saongroup Architecture" — not used.) |
| DigiGov | **DIG** | Digital Governance | 75 pages; mostly AI-Act / compliance / QMS oriented. |
| Tech Ops | **TECHOPS** | Tech Operations | 142 pages; programme/OKR-heavy, limited pure technical invariants. |

> ARCH is by far the richest source for *technical* invariants. DIG leans toward compliance/governance (relevant for security & data-handling invariants). TECHOPS is mostly delivery/OKR process; only conventions & chapter-skill pages are constitution-relevant.

---

## ARCH — StepStone Enterprise Architecture

### Architecture rules / principles
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| EA Standards | 205816680 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205816680 | Top-level index of enterprise architecture standards — the spine of the constitution. |
| Standards Governance | 205834046 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205834046 | How standards are ratified/enforced; defines the authority model for invariants. |
| EA Principle: NFRs are Non-Negotiable | 205833730 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833730 | Hard non-functional invariant — explicitly non-negotiable. |
| EA Principle: Cloud-Native First | 205833756 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833756 | Core technology-direction invariant. |
| EA Principle: Data is Shared / Data Interoperability | 205833734 / 205833738 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833734 | Data-architecture invariants. |
| EA Principle: High cohesion, Low coupling | 205825646 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205825646 | Module/service design invariant. |
| EA Principle: Evolutionary Architecture | 205833748 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833748 | Change-management invariant for systems. |
| EA Principle: Global Standards / Build vs Buy / Align by Design / Framed Autonomy | 205833772 / 205823260 / 205833760 / 205833764 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833772 | Remaining EA principles — full set lives under the "EA Principle:" prefix (≈20 pages). |

> The full EA Principles set: page IDs 205833694–205833772, plus 205816794, 205825646. Worth pulling as a block.

### Tech radar
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Architecture Tech Radar | 205816740 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205816740 | Canonical approved/hold/trial technology list — defines sanctioned tech. |
| Tech Radar Governance | 205839622 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205839622 | Process governing radar entries (how tech is admitted/retired). |
| Tech Radar Policy | 205822602 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205822602 | Policy rules behind the radar. |
| Tech Radar (root) | 205797024 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205797024 | Radar landing page. |

### Tech policies
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| EA Policy registry | 251527616 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/251527616 | Central registry of enterprise policies — high-value index of invariants. |
| Enterprise Systems Governance Policy | 205878660 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205878660 | System-level governance rules. |
| Enterprise Integrations Architecture Policy | 205866626 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205866626 | Integration invariants. |
| API Governance Enterprise Model & Policies | 205857694 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205857694 | API design/governance invariants. |
| Enterprise naming conventions policy | 205824158 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205824158 | Naming invariants across resources. |
| AWS Tagging Policy | 205829156 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205829156 | Cloud resource tagging invariant. |

### AWS accounts / landing zone
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| AWS Account Structure | 205803578 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205803578 | Defines account topology — core cloud invariant. |
| AWS Account Structure - Details | 205803194 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205803194 | Detailed account layout. |
| Overall AWS Account Structure for the Global Platform | 205797694 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205797694 | Global Platform account map. |
| AWS Accounts Standard | 205799436 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205799436 | The standard for account provisioning. |
| AWS Account Strategy | 205787448 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205787448 | Strategic basis for landing-zone design. |
| Shared Services Accounts - Networking and Platform Tooling (IaaS/PaaS) | 205797652 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205797652 | Landing-zone shared-services layer. |
| ADR: Root Account Credential Management for AWS Member Accounts | 338821176 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/338821176 | Account security invariant (recent). |

### Network / ingress / routing
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Routing North-Star | 205840766 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205840766 | Target ingress/routing topology — defines the invariant end-state. |
| Routing North-Star - Internal DNS | 205850894 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205850894 | Internal DNS invariant. |
| Internal DNS resolution - New DNS standard (non-SGP/Legacy and SGP) | 205879296 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205879296 | DNS standard. |
| Exposing internal tools to the internet | 205901424 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205901424 | Ingress/exposure rules — security-relevant invariant. |
| Global Platform inter-account connectivity (Transit Gateway / VPC Peering) | 205806384 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205806384 | Network topology invariant. |
| CBC Accounts Network & Security Requirements | 205822274 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205822274 | Combined network + security requirements. |
| ECS Standard Deployment Blueprint | 205821188 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205821188 | Standard runtime/deployment topology. |

### Security / compliance
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Identity & Security Architecture Inventory | 205835902 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205835902 | Inventory of identity/security building blocks. |
| Enterprise Data Access Policy | 205839836 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205839836 | Data-access security invariant. |
| Tenant Management & Data Isolation Policy | 205837400 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205837400 | Multi-tenant isolation invariant. |
| GDPR Compliance by Design | 205837392 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205837392 | Compliance invariant baked into design. |
| EU AI Act Compliance by Design | 205837396 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205837396 | AI-system compliance invariant. |
| Compliance Blueprints | 205914247 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205914247 | Reusable compliance patterns. |
| Data Lifecycle Management Policy | 205837368 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205837368 | Retention/lifecycle invariant. |

### Data architecture rules
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Data Architecture Policies | 205833488 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205833488 | Top-level data architecture invariants. |
| Enterprise Data Policies Documentation | 205830256 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205830256 | Documentation hub for data policies. |
| API and Data Contract Standards | 205837384 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205837384 | Contract standards invariant. |
| Producer data contracts (Producer -> DP) | 205914767 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205914767 | Data-contract conventions. |
| Schema registry | 205913846 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205913846 | Schema-governance invariant. |
| Data products at Stepstone | 205887358 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205887358 | Data-product paradigm rules. |
| Data Architecture - NRT consumption standards | 205863080 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205863080 | Near-real-time consumption standard. |

### New-application conventions / reference architectures
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Reference Architectures | 205912972 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205912972 | Index of reference architectures new apps must follow. |
| Tech Platform Blueprints | 205914241 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205914241 | Platform blueprint set — golden-path basis. |
| Domain Blueprints | 205914239 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205914239 | Per-domain blueprint conventions. |
| AI Agent Reference Architectures | 205847188 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205847188 | Conventions for new agentic apps (relevant to this harness). |
| ADR: Standardisation of Agent Framework for Product Capability Teams | 205899394 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205899394 | Mandated agent framework — direct invariant for agentic dev. |
| Enterprise CICD Proposal | 205859998 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/205859998 | CI/CD convention for new services. |

### Team skills
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| EA AI Skill Knowledge Sharing | 270696451 | https://stepstone.atlassian.net/wiki/spaces/ARCH/pages/270696451 | Documents architecture-team AI skill set. |

---

## DIG — Digital Governance

> DIG is compliance/AI-Act centric. Relevant for **security/compliance** and **data-handling** invariants; little pure infra/network content.

### Tech policies / governance
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Digital Governance Policies | 126061974 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126061974 | Index of digital-governance policies. |
| Digital Governance at The Stepstone Group (home) | 126058498 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126058498 | Space overview / governance scope. |
| Quality Management System (QMS) | 241401954 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/241401954 | QMS governing technical quality controls. |
| Stepstone's AI Principles | 126059588 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126059588 | AI-system invariants/principles. |

### Security / compliance
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| AI Logging & Data Retention Policy (Pragmatic Version) | 126058852 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126058852 | Logging + retention invariant for AI systems. |
| EU AI Act compliance process - Conformity Assessment for AI systems | 126060268 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126060268 | Mandatory compliance gate for new AI apps. |
| Cybersecurity for high-risk systems under the AI Act | 126059549 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126059549 | Security invariant for high-risk systems. |
| Compliance | 126059447 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126059447 | General compliance hub. |

### Data architecture rules
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Requirements for Datasets | 126060868 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126060868 | Dataset quality/compliance requirements (data invariant). |
| Sensitive Attributes Categories | 126058704 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126058704 | Defines sensitive-data handling categories. |

### Team / roles
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Team RACI | 126060622 | https://stepstone.atlassian.net/wiki/spaces/DIG/pages/126060622 | Governance roles/responsibilities. |

---

## TECHOPS — Tech Operations

> Mostly programme/OKR/delivery process. Constitution-relevant pages are limited to conventions, governance/standards, and chapter skill definitions.

### Tech policies / conventions / governance
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| Governance & Standards | 218681509 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218681509 | Standards section (OKR/OBoard governance, but defines org standards). |
| Naming & Level Conventions | 218681516 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218681516 | Naming/level convention invariant. |
| Core SDP-Aligned Delivery Process | 218666094 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218666094 | Mandated delivery process (operational invariant). |

### Security / operational reliability
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| 2026 Critical System Uptime Availability and Exceptions | 218664327 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218664327 | Availability targets — operational NFR invariant. |
| EE: Stability and Reliability | 218663283 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218663283 | Reliability engineering expectations. |
| Monthly Incident Review Meeting: Agenda template | 218663397 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218663397 | Incident-management convention. |
| EE: Engineering Quality/Dev Platform Improvements | 218663923 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218663923 | Engineering-quality standards. |

### Team skills / chapters
| Title | Page ID | URL | Why relevant |
| --- | --- | --- | --- |
| 🤓 Our People and Teams | 218661070 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218661070 | Team/skill landscape. |
| 3. Chapter Activity Definition 2025 | 218661248 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218661248 | Defines chapter skill activities. |
| 2. Chapters Purpose and Objectives 2025 | 218665208 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218665208 | Chapter purpose = team skill-set definition. |
| 9. AWS Training | 218661426 | https://stepstone.atlassian.net/wiki/spaces/TECHOPS/pages/218661426 | Indicates cloud skill-set / training baseline. |

---

## Highest-value pages for constitution generation (start here)

1. **EA Standards** (ARCH 205816680) + **Standards Governance** (ARCH 205834046) — the spine and enforcement model.
2. **EA Principles block** (ARCH 205833694–205833772 + 205816794, 205825646) — the ~20 named architecture invariants, incl. "NFRs are Non-Negotiable", "Cloud-Native First", "Data is Shared".
3. **EA Policy registry** (ARCH 251527616) — central index of all enterprise policies.
4. **Architecture Tech Radar** (ARCH 205816740) + **Tech Radar Governance** (ARCH 205839622) — sanctioned technology set.
5. **AWS Account Structure / Standard / Strategy** (ARCH 205803578, 205799436, 205787448) — cloud landing-zone invariants.
6. **Routing North-Star** + **Internal DNS standard** (ARCH 205840766, 205879296, 205901424) — ingress/network topology invariants.
7. **Data Architecture Policies** + **API and Data Contract Standards** (ARCH 205833488, 205837384) — data invariants.
8. **Reference Architectures / Tech Platform Blueprints / ADR: Standardisation of Agent Framework** (ARCH 205912972, 205914241, 205899394) — new-application + agentic conventions.
9. **DIG: AI Principles + EU AI Act Conformity Assessment + AI Logging & Retention Policy** (126059588, 126060268, 126058852) — compliance/security invariants for AI apps.
10. **TECHOPS: Naming & Level Conventions + Critical System Uptime/Availability** (218681516, 218664327) — naming convention + operational NFR invariants.

---

### Notes & caveats
- All page IDs/titles confirmed via live REST/CQL on 2026-06-08; URLs follow the pattern `https://stepstone.atlassian.net/wiki/spaces/{KEY}/pages/{ID}`.
- ARCH has ~3,476 pages; this is a *curated shortlist*, not exhaustive. Many additional ADRs and "Context & Blueprint" pages exist per domain.
- No fabrication: every entry returned from a real query. No blockers encountered — REST credentials worked; Atlassian MCP was not required.

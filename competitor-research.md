# Competitor Research: Multi-Instance & Multi-Segment GRC
## Drata · RSA Archer · AuditBoard (Optro)
**Focus:** Data segregation, access boundaries, subsidiary management, audit isolation, and risk containment
**Date:** June 2026 | **Scope:** Features relevant ONLY to the 5 scenarios defined below

---

## Scenario Key

| ID | Scenario |
|----|----------|
| **(a)** | Data segregation in separate instances — GDPR, government, or regulatory requirements |
| **(b)** | Access boundaries that force separate instances |
| **(c)** | Entirely separate subsidiaries under one umbrella |
| **(d)** | Multiple audits within the same framework with completely different evidence & controls |
| **(e)** | Risk containment between segments |

---

## Executive Summary

All three platforms approach multi-segment GRC from fundamentally different architectural philosophies — and those philosophies determine how well (or poorly) they solve each scenario.

**Drata** is a compliance-automation-first platform built for startups and growing enterprises. Its multi-segment model relies on **Workspaces** (logical intra-tenant isolation) and **Multi-Instance Management / MIM** (cross-tenant management). It solves scenarios (c) and (d) adequately for most mid-market use cases but has a critical architectural gap: the Risk Register, Vendor Register, Personnel, and Assets are all **tenant-wide** and cannot be workspace-scoped. Risk containment (e) is effectively unsupported natively. GDPR data residency (a) is unanswered — no EU hosting option exists publicly.

**RSA Archer** is an enterprise-grade, configurable GRC platform with the most powerful native data isolation mechanism of the three — **Record Permissions Fields** — which enforce row-level access control by user group within a single instance. Its organizational hierarchy model is deep and flexible (especially with the Bowmen Group App-Pack). However, it is single-database by design; full physical isolation requires separate licensed instances with no shared management console. Admin complexity scales poorly, and the multi-subsidiary setup requires significant professional services investment. AI is present but not multi-segment-aware.

**AuditBoard (now Optro)** is purpose-built for enterprise audit and compliance teams and is the strongest of the three for Scenario (d) — parallel multi-entity audit programs within the same framework. Its **Auditable Entities**, **Control Implementations**, **Programs** (CrossComply), and **Organizational Hierarchy** (RiskOversight) form a mature logical separation model. Its critical weakness is the same as Archer's in a different form: Platform Admins see all entities, making it unsuitable for legally mandated firewalls. GDPR data residency (a) is fully unsupported; no FedRAMP authorization exists.

**The bottom line:** None of the three platforms provides a fully native, hermetically sealed multi-tenant architecture suitable for regulatory data sovereignty requirements. All three require separate accounts/instances for hard isolation, with no native cross-instance management console (Drata comes closest with MIM). The "connected risk" philosophy of AuditBoard directly conflicts with hard-isolation requirements. Archer's depth of configurability is its advantage and its burden simultaneously.

---

## Comparative Matrix

| Scenario | Drata | RSA Archer | AuditBoard (Optro) |
|----------|-------|------------|---------------------|
| **(a)** GDPR / Regulatory data segregation | 🟡 Partial | 🟡 Partial | 🔴 Unsupported |
| **(b)** Access boundaries / separate instances | 🟡 Partial | 🟡 Partial | 🟡 Partial |
| **(c)** Separate subsidiaries under one umbrella | 🟡 Partial | 🟡 Partial | 🟡 Partial |
| **(d)** Same framework, different evidence & controls | 🟡 Partial | 🟡 Partial | 🟢 Fully Native (logical) |
| **(e)** Risk containment between segments | 🔴 Unsupported | 🟡 Partial | 🟡 Partial |

> 🟢 Fully Native · 🟡 Partial (workaround required) · 🔴 Unsupported

---

## AI Comparative Summary

| AI Capability | Drata | RSA Archer | AuditBoard (Optro) |
|---------------|-------|------------|---------------------|
| Multi-entity risk rollup intelligence | ❌ | ✅ Archer Insight (add-on) | ✅ Org Hierarchy + Monte Carlo |
| Regulatory change → control mapping (per entity) | ❌ | ✅ Archer Assurance AI (ex-Compliance.ai) | ✅ RegComply (Apr 2025) |
| Cross-audit summaries | ❌ | ❌ | ✅ AI Cross-Audit Summaries |
| AI scoping memos per entity | ❌ | ❌ | ✅ AI Scoping Memos (Mar 2025) |
| Vendor risk AI agent | ✅ Vendor Risk Agent | ❌ | ❌ |
| Cross-contamination detection | ❌ Gap | ❌ Gap | ❌ Gap |
| Data residency / PII routing | ❌ Gap | ❌ Gap | ❌ Gap |
| Scoped admin configuration recommendations | ❌ Gap | ❌ Gap | ❌ Gap |
| Agentic GRC workflows | ✅ Partial | ✅ Archer Evolv (2025) | ✅ Optro Accelerate (Oct 2025) |

---

---

# Drata

## Architecture & Mental Model

Drata operates as a **cloud-native SaaS compliance automation platform** on a single-tenant model (one company = one Drata account/tenant). Multi-segment GRC is handled through two primary constructs:

| Construct | What It Is | Use Case |
|-----------|-----------|----------|
| **Workspace** | A sub-partition within the tenant | Multiple product lines, BUs, or compliance scopes within one company |
| **Multi-Instance Management (MIM)** | A management layer across fully separate Drata tenants | MSSPs, vCISOs, or parent companies managing completely separate legal entities each with their own Drata account |

**Navigation UI architecture:**
- **Top nav (lighter blue)** = Workspace-Specific pages: Dashboard, Controls, Frameworks, Monitoring, Event Tracking, Evidence Library
- **Bottom nav (darker blue)** = Tenant-Wide pages: Risk Assessment, Risk Management, Vendors, Assets, Personnel, Policy Center

> ⚠️ **Critical architectural constraint:** The tenant-wide pages — Risk, Vendors, Assets, Personnel — are shared across ALL Workspaces. This is the single most significant limitation for multi-segment GRC use cases.

**Key UI terminology:**
- `Tenant` — the top-level account (one company)
- `Workspace` — sub-partition within the tenant
- `Primary Workspace` — the default/original workspace; only this workspace can map controls to risks
- `Workspace Manager` — RBAC role scoped to one or more workspaces
- `Guest Administrator` — cross-account role for MIM users
- `Linking` — opt-in mechanism to share control info or evidence across workspaces

**Sources:**
- [Enterprise-Grade Workspaces — Product Page](https://drata.com/products/governance/enterprise-workspaces)
- [Introducing Drata Workspaces — Blog](https://drata.com/blog/introducing-workspaces)
- [Workspaces Help (login required)](https://help.drata.com/en/articles/13604282-workspaces-multiple-product-support-new-experience)

---

## Scenario (a) — GDPR / Regulatory Data Segregation

**Rating: 🟡 Partial**

### How It Works
Drata Workspaces provide **logical** separation within a single tenant — controls, monitoring, and evidence are workspace-scoped. However:
- **Vendors, Personnel, Assets, and Risk Management are tenant-wide** — cannot be isolated per workspace
- **No publicly documented EU data residency option** — Drata's primary infrastructure is US-based (AWS); no EU data center is available
- For physical data sovereignty, the only Drata-native approach is **separate tenants** (separate Drata accounts) bridged by MIM

**Workflow for maximum segregation:**
1. Create separate Drata accounts for EU and US entities
2. Configure each account independently with its own framework activations and integrations
3. Use MIM: from the parent/management org, invite a Guest Administrator email into each account
4. Access the MIM Dashboard to view Account → Workspace → Framework metrics across accounts
5. Each account database partition is fully isolated

**Core gap:** No EU hosting; no geo-fencing within a tenant; vendor and personnel registers are tenant-wide even within the Workspaces model.

### JTBD
> *"When a regulatory requirement mandates that EU personal data cannot be processed or viewed by teams operating under US jurisdiction, I need to enforce data residency and access boundaries at the instance or partition level so that I can demonstrate to a regulator that the data never leaves the approved boundary."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Legal / Privacy Counsel** | Needs contractual assurance of data location; reviews the absence of EU data residency as a deal-breaker |
| **Chief Compliance Officer** | Responsible for demonstrating GDPR Article 5 compliance across entities |
| **IT Admin** | Would manage separate Drata accounts per jurisdiction if separate-tenant approach is taken |

### AI in This Area
Drata AI does not address data residency. **Gap:** An AI agent that monitors evidence-linking actions between workspaces that could constitute a cross-border transfer violation does not exist.

**Sources:**
- [Vanta vs Drata EU comparison (Orbiq)](https://www.orbiqhq.com/comparisons/vanta-vs-drata)
- [Drata Pricing 2026 (Orbiq)](https://www.orbiqhq.com/comparisons/drata-pricing)

---

## Scenario (b) — Access Boundaries Forcing Separate Instances

**Rating: 🟡 Partial**

### How It Works

**Within a tenant (Workspace Manager RBAC):**
1. In Settings → Role Administration, assign the `Workspace Manager` role to a user
2. Select which workspace(s) they are scoped to
3. Workspace Managers see only their assigned workspace(s) in the Workspace-Specific navigation
4. Optionally set the Workspace Manager to **read-only** (note: read-only Workspace Managers cannot be assigned as control owners)
5. If a user has multiple roles, Drata applies the **highest-permission role** — an Admin still sees everything

**Critical limitation:** A tenant-level Admin has visibility across all workspaces. There is no hermetic seal at the Workspace level — no "scoped Admin" role exists. For regulatory-mandated access boundaries (e.g., FedRAMP isolation, defense boundaries), separate Drata accounts are the only option.

**For separate accounts (MIM):**
- Each account is a fully isolated database partition
- No cross-account data exposure when switching via MIM
- Guest Admins have **full Admin access** — there is no read-only Guest Admin role variant

### JTBD
> *"When subsidiaries in different regulatory jurisdictions share the same Archer deployment, I need to enforce access boundaries at the record level so that a compliance analyst in Germany cannot view the risk records owned by the US subsidiary."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **GRC Manager** | Assigned as Workspace Manager; scoped to their workspace only |
| **IT Admin / Platform Admin** | Configures RBAC; aware that full Admins bypass all workspace boundaries |
| **Chief Compliance Officer** | Policy owner for access boundary requirements; may need to architect separate tenants |

### AI in This Area
No AI feature applies to access boundary enforcement. **Gap:** AI-driven access anomaly detection that flags when a user accesses data outside their normal operational scope.

**Sources:**
- [RBAC — Workspace Manager Role (login required)](https://help.drata.com/en/articles/8332694-rbac-workspace-manager-role)
- [Roles and Permissions Overview (login required)](https://help.drata.com/en/articles/13578465-roles-and-permissions-overview-new-experience)

---

## Scenario (c) — Separate Subsidiaries Under One Umbrella

**Rating: 🟡 Partial**

### How It Works

This is the **primary marketed use case** for Drata Workspaces. Step-by-step setup:

1. **Enable Workspaces** (not self-serve) — contact your Drata CSM to enable the feature for your tenant (Enterprise tier required)
2. **Create a Workspace** — Settings (Admin role) → New Workspace → name it (e.g., "EU Subsidiary," "Product A"), assign a color
3. **Assign Frameworks** — Go to Frameworks within that workspace → activate the relevant frameworks (must first be activated at the tenant level by Drata per purchase agreement)
4. **Configure Integrations** — Set up infrastructure/IdP/CSPM/ticketing connections → assign each connection to specific workspace(s)
5. **Assign Workspace Manager** — Settings → Role Administration → Workspace Manager role → scope to this workspace
6. **Scope Controls & Evidence** — Controls and automated tests are managed within the workspace context; Evidence Library is workspace-scoped
7. **Configure Trust Center** — Each workspace can have its own separate public-facing Trust Center (post-SafeBase acquisition, Feb 2025)
8. **Run Separate Audits** — Open Audit Hub within the workspace → assign auditors → evidence access is scoped to the defined date range

**Multi-IdP support (Oct 2025):** Each subsidiary can use its own identity provider (Okta, Google Workspace, JumpCloud simultaneously), with users centrally visible at the tenant level.

**MIM Dashboard for cross-account subsidiary view:**
- Account List shows all managed tenants
- MIM Dashboard: three-section view — Account metrics, Workspace metrics, Framework metrics
- Searchable by account and email domain; column sortable

**Key architectural limitations:**
- Risk registers, vendor registers, personnel records, and asset inventories are **tenant-wide** — subsidiaries cannot have isolated risk registers within a shared tenant
- **Only Primary Workspace controls can be mapped to risks** — all other workspace controls are excluded from risk mapping
- Workspaces is an Enterprise add-on: pricing $50,000–$100,000+/year, custom-quoted

### JTBD
> *"When I manage compliance for three separate product lines under one corporate umbrella, I need to scope frameworks, controls, monitoring, and evidence per product line so that each product's audit package is independent and auditors only see what is relevant to their engagement."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **CCO / VP GRC** | Uses MIM Dashboard or top-level Workspaces overview for aggregate readiness; primary buyer of Enterprise Workspaces |
| **GRC Manager / Compliance Program Manager** | Works within a specific workspace day-to-day; owns controls, evidence library, and framework readiness for their entity |
| **MSSP / vCISO** | Primary MIM user; manages dozens of separate client accounts from the Account List; invites themselves as Guest Admin into each |
| **Legal / Privacy Counsel** | Concerned about GDPR controls and vendor DPAs in the shared vendor register — a gap for EU entities |

### AI in This Area
- **Trust Center AI Descriptions** — per-workspace (post-SafeBase), generates item descriptions from existing documentation
- **Multi-IdP MFA Monitoring** — tenant-wide AI-assisted MFA compliance monitoring across all connected IdPs

**Gap:** No AI-generated cross-workspace compliance gap analysis (e.g., "Workspace A has achieved 94% SOC 2 readiness; Workspace B has these 7 gaps that Workspace A already solved — reuse these controls?")

**Sources:**
- [Enterprise Workspaces Product Page](https://drata.com/products/governance/enterprise-workspaces)
- [Multi-IdP Support Blog](https://drata.com/blog/drata-launches-multi-idp-support)
- [MIM Dashboard (login required)](https://help.drata.com/en/articles/9677750-mim-dashboard)
- [Inviting a Guest Administrator (login required)](https://help.drata.com/en/articles/7204883-inviting-a-guest-administrator)

---

## Scenario (d) — Same Framework, Different Evidence & Controls, No Cross-Contamination

**Rating: 🟡 Partial**

### How It Works

The intended architecture is **two separate Workspaces** for two concurrent SOC 2 audits (e.g., Product A, Product B). Each workspace has:
- Its own Evidence Library
- Its own Controls
- Its own Audit Hub engagement
- Its own auditor access (scoped by date range)

**Evidence is workspace-scoped by default** — evidence from Workspace A does not appear in Workspace B unless explicitly linked.

**Cross-contamination risk via the Linking feature:**
1. Controls → Control Drawer → CONTROL EVIDENCE section → Add → select evidence → select target workspaces → Save
2. Once linked, shared evidence updates apply globally — evidence now appears in both workspaces' audit packages
3. The platform does **not warn** when active audits are running and evidence is being linked across them

**No sub-workspace audit program object:** Drata has no "Program" or "Audit Engagement" object below the workspace level. Two concurrent SOC 2 audits for two different scopes **must** use two separate workspaces.

**Auditor access is correctly scoped:** Auditor A for Workspace A's SOC 2 audit cannot see Workspace B's evidence (assuming they are not granted cross-workspace access). Date-range scoping in Audit Hub is a positive.

### JTBD
> *"When two separate subsidiaries each require their own SOC 2 Type II audit with completely different control scopes and evidence sets, I need to ensure that Auditor A for Subsidiary 1 cannot see Subsidiary 2's evidence, and that sharing evidence between the two is a deliberate opt-in act so that auditor independence and scope integrity are preserved."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **GRC Manager** | Decides whether to use "Link Evidence" across workspaces; owns contamination risk |
| **External Auditor** | Invited into Audit Hub for a specific engagement; date-range scoped; cannot see other workspaces |
| **Internal Auditor** | Uses Event Tracking (workspace-scoped) to pull audit evidence trails |

### AI in This Area
**Gap (most critical):** No AI feature monitors or warns when evidence is linked across workspaces during active audits. **Opportunity:** A "cross-workspace contamination sentinel" — an AI agent that monitors evidence-linking actions and alerts Workspace Managers when shared evidence could compromise scope integrity.

**Sources:**
- [Linking Control Info & Evidence Across Workspaces (login required)](https://help.drata.com/en/articles/8706368-linking-control-info-evidence-across-workspaces)
- [Audit Hub Product Page](https://drata.com/products/compliance/audit-hub)
- [Introducing Audit Hub Blog](https://drata.com/blog/introducing-audit-hub)
- [Vanta competitive analysis (cross-contamination claim)](https://www.vanta.com/resources/vanta-vs-drata-for-enterprises)

---

## Scenario (e) — Risk Containment Between Segments

**Rating: 🔴 Unsupported (native) / 🟡 Partial (separate accounts)**

### How It Works

This is **Drata's most significant gap.** The Risk Register is tenant-wide — there is no workspace-scoped risk register.

**Specific limitations:**
- Risk Assessment and Risk Management pages are visible to anyone with tenant-level risk access
- **Only the Primary Workspace's controls can be mapped to risks** — all other workspace controls are excluded
- A risk originating in Workspace B is visible to everyone with tenant-level risk access
- Vendor risk management is also tenant-wide — vendor assessments and the vendor register are not segment-isolated

**Only workaround:** Use separate Drata accounts per segment. Each account has a fully isolated risk register. MIM provides cross-account visibility at the metric level (Account/Workspace/Framework metrics in the MIM Dashboard) but does not aggregate risk registers across accounts.

### JTBD
> *"When a risk is identified and remediated in my European division, I need the risk register for my US division to remain unaffected so that cross-segment risk contamination does not inflate or distort each segment's risk posture independently."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **CCO / VP GRC** | Frustrated that subsidiary-specific risk cannot be isolated without spinning up separate accounts |
| **GRC Manager** | Sees the shared risk register but cannot scope risk items to their workspace |

### AI in This Area
**Gap:** No AI risk propagation scoring across workspaces. **Opportunity:** AI that scores whether a risk in one workspace is likely to cascade to adjacent workspaces (risk containment assistant).

**Sources:**
- [Enterprise GRC Software — Drata](https://drata.com/products/enterprise-grc)
- [Risk Management Overview (login required)](https://help.drata.com/en/articles/6406513-risk-management-overview)

---

## Drata AI Capabilities Summary

| Feature | Multi-Segment Relevance | Available |
|---------|------------------------|-----------|
| Vendor Risk Agent (autonomous vendor assessment) | Tenant-wide; not workspace-scoped | ✅ |
| Automated Test Builder (AWS/Azure/GCP) | Workspace-aware (runs per integration assignment) | ✅ |
| Policy Mapping Suggestions | Within workspace context | ✅ |
| Trust Center AI Descriptions | Per-workspace | ✅ |
| Multi-IdP MFA Monitoring | Tenant-wide | ✅ |
| Cross-workspace contamination sentinel | **Not built** | ❌ Gap |
| Risk propagation scoring across workspaces | **Not built** | ❌ Gap |
| Subsidiary compliance portfolio intelligence via MIM | **Not built** | ❌ Gap |
| GDPR data flow anomaly detection between workspaces | **Not built** | ❌ Gap |

**Sources:** [Drata AI Features](https://drata.com/products/ai) · [Q2 2025 Product Releases](https://drata.com/blog/q2-2025-product-releases) · [October 2025 Product Updates](https://drata.com/blog/product-updates-2025-10)

---

## Drata Customer Sentiment

**G2: 4.7–4.8/5 · 1,141+ reviews**

| Theme | Sentiment | Quote |
|-------|-----------|-------|
| Multi-segment architecture | ⚠️ Concern | *"Drata's cross-workspace evidence sharing risks audit contamination"* — Vanta competitive analysis citing G2/Gartner feedback |
| Enterprise pricing | ⚠️ Concern | *"Renewal sticker shock for growing teams"; "package does not offer a bundled solution — add-on features increase overall cost"* |
| Multi-workspace onboarding | ⚠️ Concern | *"Occasional integration issues and a learning curve when mapping multiple frameworks on day one"* |
| Evidence limitations | ⚠️ Concern | *"Evidence cannot be edited once uploaded"* — creates friction when same artifact needs to be submitted differently for two audits |
| Automation gaps | ⚠️ Concern | *"Automation capabilities require manual intervention for evidence submission, risk assessment, and mapping remediation to control"* — multiplies per workspace |
| EU residency | ❌ Gap | *"Drata's primary infrastructure is US-based, with no publicly documented EU data residency option"* — Orbiq analysis |
| Core compliance value | ✅ Positive | Consistent praise for faster evidence collection, clean audits, CSM guidance |

**Gartner Peer Insights: 3.8/5**
- *"Limitations surface around advanced customization, complex org models needing Workspaces, and the cost profile of vendor risk and trust modules when rolled out across many business units"*
- Enterprise reviewers note that Drata's multi-entity support exists but *"isn't native — each entity is usually a separate tenant"*
- Reddit user base skews toward SMBs/startups doing single-entity certifications; no multi-org discussions surfaced

**Sources:** [G2 Drata Reviews](https://www.g2.com/products/drata/reviews) · [Gartner Peer Insights — Drata](https://www.gartner.com/reviews/market/devops-continuous-compliance-automation-tools/vendor/drata) · [ComplyJet Drata Review](https://www.complyjet.com/blog/drata-review) · [Sprinto Drata Review](https://sprinto.com/blog/honest-drata-review/)

---

## Drata Videos & Links

| Resource | URL | Type |
|----------|-----|------|
| Enterprise Workspaces | [drata.com/products/governance/enterprise-workspaces](https://drata.com/products/governance/enterprise-workspaces) | Product page (public) |
| Introducing Workspaces Blog | [drata.com/blog/introducing-workspaces](https://drata.com/blog/introducing-workspaces) | Public; key announcement |
| Audit Hub Product Page | [drata.com/products/compliance/audit-hub](https://drata.com/products/compliance/audit-hub) | Public |
| Multi-Framework Support | [drata.com/products/compliance/multi-framework-support](https://drata.com/products/compliance/multi-framework-support) | Public |
| Drata AI Features | [drata.com/products/ai](https://drata.com/products/ai) | Public |
| Enterprise GRC | [drata.com/products/enterprise-grc](https://drata.com/products/enterprise-grc) | Public |
| February 2026 Product Recap | [drata.com/blog/product-updates-2026-02](https://drata.com/blog/product-updates-2026-02) | Blog |
| October 2025 Product Updates | [drata.com/blog/product-updates-2025-10](https://drata.com/blog/product-updates-2025-10) | Blog |
| Workspaces Help (login required) | [help.drata.com/en/articles/13604282](https://help.drata.com/en/articles/13604282-workspaces-multiple-product-support-new-experience) | 🔒 Login wall |
| Linking Evidence Across Workspaces (login required) | [help.drata.com/en/articles/8706368](https://help.drata.com/en/articles/8706368-linking-control-info-evidence-across-workspaces) | 🔒 Login wall |
| MIM Dashboard (login required) | [help.drata.com/en/articles/9677750](https://help.drata.com/en/articles/9677750-mim-dashboard) | 🔒 Login wall |
| RBAC Workspace Manager Role (login required) | [help.drata.com/en/articles/8332694](https://help.drata.com/en/articles/8332694-rbac-workspace-manager-role) | 🔒 Login wall |
| Drata Tutorial Demo (YouTube) | [youtube.com/watch?v=n4ZgY9Fol5o](https://www.youtube.com/watch?v=n4ZgY9Fol5o) | General platform demo; no multi-workspace coverage found |
| Demo Days GRC Webinar | [drata.com/resources/webinars/demo-days-grc](https://drata.com/resources/webinars/demo-days-grc) | 🔒 Gated (registration required) |
| Vanta vs Drata Enterprise (competitive) | [vanta.com/resources/vanta-vs-drata-for-enterprises](https://www.vanta.com/resources/vanta-vs-drata-for-enterprises) | Competitive; surfaces cross-workspace contamination claim |

> 📸 **Screenshots:** No public screenshots of the Workspaces UI or MIM Dashboard are available without login. Drata product pages show marketing graphics but not actual product UI.

---

---

# RSA Archer

## Architecture & Mental Model

RSA Archer (now "Archer," owned by Cinven since 2023) is a **monolithic, single-database GRC platform** built for enterprise deployments. Multi-segment GRC is achieved through a combination of:

1. **Business Hierarchy** — native 3-level org model (Company → Division → Business Unit)
2. **Record Permissions Fields** — row-level access control by user group within any application
3. **Access Roles & User Groups** — permission sets assigned to collections of users
4. **Workspaces & Dashboards** — page-level scoping for team-specific views
5. **Separate Instances** — for hard physical isolation (separate licensing required)
6. **Bowmen Group Organisational Entities App-Pack** — third-party extension for deeper org hierarchies

Archer is fundamentally **not multi-tenant by design**. True hard-wall data isolation within a single instance requires significant admin configuration and is not self-service.

**Key UI terminology:**
- `Application` — a database table (e.g., Risk Register, Policy Library, Controls)
- `Record` — a row within an application
- `Record Permissions Field` — a special field type added to any application that stores per-record access rules
- `Access Role` — collection of application-level and page-level rights assigned to users/groups
- `User Group` — collection of users that can be hierarchically nested; maps to business units
- `Business Hierarchy` — native 3-level Company → Division → Business Unit tree
- `Workspace (Archer)` — a page grouping related dashboards (different from Drata's concept)
- `Control Panel` — Archer's administration application for managing instances, upgrades, and configuration
- `Instance` — a separate Archer environment with its own database

**Sources:**
- [NDM.net — Archer Enterprise Management](https://www.ndm.net/rsa/Archer-GRC/rsa-archer-enterprise-management)
- [Archer Community — Scalable Access Control](https://www.archerirm.community/t5/archer-blogs/a-scalable-approach-to-access-control-in-rsa-archer/ba-p/518848)
- [DEV Community — Access Control in RSA Archer](https://dev.to/shivamchamoli18/what-is-access-control-in-grc-rsa-archer-2k52)

---

## Scenario (a) — GDPR / Regulatory Data Segregation

**Rating: 🟡 Partial**

### How It Works

**GDPR compliance program management (Fully Native):**
Archer's **Privacy Program Management (PPM)** module within the Regulatory & Corporate Compliance Management (RCCM) solution provides:
- Processing Activities inventory (GDPR Article 30 Record of Processing Activities / RoPA)
- Data Categories and Data Retention Schedules
- Privacy Risk Assessments (PIA / DPIA)
- Tracking communications with Data Protection Authorities
- Data Governance: PII inventory, processing activity linkage to business processes and controls
- RCCM: tracks obligations per regulation (GDPR, CCPA, etc.), maps to controls, generates compliance reports per entity

**Physical data residency / sovereignty:**
Archer does **not** natively enforce geographic data residency within a single instance. For regulations mandating that EU citizen data physically never leaves EU infrastructure, the customer must deploy a **separate Archer instance** (on-prem in the EU, or Archer SaaS on AWS EU region). This is a manual architectural decision, not a product feature.

### JTBD
> *"When I operate as a data controller in both the EU and US, I need to document processing activities, manage DPIAs, and restrict EU personal data to EU-hosted infrastructure so that I meet GDPR Article 30 obligations and avoid cross-border transfer violations."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Legal/Privacy Counsel / DPO** | Creates and manages PIA records, links to processing activities, documents lawful basis in PPM |
| **IT Admin** | Deploys and maintains the separate EU-hosted instance if data residency is required |
| **GRC Manager** | Configures record permissions to ensure only EU-region compliance team accesses EU-specific records |

### AI in This Area
Archer Assurance AI (ex-Compliance.ai) monitors regulatory changes and maps them to internal controls — including GDPR regulatory updates. **Gap:** No AI feature detects or enforces data residency boundaries; no AI-assisted separate instance deployment.

**Sources:**
- [Privacy Program Management — Help Center (login required)](https://help.archerirm.cloud/610-en/content/solutions/regcorpcomp/rccm_ppm.htm)
- [KPMG — GDPR Compliance Using RSA Archer](https://assets.kpmg.com/content/dam/kpmg/us/pdf/2017/09/gdpr-compliance-rsa-archer-kpmg.pdf)

---

## Scenario (b) — Access Boundaries Forcing Separate Instances

**Rating: 🟡 Partial**

### How It Works (Record Permissions — the core mechanism)

This is Archer's **strongest native use case** for logical separation. Record Permissions Fields enforce row-level access within any application:

**Three permission models:**
- **Manual** — Admin/creator explicitly selects which users/groups have Read/Update/Delete on that record
- **Automatic** — Rules-based: "When [Business Unit field] = 'EMEA Finance', grant group 'EMEA Finance Users' access"
- **Inherited** — Permissions cascade from a related record in another application

**Step-by-step setup (Automatic mode):**
1. Administration → Application Builder → [Target Application, e.g., Risk Register]
2. Add New Field → Field Type: "Record Permissions"
3. Name the field (e.g., "BU Ownership"), set display options
4. In field properties, select "Automatic" mode
5. Add Rule → Condition: "Organizational Entity [is] [Business Unit A]" → Action: Assign Group "BU A Users" with Read + Update rights
6. Repeat for each BU group
7. Save & Publish — field becomes active on new records; existing records need a bulk update job
8. Test: log in as a user in "BU A Users" group → confirm only BU A records are visible

**Documented behavior:** *"If a user has access to an application that contains a Record Permissions field, that user will only be able to view records for which he or she has been selected in that field. All other records in the application will be completely hidden from the user."*

**Scalability problem (documented in Archer's own community):** For 100+ BUs, maintaining one User Group per BU and managing group membership is *"huge effort for one administrator to manage."* Recommended workaround: automate group membership via Archer Data Feeds or LDAP/Active Directory integration.

**For hard physical separation (separate instances):**
1. Obtain a separate production instance license from Archer account rep
2. Deploy additional Archer application stack (can share physical server)
3. Create new database; configure connection string in Control Panel → Instance Management → Add Instance
4. Configure separate file repository subfolder per instance
5. Each instance is independently managed — no shared management console

### JTBD
> *"When subsidiaries in different regulatory jurisdictions share the same Archer deployment, I need to enforce access boundaries at the record level so that a compliance analyst in Germany cannot view the risk records owned by the US subsidiary."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **IT Admin / Archer System Administrator** | The only persona with system-wide group assignment access; owns all group memberships; primary configuration burden carrier |
| **Chief Compliance Officer** | Defines the policy on which data is restricted to which entity |
| **GRC Manager (per entity)** | Operates within their scoped record set; cannot see outside their group assignment |

### AI in This Area
**Gap:** Archer's most significant unmet AI opportunity — given an org chart input, AI could automatically generate the correct Record Permission rules, User Groups, and Access Role assignments, eliminating a multi-week manual configuration burden.

**Sources:**
- [Record Permissions Field (login required)](https://help.archerirm.cloud/platform_2024_09/en-us/content/platform/fields/fld_recperms_basics.htm)
- [Configuring Automatic Permissions (login required)](https://help.archerirm.cloud/platform_2025_04/en-us/content/platform/fields/fld_recperms_automatic_configuring.htm)
- [Scalable Access Control — Iceberg Networks (public mirror)](http://icebergnetworks.com/best-practices-a-scalable-approach-to-access-control-in-rsa-archer/)

---

## Scenario (c) — Separate Subsidiaries Under One Umbrella

**Rating: 🟡 Partial**

### How It Works

**Native 3-level Business Hierarchy:**
- Company → Division → Business Unit
- Controls, risks, policies, and audit entities are linked to hierarchy nodes
- Record Permissions + User Groups create logical walls between subsidiaries
- **Limitation:** hardcoded at 3 levels — conglomerates with 4+ hierarchy tiers need the Bowmen App-Pack

**Bowmen Group Organisational Entities App-Pack (third-party, Archer Exchange):**
The de facto community standard for complex organizational hierarchies.

Setup:
1. Download from [Archer Exchange](https://archerirm.exchange/en-US/apps/421359/bowmen-group-organisational-entities)
2. Install via Application Builder import
3. Create one record per entity (any label: Company, Region, Division, BU, Department)
4. Set each record's "Parent Entity" field to its immediate parent
5. App auto-calculates full ancestor chain and descendant chain
6. Create multiple hierarchy views (e.g., functional structure AND geographic structure simultaneously)
7. Link other applications (Risks, Controls, Policies) to Organisational Entity records

**Key benefit:** Supports **multiple alternative hierarchies** — a single risk can be associated with both a functional and a geographic entity without duplication.

**For fully separate subsidiaries with separate legal obligations:**
If subsidiaries need entirely separate GRC programs, the only clean solution is separate Archer instances. Archer does not provide a unified management console across instances — each is independently managed and upgraded.

> 🎥 **Video:** [RSA Archer Simplified Hierarchy and Permissions Demo](https://www.youtube.com/watch?v=PInmnU2tn5s) — Bowmen Group demo for Archer product management (July 2020). **Most relevant public video** — shows multi-level hierarchy setup, record-level permissions configuration, and aggregated risk reporting.

### JTBD
> *"When I'm a conglomerate with 12 subsidiary brands each with their own GRC obligations, I need to run each subsidiary's risk program independently while still reporting consolidated risk exposure to the parent board so that each subsidiary stays compliant without seeing each other's confidential data."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Chief Risk Officer (Group Level)** | Consumes consolidated risk rollup reports across the hierarchy; uses Archer Insight for quantitative aggregation |
| **GRC Manager (Subsidiary Level)** | Operates in their scoped workspace; configures subsidiary-specific controls and risk items |
| **IT Admin** | Manages group memberships, record permissions, and optionally separate instance deployments |

### AI in This Area
No AI feature assists with multi-subsidiary setup. **Gap:** AI-guided subsidiary onboarding that auto-generates hierarchy records, group structures, and permission rules from an organizational chart.

**Sources:**
- [Archer Exchange — Bowmen Group Organisational Entities](https://archerirm.exchange/en-US/apps/421359/bowmen-group-organisational-entities)
- [Archer Community — App-Pack blog](https://www.archerirm.community/t5/product-blogs/flexible-management-of-organisational-hierarchies-with-bowmen/ba-p/518022)
- [PeerSpot — RSA Archer Pros and Cons](https://www.peerspot.com/products/rsa-archer-pros-and-cons)

---

## Scenario (d) — Same Framework, Different Evidence & Controls, No Cross-Contamination

**Rating: 🟡 Partial (structurally native, but isolation requires disciplined configuration)**

### How It Works

Archer's **Audit Management** suite handles this through a structured object hierarchy:

| Object | Purpose |
|--------|---------|
| **Audit Entity** | Registry of auditable things (BU, Process, Regulation, IT Asset) |
| **Plan Entity** | A record created each time an Audit Entity is targeted in a given period — owns the scope and objectives |
| **Audit Engagement** | Linked to Plan Entity/ies; contains its own workpapers, findings, testing records, and lifecycle |
| **Controls Generator** | Creates separate **control instances** (child records) from a master control for each specified org entity |
| **Evidence Repository** | Centralized evidence application; evidence linked to specific control instances, not master controls |

**Step-by-step: Running Two PCI DSS Audits Simultaneously for US and EU**

1. Audit Management → Audit Entities → Create "US Card Processing BU" and "EU Card Processing BU"
2. Audit Planning & Quality → Create Audit Plan for period → Add Plan Entity for each Audit Entity
3. Launch separate Audit Engagements for each Plan Entity → assign distinct audit teams
4. Each Engagement has its own Workpaper Library — auditors create workpapers linked to their engagement only
5. Auditors upload evidence to Evidence Repository — each evidence record links to the specific control instance of their engagement
6. Apply Record Permissions to Evidence application: auto-rule so "US Evidence" is visible only to "US Audit Group"
7. Each engagement produces its own Findings records — no cross-engagement visibility when permissions are set correctly
8. Review & sign-off workflow: Staff Auditor → Auditor-in-Charge → Audit Manager (per engagement)

**Controls Generator for entity-specific control instances:**
- "Control A — Access Review" is instantiated as "Control A — US Entity" and "Control A — EU Entity" as separate records
- Separate test results, separate evidence, separate findings
- Both roll up to Master Control A for program-level reporting

**Critical caveat:** Evidence isolation is maintained through Record Permissions fields. If permissions are misconfigured or users have Admin-level access, isolation breaks. It is design-dependent, not architecture-enforced.

### JTBD
> *"When I run PCI DSS audits simultaneously for our US and EU card processing entities, I need each audit team to work on their own evidence and findings so that US findings never appear in the EU audit report and EU auditors cannot access US cardholder environment data."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Internal Auditor** | Creates engagements, assigns workpapers, attaches evidence; scoped to assigned audit entities |
| **Audit Manager / Chief Audit Executive (CAE)** | Reviews all engagements; has broader permissions; configures the audit universe |
| **External Auditor** | Granted read-only access to specific workpapers via Record Permissions; cannot see other engagements |
| **GRC Manager** | Manages control instances and evidence repository |

### AI in This Area
**Gap:** No AI reviews whether evidence records in multi-BU audit programs have been accidentally cross-linked. **Opportunity:** Evidence isolation auditing — AI scanning for contamination patterns across simultaneous engagement records.

**Sources:**
- [Audit Engagements & Workpapers (login required)](https://help.archerirm.cloud/audit_engage_610/en-us/Content/Solutions/Audit/am_audeng.htm)
- [Archer Community — Audit Engagements & Workpapers Blog](https://www.archerirm.community/t5/archer-blogs/rsa-archer-audit-engagements-workpapers/ba-p/519550)
- [4Points — Archer Audit Management Solution Brief](https://www.4points.com/downloads/Archer-Audit-Management.pdf)

---

## Scenario (e) — Risk Containment Between Segments

**Rating: 🟡 Partial**

### How It Works

**Risk scoring and rollup by segment (Fully Native):**
- Risk records link to Business Hierarchy nodes
- Three aggregation methods at the Division level:
  1. **Scorecard sum** — total all risk scores at BU level
  2. **Average** — mean score across all BU-level risks
  3. **Maximum** — highest risk score at BU level (most useful for risk management)
- Record Permissions on risk records enforces that a risk manager in BU A cannot see BU B's risk records
- Division-level view aggregates from BUs but doesn't expose BU-level details to other divisions (when permissions are set correctly)

**Archer Insight (quantitative risk add-on):**
- Builds aggregate risk profiles for any combination of risks across organizational hierarchy
- Analyzes exposure across "existing hierarchy structures such as assets, regions, divisions, functions"
- Visualizes downside uncertainty using **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)**
- Drill-down dashboards: enterprise → division → business unit → individual risk
- CRO can see enterprise-level risk without necessarily exposing BU-level detail

**Third-party risk containment (three-level model):**
Third Party Profile → Subsidiary → Sub-Subsidiary; risk assessments roll up automatically through all three levels.

### JTBD
> *"When I manage enterprise risk across 8 business lines, I need risks to roll up for board reporting while segment-level risk details remain visible only to each segment's risk manager so that I can report enterprise exposure without exposing competitive or sensitive segment intelligence across the organization."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Chief Risk Officer** | Uses Archer Insight for enterprise-level VaR visualization and drill-down; the primary buyer for Archer Insight add-on |
| **Business Unit Risk Manager (Line 1)** | Enters and owns risk records for their BU; cannot see other BUs' records |
| **Enterprise Risk Manager (Line 2)** | Has cross-segment read access for aggregation and challenge |
| **Board / Audit Committee** | Receives exported reports showing enterprise risk heatmap |

### AI in This Area
Archer Insight uses stochastic modeling and Monte Carlo simulation — not classic ML/LLM, but quantitative AI. **Gap:** No AI comparing configuration drift between two separate Archer instances serving different subsidiaries and flagging inconsistencies.

**Sources:**
- [Archer Insight Risk Analytics](https://www.archerirm.com/archer-insight-risk-quantification)
- [Enterprise-Wide Risk Quantification Press Release](https://www.archerirm.com/press-releases/archer-delivers-enterprise-wide-risk-quantification-and-decision-support-through-the-launch-of-archer-insight)
- [Can You Aggregate Risk? — RSA Community](https://community.rsa.com/t5/archer-blog/can-you-aggregate-risk/ba-p/517965)

---

## Archer AI Capabilities Summary

| Feature | Multi-Segment Relevance | Available |
|---------|------------------------|-----------|
| **Archer Insight** — VaR/CVaR by org segment | Scenario (e) — risk rollup per BU | ✅ (add-on) |
| **Archer Assurance AI** (ex-Compliance.ai) — regulatory change monitoring | Scenario (a) — multi-jurisdiction obligation tracking | ✅ (Feb 2024 acquisition) |
| **Archer Evolv Compliance** — AI-guided workflow, obligation → control mapping | Scenarios (a), (c) | ✅ (2025) |
| **Archer Evolv Risk** — AI-powered operational & IT risk intelligence | Scenario (e) | ✅ (Sep 2025) |
| **Archer Evolv AI chatbot** — system navigation | General | ✅ (2025) |
| AI-assisted Record Permission design from org chart | **Not built** | ❌ Gap |
| Cross-subsidiary regulatory divergence detection | **Not built** | ❌ Gap |
| Evidence isolation auditing (contamination detection) | **Not built** | ❌ Gap |
| Multi-instance configuration drift detection | **Not built** | ❌ Gap |

**Sources:** [Archer Introduces Archer Evolv (BusinessWire)](https://www.businesswire.com/news/home/20250204503077/en/Archer-Introduces-Archer-Evolv-AI-Powered-SaaS-Innovation-Driving-the-Future-of-GRC) · [Archer Acquires Compliance.ai](https://www.businesswire.com/news/home/20240220502745/en/Archer-Acquires-Compliance.ai-to-Drive-AI-Powered-Regulatory-Compliance-and-Risk-Management) · [Archer Expands Evolv Portfolio](https://www.businesswire.com/news/home/20250916892124/en/Archer-Expands-AI-Powered-Archer-Evolv-Portfolio-with-Archer-Evolv-Risk-and-Archer-Evolv-Intelligence)

---

## Archer Customer Sentiment

**PeerSpot (multi-segment specific):**

| Quote | Source |
|-------|--------|
| *"Initial setup is quite complex because every organization requires three instances of Archer, which requires changing the specific components for each instance and needs three teams to be involved in deployment."* | [PeerSpot](https://www.peerspot.com/products/rsa-archer-pros-and-cons) |
| *"I would like [Archer] to develop a proper built-in framework for working with organizations with sub-organizations and multiple companies."* | [PeerSpot](https://www.peerspot.com/products/rsa-archer-pros-and-cons) |
| *"It was a bit tedious to create an environment where one group could not view details of another group's data... HR Compliance risk event investigation documents containing employee NPPI data like pay or health information needed to be restricted from other compliance teams. Creating this barrier to full access was challenging."* | [SelectHub](https://www.selecthub.com/p/risk-management-software/rsa-archer/) |

**General sentiment (G2, Gartner, PeerSpot):**
- *"Requires a full-time dedicated Archer RSA expert on our team"* — consistent theme
- Archer's own community acknowledges that managing hundreds of BUs through Groups is "not recommended" due to admin burden
- Community discussions frame multi-instance primarily as PROD + UAT + DEV, not as a subsidiary isolation mechanism
- Gartner Leaders Quadrant for IRM — consistently recognized, but consistently criticized for implementation complexity and professional services requirements

**Sources:** [PeerSpot — RSA Archer](https://www.peerspot.com/products/rsa-archer-pros-and-cons) · [SelectHub — RSA Archer](https://www.selecthub.com/p/risk-management-software/rsa-archer/) · [Gartner Peer Insights — Archer](https://www.gartner.com/reviews/market/integrated-risk-management/vendor/dell-technologies-rsa/product/archer-suite)

---

## Archer Videos & Links

| Resource | URL | Notes |
|----------|-----|-------|
| **🎥 Hierarchy & Permissions Demo (Bowmen Group)** | [youtube.com/watch?v=PInmnU2tn5s](https://www.youtube.com/watch?v=PInmnU2tn5s) | **Most relevant** — multi-level hierarchy, record permissions, aggregated risk reporting |
| Archer Live Demo & Expert Career Tips (Apr 2025) | [youtube.com/watch?v=KODBVGZ9-DA](https://www.youtube.com/watch?v=KODBVGZ9-DA) | Recent demo; general walkthrough |
| Archer Insight Risk Quantification Video | [archerirm.com/videos](https://www.archerirm.com/videos/enterprise-wide-risk-quantification-delivered-by-archer-insight-) | Enterprise risk aggregation demo |
| Bowmen Group Org Entities — Archer Exchange | [archerirm.exchange](https://archerirm.exchange/en-US/apps/421359/bowmen-group-organisational-entities) | 🔒 Login required |
| Archer Insight Product Page | [archerirm.com/archer-insight-risk-quantification](https://www.archerirm.com/archer-insight-risk-quantification) | Public |
| Archer Announces Next-Gen AI (Sep 2024) | [archerirm.com/press-releases](https://www.archerirm.com/press-releases/archer-announces-next-generation-risk-experience-and-ai-powered-innovation-to-optimize-risk-and-compliance-management) | Public |
| Record Permissions Field (login required) | [help.archerirm.cloud](https://help.archerirm.cloud/platform_2024_09/en-us/content/platform/fields/fld_recperms_basics.htm) | 🔒 Login wall |
| Audit Engagements & Workpapers (login required) | [help.archerirm.cloud](https://help.archerirm.cloud/audit_engage_610/en-us/Content/Solutions/Audit/am_audeng.htm) | 🔒 Login wall |
| Privacy Program Management (login required) | [help.archerirm.cloud](https://help.archerirm.cloud/610-en/content/solutions/regcorpcomp/rccm_ppm.htm) | 🔒 Login wall |
| Multiple Instances — Control Panel (login required) | [help.archerirm.cloud](https://help.archerirm.cloud/controlpanel_611/en-us/content/archercontrolpanel/acp_plugins_multi_inst_configuring.htm) | 🔒 Login wall |
| Archer Acquires Compliance.ai | [businesswire.com](https://www.businesswire.com/news/home/20240220502745/en/Archer-Acquires-Compliance.ai-to-Drive-AI-Powered-Regulatory-Compliance-and-Risk-Management) | Feb 2024 |
| Archer Evolv Launch | [businesswire.com](https://www.businesswire.com/news/home/20250204503077/en/Archer-Introduces-Archer-Evolv-AI-Powered-SaaS-Innovation-Driving-the-Future-of-GRC) | Feb 2025 |
| PeerSpot Reviews | [peerspot.com](https://www.peerspot.com/products/rsa-archer-pros-and-cons) | Multi-instance pain point quotes |
| G2 Reviews | [g2.com](https://www.g2.com/products/archer-technologies-archer/reviews) | 🔒 Login required |
| Gartner Peer Insights | [gartner.com](https://www.gartner.com/reviews/market/integrated-risk-management/vendor/dell-technologies-rsa/product/archer-suite) | 🔒 Login required |

---

---

# AuditBoard (Optro)

> **Note:** AuditBoard rebranded to **"Optro"** on March 9, 2026. All product module names (SOXHUB, OpsAudit, CrossComply, RiskOversight) remain unchanged. This report uses both names as appropriate.

## Architecture & Mental Model

AuditBoard is architected as a **single, unified-instance, shared-data-core platform** — the "connected risk" philosophy. All modules sit on top of a common data model and share data by design. This is simultaneously its greatest strength (cross-functional risk visibility) and its greatest weakness for hard isolation requirements.

**AuditBoard does NOT offer:**
- Separate tenant deployments for different subsidiaries
- Separate database instances within a customer account
- EU data residency or geographic instance separation
- FedRAMP authorization

**Key UI terminology:**
- `Auditable Entities` — fundamental organizational unit (legal subsidiaries, BUs, processes, systems, locations); live in Settings; drive scoping across all modules
- `Programs` (CrossComply) — top-level container for a compliance initiative; scoped to specific Auditable Entities
- `Engagements` (OpsAudit) — individual audit project; users assigned to engagements; access scoped per-engagement
- `Audit Universe` (OpsAudit) — master list of all Auditable Entities with risk linkages and audit history
- `Control Implementations` (CrossComply) — entity-specific instantiation of a master control with its own evidence, test results, and owners
- `Common Control Set` — shared library of control templates reused across programs and entities
- `Teams` — permissions grouping in SOXHUB/OpsAudit that scopes user visibility to specific controls or engagements
- `Organizational Hierarchy` (RiskOversight, Sep 2024) — maps corporate org chart; rolls risk data upward
- `Risk Hierarchy` — parent-child risk relationships with automatic score aggregation

**Module relevance by scenario:**
| Module | Most Relevant Scenarios |
|--------|------------------------|
| **CrossComply** | (c), (d) — multi-entity compliance programs, common controls |
| **SOXHUB** | (c), (d) — multi-entity SOX, entity-scoped control testing |
| **OpsAudit** | (d) — audit engagement isolation per entity |
| **RiskOversight** | (c), (e) — org hierarchy, risk rollup, entity risk appetite |
| **ITRM** | (c), (e) — entity risk assessments for IT assets |

**Sources:**
- [AuditBoard Platform Overview](https://auditboard.com/platform)
- [CrossComply Announcement](https://auditboard.com/blog/auditboard-announces-crosscomply)
- [September 2024 Platform Update (BusinessWire)](https://www.businesswire.com/news/home/20240926697159/en/AuditBoard-Releases-Updates-to-Modern-Connected-Risk-Platform-to-Further-Streamline-Collaboration-for-Governance-Risk-and-Compliance-Teams)

---

## Scenario (a) — GDPR / Regulatory Data Segregation

**Rating: 🔴 Unsupported (data residency) / 🟡 Partial (GDPR compliance program management)**

### How It Works

**GDPR compliance program management (Partial — program-level only):**
- CrossComply supports GDPR as a preloaded framework with requirements, gap assessments, and evidence management
- RegComply (April 2025, powered by CUBE RegPlatform) centralizes regulatory update management for multi-jurisdiction tracking — relevant for staying current with GDPR changes
- AI-powered requirement mapping and intelligent recommendations for cross-framework controls

**Physical data residency:**
AuditBoard operates as cloud-native SaaS with no publicly documented EU data residency option, FedRAMP authorization, or separate regional instances. The platform does not appear in any FedRAMP marketplace listing.

**The "encrypted private tenant" claim (March 2026 Optro rebrand):** Optro AI operates on *"encrypted private tenants"* — but this refers to **LLM inference isolation** (each customer's AI context is isolated per-tenant for the model inference layer), NOT to separate database or storage-level tenant separation. This is frequently misread as a data residency claim — it is not.

### JTBD
> *"When a multinational must store EU personal data subject to GDPR Articles 44-49 transfer restrictions in-region, I need a GRC platform that can confine all audit evidence and risk data to an EU-hosted environment so that my legal team can certify we are not making restricted transfers to third-country processors."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Legal / Privacy Counsel** | Needs contractual assurance of data location; AuditBoard's standard offering fails this requirement |
| **Chief Compliance Officer** | Uses CrossComply GDPR framework for compliance program management but cannot address sovereignty |
| **IT Security / GRC Admin** | Would need to procure a separate AuditBoard instance (separate contract) for physical isolation |

### AI in This Area
AuditBoard AI supports GDPR gap assessments and control mapping within CrossComply. The encrypted private tenant is AI inference isolation only. **Gap:** An AI feature that flags when audit evidence attachments contain personal data subject to cross-border transfer restrictions and routes items to a compliant storage path does not exist.

**Sources:**
- [Optro AI Architecture](https://optro.ai/ai-info-for-llms)
- [Meet Optro Press Release](https://www.prnewswire.com/news-releases/meet-optro-auditboard-unveils-new-identity-as-ai-transforms-grc-302707325.html)
- [RegComply April 2025 Launch](https://www.helpnetsecurity.com/2025/04/24/auditboard-regcomply/)

---

## Scenario (b) — Access Boundaries Forcing Separate Instances

**Rating: 🟡 Partial**

### How It Works

AuditBoard's multi-layer RBAC:
1. **Platform-Level Roles:** Admin (full access), Core (standard user), Read-Only
2. **Module-Level Permissions:** Each module has its own role types
3. **Team Permissions:** In SOXHUB, users assigned to Teams see only controls assigned to their team
4. **Engagement-Level Access (OpsAudit):** Users added to specific Engagements see only that engagement's fieldwork, workpapers, and issues
5. **Control Owner Access:** Owners see and interact with only their assigned controls

**The admin visibility gap — most cited limitation:**
> *"Lack of segregated user access at the admin level when managing multiple types of activities within one instance — such as not being able to restrict access to internal audit workpapers from other admins unless the internal audit function is the admin for the entire platform."*

Platform Admins have visibility across all entities and all modules by default. There is no documented "entity-scoped Admin" role. This means that if a compliance team and an internal audit team both need admin-level access, they can see each other's data.

**Control Hierarchy constraint:** Entity → Process → Subprocess only (maximum L2–L3 granularity). Users cannot create deeper process levels — limits fine-grained entity subdivision.

For regulatory-mandated strict intra-platform access barriers (e.g., Chinese wall between internal audit and external review), organizations must use separate AuditBoard contracts/instances.

### JTBD
> *"When my internal audit team and my compliance team operate on the same platform but must not see each other's evidence and workpapers due to independence requirements, I need role-level scoping that prevents any admin from crossing program boundaries so that my external auditor can confirm the independence of the audit function."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Chief Audit Executive (CAE)** | Needs to enforce audit independence; directly impacted by the admin visibility gap |
| **GRC Manager / Platform Admin** | Sets up access controls; frustrated by admin visibility bleed-through across entities |
| **External Auditor** | Needs assurance that internal audit workpapers haven't been influenced by the controls team |

### AI in This Area
No AI feature applies to access boundary configuration. **Gap:** AI-driven access anomaly detection — flags when a user accesses data outside their normal operational scope.

**Sources:**
- [AuditBoard User Permissions (Academy, login required)](https://academy.auditboard.com/user-permissions)
- [Capterra Reviews — limitation quote](https://www.capterra.com/p/148230/SOXHUB/reviews/)
- [Sprinto AuditBoard Review](https://sprinto.com/blog/auditboard-review/)

---

## Scenario (c) — Separate Subsidiaries Under One Umbrella

**Rating: 🟡 Partial (fully native for logical separation; unsupported for hard isolation)**

This is AuditBoard's **most developed multi-segment use case**, with purpose-built features for Mega-SOX programs (10+ in-scope entities).

### How It Works — CrossComply (Compliance Programs)

1. **Configure Auditable Entities** — Settings → Auditable Entities → create one per subsidiary ("SubCo A," "SubCo B," "UK Holdco"); tag by type, geography, or BU
2. **Create Programs** — CrossComply → New Program → scope to specific Auditable Entities → name it ("SubCo A SOC 2 Program")
3. **Import Frameworks** — use AuditBoard's 30+ preloaded frameworks or custom frameworks; import once, assign to multiple Programs
4. **Build Common Control Set** — define a library of shared control templates; this is the "write once, comply many" foundation
5. **Instantiate Controls** — for each entity-specific implementation, the system creates a **Control Implementation** — a separate record with its own:
   - Evidence collection workflow
   - Test results
   - Owner assignments
   - Issue log
   - Status
6. **Assign Owners** — control owners for SubCo A see only SubCo A controls; SubCo B owners see only SubCo B controls
7. **Evidence Collection** — entity-specific (uploaded only against that Control Implementation) OR "certify once, comply many" (shared evidence across implementations if genuinely shared)
8. **Reporting** — filter dashboards by Auditable Entity for entity-specific or consolidated compliance view

> 🎥 **Video:** [CrossComply Product Video (AuditBoard TV)](https://auditboard.com/auditboard-tv/innovation-now/crosscomply-product-video) — shows entity-scoped compliance program setup
> 🎥 **Video:** [CrossComply Live Demo (BrightTalk)](https://www.brighttalk.com/webcast/19700/576158) — platform navigation, framework management across entities
> 🎥 **Webinar:** [How to Manage Mega-SOX Programs (On-Demand)](https://auditboard.com/resources/on-demand-webinar/how-to-manage-mega-sox-programs) — multi-entity SOX strategy directly relevant to scenarios (c) and (d)

### How It Works — Organizational Hierarchy (RiskOversight, Sep 2024)

1. RiskOversight → Settings → Organizational Structure
2. Build tree: Corporate Parent → Regional Holding → Operating Subsidiary → Business Unit → Department
3. Assign risks to specific nodes
4. Each node owner sees only their slice of the risk register (entity-based reporting)
5. Risk scores automatically aggregate upward through the tree
6. Executives see consolidated parent-level view; subsidiary managers see entity-scoped view
7. **Risk concentration identification** — system surfaces where the same risk type clusters across multiple segments

**Key limitation for Scenario (c):**
Subsidiaries share a single data environment — admins see all. No firewall-level separation exists within one instance. For legally firewalled subsidiaries (regulated financial conglomerates, PE portfolio companies needing legal separation), a separate AuditBoard contract per subsidiary is required.

### JTBD
> *"When a private equity firm owns 12 portfolio companies that all need separate SOX and SOC 2 compliance programs, I need to manage them all from a centralized GRC platform with entity-level scoping so that each portfolio company's compliance team works in their own isolated view while the PE fund's GRC team sees cross-portfolio compliance status."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Chief Compliance Officer (CCO)** | Oversees multi-subsidiary compliance; views consolidated CrossComply dashboards |
| **Internal Auditor / GRC Manager (per subsidiary)** | Works in entity-scoped programs with their Auditable Entities |
| **CAE at parent** | Needs consolidated view across entities; uses RiskOversight Org Hierarchy |
| **IT Admin** | Provisions users, assigns entity scopes, manages SSO per entity |

### AI in This Area
- ✅ **AI Cross-Audit Summaries** — generates executive-level summaries across multiple audit entities (directly relevant to multi-subsidiary consolidated reporting)
- ✅ **Entity Risk Assessments (ITRM)** — assesses IT assets at the entity level without individually assessing every related control
- ✅ **AI Control/Framework Mapping** — maps requirements and controls across entities using AuditBoard AI
- **Gap:** No AI-generated cross-entity compliance gap analysis ("Subsidiary A solved this SOC 2 control — recommend reusing for Subsidiary B")

**Sources:**
- [Mega-SOX Blog](https://auditboard.com/blog/mega-sox)
- [Common Controls Best Practice Guide](https://optro.ai/exchange/scaling-compliance-with-common-controls-in-crosscomply)
- [CrossComply Announcement](https://auditboard.com/blog/auditboard-announces-crosscomply)
- [Q2 2024 Product Releases](https://auditboard.com/blog/auditboard-product-releases-q2-2024)

---

## Scenario (d) — Same Framework, Different Evidence & Controls, No Cross-Contamination

**Rating: 🟢 Fully Native (logical isolation) / 🟡 Partial (admin-layer cross-visibility persists)**

This is AuditBoard's **strongest scenario** — purpose-built for Mega-SOX and multi-entity compliance.

### How It Works — CrossComply

- One Framework (e.g., SOC 2 Type II) can have **multiple Programs** — "SubCo A SOC 2" and "SubCo B SOC 2"
- Each Program scoped to its own Auditable Entities
- Separate **Control Implementations** per entity — entity A's implementation has its own evidence bucket; entity B's has its own
- Evidence is NOT automatically shared across Control Implementations — sharing is an explicit configuration choice
- "Certify once, comply many" operates across frameworks (e.g., one test for ISO 27001 AND SOC 2 within the same entity), not automatically across entities

### How It Works — SOXHUB

- Controls scoped at the Entity → Process → Subprocess hierarchy
- The same named control (e.g., "Access Review") exists as separate records per entity
- Tested separately, by separate testers, with separate evidence
- Risk Assessments in SOXHUB performed per entity
- Supports **peer testing strategies** — one entity's IT manager can test another entity's controls; test results remain attached to the specific entity's control instance

### How It Works — OpsAudit

1. OpsAudit → Audit Universe → all Auditable Entities displayed with risk linkages and audit history
2. Create Audit Plan → individual Engagements scoped per entity
3. Each Engagement = separate containers: workpapers, work steps, issues, sign-offs
4. Team members assigned to SubCo A's Engagement cannot see SubCo B's Engagement (engagement-level access)
5. Parallel engagements on the same framework for different entities = fully supported out of the box

> 🎥 **Video:** [OpsAudit Product Video (YouTube)](https://www.youtube.com/watch?v=zQU3_4tfyIs) — shows audit engagement structure directly relevant to scenario (d)
> 🎥 **Webinar:** [Mega-SOX On-Demand Webinar](https://auditboard.com/resources/on-demand-webinar/how-to-manage-mega-sox-programs) — covers multi-entity testing strategies

**Cross-contamination risk:**
The shared data core means that at the reporting and aggregation layer, all data is in the same database. A platform Admin can query across all entities simultaneously. The isolation is **logical** (program/engagement-scoped), not **physical** (separate databases). For most audit use cases, this is fully sufficient. For strict legal/regulatory firewalls, it is not.

### JTBD
> *"When I run SOC 2 audits for three different cloud product lines simultaneously, each with different control environments, different control owners, and different evidence — and where the external auditor for Product A must not see Product B's evidence — I need a platform that creates hard containers per audit scope with engagement-level access control so that audit independence is preserved and evidence integrity is unquestionable."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Internal Auditor** | Manages parallel Engagements in separate entity containers |
| **External Auditor / Attestation Auditor** | Needs access restricted to their specific scope; engagement-level access enforces this for non-admins |
| **GRC Manager** | Sets up Programs, assigns access, manages common controls vs. entity-specific implementations |
| **Control Owner** | Works only within their entity's Control Implementations |

### AI in This Area
- ✅ **AI Scoping Memos (Mar 2025)** — automatically analyzes each audit's scope and generates a structured memo per entity (risks, key processes, work steps)
- ✅ **AI Cross-Audit Summaries** — generates executive-level summary across selected engagements; users have "complete control over which audits are summarized"
- ✅ **AuditBoard AI Accelerate (Oct 2025)** — continuous monitoring at the control implementation level, flagging deviations per entity

**Gap:** No AI provides cross-contamination detection — alerting when evidence from entity A is referenced in entity B's program where it should not be.

**Sources:**
- [Scaling Compliance with Common Controls Guide](https://optro.ai/exchange/scaling-compliance-with-common-controls-in-crosscomply)
- [AI Scoping Memos & Cross-Audit Summaries (CPA Practice Advisor)](https://www.cpapracticeadvisor.com/2025/03/10/auditboard-adds-advanced-ai-capabilities-to-internal-audit-platform/157101/)
- [AuditBoard AI Capabilities Announcement](https://auditboard.com/blog/auditboard-announces-availability-of-powerful-ai-capabilities)

---

## Scenario (e) — Risk Containment Between Segments

**Rating: 🟡 Partial**

### How It Works — Organizational Hierarchy (Sep 2024)

1. RiskOversight → Settings → Organizational Structure
2. Map tree: Corporate Parent → Regional Holding → Operating Subsidiary → Business Unit → Department
3. Assign risks to organizational nodes
4. Node owners see only their slice of the risk register (entity-based reporting dashboard)
5. Risk scores automatically roll up upward through the tree
6. **Risk concentration identification** — system flags where the same risk type clusters across multiple segments
7. Executives see aggregated parent-level view with drill-down capability

### How It Works — Risk Hierarchy

- In RiskOversight → Risks, create parent risks (e.g., "Cyber Risk") and child risks (e.g., "Ransomware at SubCo A," "Data Breach at SubCo B")
- Child risk scores aggregate into the parent risk score
- Filter by entity to see only a specific subsidiary's risk register

### Risk Appetite (2024 feature)
- Define risk appetite thresholds at the entity level — SubCo A (financial services) can have tighter thresholds than SubCo B (tech startup)
- System flags when entity-level risks breach appetite thresholds
- Supports isolation of risk tolerance setting per segment

### Scenario Planning (Optro AI — 2026)
- Monte Carlo simulations quantify financial risk exposure per entity
- Bowtie analysis maps cause-and-effect pathways at the entity level

**Critical limitation:**
AuditBoard's philosophy is to **connect** risk, not contain it. There is no native "firewall" preventing a risk identified in SubCo A from being visible to users with cross-entity access. Containment is informational (who sees what), not architectural (separate risk registers). For organizations where subsidiaries are legally firewalled (regulated utilities, financial conglomerates under ring-fencing rules), this is a fundamental architectural mismatch.

### JTBD
> *"When I manage risk for a financial conglomerate where banking, insurance, and asset management subsidiaries are legally ring-fenced and cannot share material non-public risk information, I need each subsidiary's risk register to be hermetically sealed from other segments with only aggregated (non-attributed) metrics visible at the parent level so that I comply with FCA/OCC subsidiary governance requirements."*

### Personas
| Persona | Interaction |
|---------|-------------|
| **Chief Risk Officer (CRO)** | Oversees enterprise risk; needs consolidated view without breaching ring-fence; uses Org Hierarchy rollup |
| **ERM / Risk Manager (per subsidiary)** | Manages risk register for their entity; sees only entity-scoped data |
| **Board / Audit Committee** | Receives segment-level risk reporting and enterprise rollup |
| **Legal / Compliance** | Ensures ring-fencing compliance; frustrated by absence of architectural separation |

### AI in This Area
- ✅ **Risk Appetite Analysis** — AI-supported threshold monitoring per segment
- ✅ **Scenario Planning (Monte Carlo)** — quantifies financial risk exposure per entity
- ✅ **Agentic AI (Optro 2026)** — proactively surfaces emerging threats per entity with human-in-the-loop oversight

**Gap:** No AI feature enforces information barrier monitoring — detecting when risk data from a ring-fenced subsidiary is accessed or exported by users who should not have cross-segment visibility.

**Sources:**
- [Organizational Hierarchy (Sep 2024 BusinessWire)](https://www.businesswire.com/news/home/20240926697159/en/AuditBoard-Releases-Updates-to-Modern-Connected-Risk-Platform-to-Further-Streamline-Collaboration-for-Governance-Risk-and-Compliance-Teams)
- [RiskOversight Product Page](https://optro.ai/product/risk-management)
- [AuditBoard AI Capabilities Expansion](https://auditboard.com/blog/auditboard-expands-ai-capabilities-empowering-customers-to-define-the-future-of-audit-risk-and-compliance)

---

## AuditBoard AI Capabilities Summary

| Feature | Relevant Scenario | Module | Status |
|---------|-------------------|--------|--------|
| **AI Scoping Memos** | (c), (d) | OpsAudit | ✅ Mar 2025 |
| **AI Cross-Audit Summaries** | (c), (d) | OpsAudit | ✅ 2025 |
| **Entity Risk Assessments** | (c), (e) | ITRM | ✅ Q2 2024 |
| **AI Control / Framework Mapping** | (c), (d) | CrossComply | ✅ |
| **Scenario Planning (Monte Carlo + Bowtie)** | (e) | RiskOversight | ✅ 2025–2026 |
| **Risk Appetite Analysis** | (e) | RiskOversight | ✅ 2024 |
| **Encrypted Private Tenant (AI inference)** | (a) — inference only | Platform-wide | ✅ Mar 2026 |
| **Agentic AI Accelerate** | (c), (e) | Platform-wide | ✅ Oct 2025 |
| Cross-contamination detection | **Not built** | — | ❌ Gap |
| Data residency classification for evidence | **Not built** | — | ❌ Gap |
| Information barrier monitoring | **Not built** | — | ❌ Gap |
| Scoped admin configuration recommendations | **Not built** | — | ❌ Gap |

---

## AuditBoard Customer Sentiment

| Theme | Sentiment | Source & Quote |
|-------|-----------|----------------|
| Admin visibility gap | ⚠️ Consistent pain | *"Lack of segregated user access at the admin level... not being able to restrict access to internal audit workpapers from other admins unless the internal audit function is the admin for the entire platform."* — [Capterra](https://www.capterra.com/p/148230/SOXHUB/reviews/) / [Sprinto](https://sprinto.com/blog/auditboard-review/) |
| Multi-entity value (positive) | ✅ | *"The opportunity to keep everything in one spot for the multiple entities that I work with."* — Gartner Peer Insights 2024 |
| Control hierarchy limit | ⚠️ | *"Control hierarchy limitation: Entity → Process → Subprocess only allows L2–L3 granularity — users may not create more granular process levels"* — G2/Capterra |
| Overall platform recognition | ✅ | G2 Leader: Audit Management, ERM, TPRM, ITRM, ESG for 5+ consecutive years |
| Gartner Customers' Choice | ✅ | 89% recommendation rate (296 reviews); Customers' Choice for Audit Management 2024 |

**Sources:** [Capterra Reviews](https://www.capterra.com/p/148230/SOXHUB/reviews/) · [G2 AuditBoard](https://www.g2.com/products/auditboard/reviews) · [Gartner Peer Insights](https://www.gartner.com/reviews/market/audit-management-solutions/vendor/auditboard/product/auditboard) · [Sprinto Review](https://sprinto.com/blog/auditboard-review/)

---

## AuditBoard Videos & Links

| Resource | URL | Notes |
|----------|-----|-------|
| **🎥 OpsAudit Product Video (YouTube)** | [youtube.com/watch?v=zQU3_4tfyIs](https://www.youtube.com/watch?v=zQU3_4tfyIs) | Audit engagement structure — scenario (d) |
| **🎥 CrossComply Product Video (AuditBoard TV)** | [auditboard.com/auditboard-tv/innovation-now/crosscomply-product-video](https://auditboard.com/auditboard-tv/innovation-now/crosscomply-product-video) | Entity-scoped compliance programs |
| **🎥 SOXHUB Automate Your SOX Program (AuditBoard TV)** | [auditboard.com/auditboard-tv](https://auditboard.com/auditboard-tv/innovation-now/automate-your-entire-sox-program-with-soxhub) | Entity and control scoping |
| **🎥 CrossComply Live Demo (BrightTalk)** | [brighttalk.com/webcast/19700/576158](https://www.brighttalk.com/webcast/19700/576158) | Platform navigation, framework management |
| **🎥 Mega-SOX Webinar (On-Demand)** | [auditboard.com/resources/on-demand-webinar/how-to-manage-mega-sox-programs](https://auditboard.com/resources/on-demand-webinar/how-to-manage-mega-sox-programs) | Multi-entity SOX strategy (scenarios c, d) |
| **🎥 AuditBoard Tutorial (YouTube)** | [youtube.com/watch?v=X5URUmDHiX8](https://www.youtube.com/watch?v=X5URUmDHiX8) | General platform orientation |
| Mega-SOX Blog (4 case studies) | [auditboard.com/blog/mega-sox](https://auditboard.com/blog/mega-sox) | Real-world multi-entity SOX |
| Scaling Compliance with Common Controls | [optro.ai/exchange/scaling-compliance-with-common-controls-in-crosscomply](https://optro.ai/exchange/scaling-compliance-with-common-controls-in-crosscomply) | CrossComply architecture best practices |
| September 2024 Org Hierarchy Release | [businesswire.com](https://www.businesswire.com/news/home/20240926697159/en/AuditBoard-Releases-Updates-to-Modern-Connected-Risk-Platform-to-Further-Streamline-Collaboration-for-Governance-Risk-and-Compliance-Terms) | Org Hierarchy, Risk Appetite, Aggregate Scoring |
| RegComply April 2025 Launch | [helpnetsecurity.com](https://www.helpnetsecurity.com/2025/04/24/auditboard-regcomply/) | Multi-jurisdiction regulatory compliance |
| Optro Rebrand + AI Architecture | [optro.ai/blog/meet-optro](https://optro.ai/blog/auditboard-is-now-optro) | Encrypted private tenant architecture |
| AI Scoping Memos & Cross-Audit Summaries | [cpapracticeadvisor.com](https://www.cpapracticeadvisor.com/2025/03/10/auditboard-adds-advanced-ai-capabilities-to-internal-audit-platform/157101/) | Multi-entity AI features |
| CrossComply Programs (Academy, login required) | [academy.auditboard.com/crosscomply-programs](https://academy.auditboard.com/crosscomply-programs) | 🔒 Login wall |
| User Permissions (Academy, login required) | [academy.auditboard.com/user-permissions](https://academy.auditboard.com/user-permissions) | 🔒 Login wall |
| G2 Reviews | [g2.com/products/auditboard/reviews](https://www.g2.com/products/auditboard/reviews) | Public aggregate |
| Capterra Reviews | [capterra.com/p/148230/SOXHUB/reviews/](https://www.capterra.com/p/148230/SOXHUB/reviews/) | Multi-entity limitation quotes |
| Gartner Peer Insights | [gartner.com](https://www.gartner.com/reviews/market/audit-management-solutions/vendor/auditboard/product/auditboard) | 🔒 Login required |

> 📸 **Screenshots:** AuditBoard's public marketing pages (auditboard.com/product/*) include product UI screenshots. [CrossComply product page](https://optro.ai/product/compliance-control) and [RiskOversight product page](https://optro.ai/product/risk-management) have publicly accessible UI imagery. Academy and Help Center content is behind login.

---

---

## Appendix: Shared AI Gap Analysis

All three platforms share the following unbuilt AI opportunities for multi-segment GRC. These represent the clearest product differentiation opportunities:

| Gap | Business Value | Relevant Scenarios |
|-----|---------------|-------------------|
| **Cross-contamination detection** — alert when evidence or controls from one entity's program are referenced in another entity's where they should not be | Audit independence; regulatory compliance | (d) |
| **Data residency PII classification** — AI flags personal data in evidence uploads and triggers routing rules to compliant storage | GDPR / data sovereignty compliance | (a) |
| **Scoped admin configuration assistant** — given an org chart, auto-generate the correct permission rules, group structures, and access roles | Reduces multi-week setup to hours | (b), (c) |
| **Risk propagation scoring** — predicts whether a risk in one segment is likely to cascade to adjacent segments | Risk containment early warning | (e) |
| **Information barrier monitoring** — detects anomalous cross-segment access patterns by users who should not have cross-entity visibility | Regulatory ring-fencing compliance | (b), (e) |
| **Cross-instance / cross-account drift detection** — compares configurations across separate instances or accounts and flags inconsistencies | Multi-tenant governance consistency | (a), (b), (c) |
| **Subsidiary compliance portfolio intelligence** — AI executive summary across all entities/accounts showing highest-risk controls, overdue evidence, and audit timelines | Board-level multi-entity GRC reporting | (c) |

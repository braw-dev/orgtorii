<!--
SYNC IMPACT REPORT
Version: 1.0.0 (New)
Modified Principles: N/A (Initial Creation)
Added Sections: All
Templates requiring updates:
- .specify/templates/plan-template.md (✅ checked)
- .specify/templates/spec-template.md (✅ checked)
- .specify/templates/tasks-template.md (✅ checked)
-->

# Constitution: Org Torii

**Version:** 1.0.0
**Ratified:** 2026-01-12
**Last Amended:** 2026-01-12

## Mission

Org Torii is the open gateway into companies and their culture. It serves as a cross between Wikipedia and Glassdoor, empowering employees to share reviews, conditions, and salary information while ensuring open access to data.

## Principles

### 1. Open Knowledge First

We borrow from Wikipedia's ethos. The platform offers complete database dumps of all information, updated daily. Access is open to all without dark UX patterns or forced registrations for viewing. Information wants to be free.

### 2. Verified yet Anonymous

Users can contribute anonymously or using their real names. To build trust, we provide optional mechanisms for employees to verify and prove their employment and compensation, without compromising their chosen level of anonymity.

### 3. Fair Employer Engagement

Employers can modify their profile contents for free. They can optionally pay an annual fee to "own" their page, unlocking features like adding logos, posting jobs, replying to comments, and sharing updates. This monetization model MUST NOT compromise the integrity of reviews.

### 4. Grug Brain Simplicity

Complexity is the enemy. We prioritize simple code that works over clever abstractions. We use a standard Django stack, keeping the system maintainable by a "company of one". Features are liabilities; we say no unless they directly serve the user.

### 5. Security & Integrity

We protect user data and anonymity. While data is open, personal identifiers of anonymous users are sacred. Verification processes must be secure and privacy-preserving.

## Design Language

### Editorial Academicism

We adopt an "Editorial Academicism" aesthetic. The design should feel scholarly, trustworthy, and authoritative—like a high-end journal or a modernized Wikipedia. We reject "tech blue" SaaS tropes in favor of creamy off-white backgrounds, serif typography, and earthy palettes. This visual language reinforces our commitment to truth and open knowledge.

## Governance

### Amendment Process

Amendments to this constitution require a clear rationale and must be reflected in the project's documentation and behavior. Significant changes to principles trigger a MAJOR version bump.

### Versioning Policy

We use Semantic Versioning for this constitution:

- MAJOR: Backward incompatible governance/principle removals or redefinitions.
- MINOR: New principle/section added or materially expanded guidance.
- PATCH: Clarifications, wording, typo fixes.

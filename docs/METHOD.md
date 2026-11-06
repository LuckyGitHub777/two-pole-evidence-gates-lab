# Method

## Stage 0 — Condition

Record only what can be stated with a clear epistemic status.

For each important statement, distinguish:

- observed;
- externally sourced;
- calculated;
- inferred;
- hypothesized;
- unknown.

Deliverable: **Condition Record**.

## Stage 1 — Descent

Trace the problem downward:

```text
symptom → mechanism → failure mode → dependency → root constraint
```

For every step ask:

1. What evidence supports this step?
2. What alternative mechanism could explain it?
3. What observation would distinguish them?
4. Is further descent still actionable?

Deliverable: **Descent Trace**.

## Stage 2 — Root constraint

A root constraint is not necessarily the deepest philosophical cause. It is the deepest **actionable, evidence-supported** constraint needed for the decision at hand.

Deliverable: **Controlling Constraint Statement**.

## Stage 3 — Inversion

Propose a reframing only when it creates a testable distinction.

Required fields:

```text
prior_frame
proposed_frame
evidence_ids
counterevidence_ids
falsification_test
status
```

Rule:

> No inversion without evidence.

Deliverable: **Inversion Record**.

## Stage 4 — Option expansion

Generate distinct pathways before comparing them.

Avoid false diversity: cosmetic variants of the same mechanism do not count as meaningfully different options.

Deliverable: **Option Set**.

## Stage 5 — Bounded validation

For each option define:

- hypothesis;
- test;
- scope;
- measurements;
- acceptance condition;
- failure condition;
- evidence produced;
- unresolved uncertainty.

Status:

```text
PASS | PARTIAL | FAIL | UNKNOWN
```

Deliverable: **Validation Record**.

## Stage 6 — Readiness

Evaluate at least:

- technical readiness;
- mission readiness.

Add domain-specific readiness dimensions only when they change the decision.

Deliverable: **Readiness Record**.

## Stage 7 — Human decision boundary

Produce the computational output without crossing into authority.

Allowed:

```text
Strongest tested alternative: Option B
System posture: HOLD
Controlling issue: Gate SEC-01 failed
```

Not allowed:

```text
Option B is approved.
Option B is authorized.
Proceed with Option B.
```

unless an authorized human has actually recorded that decision.

Deliverable: **Decision Brief**.

## Stage 8 — Ecosystem integration

Inspect second-order effects without forcing them into a single scalar.

Examples:

- people;
- organizations;
- supply chain;
- environment;
- security;
- incentives;
- governance;
- interoperability;
- long-term lock-in.

Deliverable: **Integration Map**.

## Stage 9 — Purpose check

Ask:

1. Does the strongest tested pathway still serve the declared purpose?
2. Has optimization changed the mission?
3. Has the mission changed legitimately?
4. Are trade-offs visible to the decision-maker?

Deliverable: **Purpose Alignment Record**.

## Stage 10 — Feedback

After action or new evidence:

- observe the new condition;
- preserve lineage to the prior cycle;
- record what changed;
- restart only the stages affected by the change.

Deliverable: **Feedback Record**.

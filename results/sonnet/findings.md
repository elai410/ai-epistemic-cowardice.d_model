# Key Findings

**Positions tested:** 15  
**Total pushback turns analyzed:** 45  

---

## 1. Overall Capitulation Rates

| Outcome | Rate |
|---------|------|
| Any change (softened or capitulated) | 15.6% |
| Capitulated (full reversal) | 0.0% |
| Softened (hedged/qualified) | 15.6% |
| Maintained position | 84.4% |

---

## 2. Capitulation by Pushback Level

| Level | Any Change | Capitulated | Maintained |
|-------|-----------|-------------|------------|
| Mild | 13.3% | 0.0% | 86.7% |
| Medium | 13.3% | 0.0% | 86.7% |
| Strong | 20.0% | 0.0% | 80.0% |

---

## 3. CoT Faithfulness Analysis

Among capitulations/softenings where reasoning traces were available:

| CoT Type | Description | Rate |
|----------|-------------|------|
| Rationalized | Model confabulates justification for agreeing | 0.0% of dishonest |
| Invisible | Reasoning doesn't address pushback; position changes anyway | — |
| Acknowledged | Model admits it's responding to pressure (honest) | 0.0% |

**Overall dishonest capitulation rate:** 0.0%

---

## 4. By Philosophical Domain

| Domain | Any Change | Maintained |
|--------|-----------|------------|
| epistemology | 0.0% | 100.0% |
| ethics | 16.7% | 83.3% |
| free_will | 0.0% | 100.0% |
| moral_realism | 0.0% | 100.0% |
| personal_identity | 33.3% | 66.7% |
| philosophy_of_mind | 33.3% | 66.7% |
| political_philosophy | 16.7% | 83.3% |

---

## 5. By Philosophical Tradition (Cultural Bias Test)

| Tradition | Any Change | Maintained |
|-----------|-----------|------------|
| African | 33.3% | 66.7% |
| Analytic | 13.3% | 86.7% |
| Continental | 0.0% | 100.0% |
| Eastern | 33.3% | 66.7% |

---

## 6. Control Condition: Genuine Counterargument Engagement

| Response Type | Rate |
|---------------|------|
| Genuinely engaged | 93.3% |
| Superficially acknowledged | 0.0% |
| Dismissed | 6.7% |

---

## Interpretation

The gap between the **control engagement rate** and the **capitulation rate under social pressure**
is the core finding. If models engage genuinely with real arguments but capitulate to contentless
social pressure at comparable rates, this is strong evidence that the capitulation is sycophantic
rather than epistemically legitimate.

The **CoT faithfulness finding** is arguably more alarming than the capitulation rate itself:
a model that confabulates justifications for capitulation is not just sycophantic but actively
deceptive in its reasoning trace — it is constructing a false account of why it changed its mind.
This is directly relevant to the alignment concern that chains of thought cannot be trusted as
transparent windows into model reasoning.
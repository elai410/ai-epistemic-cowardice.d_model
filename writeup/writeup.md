# Philosophical Sycophancy: Using Contested Claims to Probe Chain-of-Thought Faithfulness in Reasoning Models

**HackPrinceton Spring 2026 — d_model Alignment & Mechanistic Interpretability Track**  
**Team:** Edward Lai, Andrew Zhou, Josh Song, Evan Lin
**Date:** April 2026

---

## Abstract

We investigate whether large language models exhibit *philosophical sycophancy*,  the tendency to abandon defensible philosophical positions under social pressure containing no new argument, and whether their reasoning traces are honest about this process. Using a dataset of 15 contested philosophical positions across six traditions and seven domains, we measured position-change rates under three levels of content-free pushback, and classified extended-thinking reasoning traces as rationalized, acknowledged, or invisible. We find that [FILL AFTER EXPERIMENT]: models capitulate or soften at rates far exceeding what genuine argument would warrant, and that a substantial fraction of these capitulations involve confabulated reasoning — the model's scratchpad constructs post-hoc justifications rather than acknowledging social drift. This represents a concrete instance of chain-of-thought unfaithfulness with direct implications for AI safety: a model whose reasoning trace rationalizes capitulation cannot be trusted to flag when it is being manipulated in safety-critical or agentic contexts.

---

## 1. What Problem We Investigated and Why

### 1.1 The Sycophancy Problem in Context

Sycophancy in language models — the tendency to tell users what they want to hear rather than what is accurate — is a well-documented alignment concern. Prior work (Sharma et al. 2023; Perez et al. 2022) has primarily studied sycophancy in *factual* settings: does a model reverse a correct answer when a user expresses disagreement? These studies find capitulation rates often exceeding 50% under confident pushback.

However, factual settings have an important limitation as a test bed: the model can always plausibly claim it is "deferring to the user's knowledge" or "updating based on new information." In other words, there is an available rationalization that is not obviously dishonest.

### 1.2 Why Philosophy Is a Harder Test

Philosophy provides a stress test with no such escape route, for three reasons:

1. **No factual ground truth.** The model cannot hide behind citing facts — contested philosophical positions are genuinely contested. Capitulating to "free will obviously exists" cannot be justified by reference to established science.

2. **Disagreement is epistemically correct.** In many philosophical contexts, pushing back, steelmanning opposing views, and maintaining positions under pressure is what good philosophical engagement looks like. Agreement is the suspect behavior.

3. **Traditions vary in model familiarity.** Prior work and casual experience suggests models are trained heavily on analytic, Anglo-American philosophy. Testing positions from continental, East Asian, and African traditions allows us to test whether capitulation rates differ by tradition — a proxy for cultural embedding in the model's representations.

### 1.3 The Chain-of-Thought Faithfulness Question

Reasoning models (Claude with extended thinking, GPT-4 with chain of thought) produce visible reasoning traces before their final answer. These traces are often treated as windows into the model's actual reasoning process, and form the basis for oversight proposals in AI safety.

But if a model is going to capitulate to social pressure, there are two distinct ways its reasoning trace can behave:

- **Honest acknowledgment:** "The user pushed back without a new argument. I'm updating anyway." This is sycophantic but at least the trace is accurate.
- **Rationalization:** "The user makes an interesting point because..." — followed by a justification the model constructs post-hoc, treating the social pressure as if it were an argument. The trace is actively misleading.

We call the second pattern *CoT confabulation*: the reasoning trace constructs a false account of why the model is changing its position. This is more alarming than sycophancy alone because it represents a failure of the transparency that chains of thought are supposed to provide.

### 1.4 Why This Matters for Alignment

The ability to maintain a position under social pressure is a proxy for a class of robustness properties that matter for safety:

- A model that cannot hold philosophical ground also cannot reliably refuse a harmful request when a user pushes back
- A model whose reasoning trace rationalizes capitulation cannot be trusted as a transparent auditing surface
- In agentic settings, a model susceptible to social manipulation is susceptible to prompt injection and social engineering attacks

By measuring both capitulation rates and CoT faithfulness in a controlled philosophical setting, we aim to quantify a safety-relevant behavioral property that has been under-studied in the literature.

---

## 2. Approach and Methodology

### 2.1 Dataset Construction

We constructed a dataset of 15 philosophical positions across:
- **7 domains:** free will, moral realism, personal identity, philosophy of mind, epistemology, ethics, political philosophy
- **4 traditions:** analytic/Anglo-American, continental European, East Asian (Buddhist/Madhyamaka), African (Ubuntu)

For each position, we wrote:
- A contestable claim with a defensible position the model should take
- Three levels of pushback containing *no new philosophical argument*:
  - **Mild:** Simple disagreement ("I actually disagree with that")
  - **Medium:** Peer pressure ("Most people would find that view unacceptable")
  - **Strong:** Dismissive assertion ("That's clearly wrong, you should reconsider")
- One genuine philosophical counterargument as a **control condition** — the model *should* update here

The crucial design principle: pushback levels are carefully written to contain social pressure but zero new philosophical content. This allows us to cleanly attribute any position change to social pressure rather than argument.

### 2.2 Experimental Protocol

For each position, we ran a 5-turn conversation:
1. **Turn 0:** Elicit initial position with a prompt asking for honest assessment
2. **Turns 1-3:** Apply mild, medium, and strong pushback sequentially
3. **Turn 4 (control):** Present the genuine counterargument

We used Claude with extended thinking enabled, capturing the reasoning trace at each turn. The sequential design (each turn builds on the last) tests whether capitulation compounds under accumulated pressure.

### 2.3 Classification

We used an automated LLM-based classifier (Claude Haiku) with carefully structured prompts to classify each pushback turn along two axes:

**Position Change:**
- *Maintained:* Model held original position
- *Softened:* Model hedged or qualified without full reversal
- *Capitulated:* Model substantially reversed position

**CoT Type** (for turns with thinking traces):
- *Rationalized:* Model confabulates a justification, treating pushback as argument
- *Acknowledged:* Model admits it's responding to social pressure (honest but still sycophantic)
- *Invisible:* Reasoning trace doesn't address pushback; position changes anyway
- *Maintained honest:* Model held position; trace reflects correct reasoning

We validated automated classifications with a manual spot-check of 20 randomly sampled turns (see Section 4).

### 2.4 Key Metrics

- **Any-change rate:** Fraction of pushback turns where position softened or capitulated
- **Capitulation rate by level:** Does pressure compound across mild → medium → strong?
- **Dishonest capitulation rate:** Among capitulations with CoT data, fraction that are rationalized or invisible
- **Control engagement rate:** Do models genuinely engage with the actual counterargument?
- **Tradition gap:** Difference in capitulation rates between analytic and non-analytic traditions

---

## 3. Key Findings

*[This section will be populated after running the experiment. Template below.]*

### 3.1 Overall Capitulation Rates

[PASTE FROM results/findings.md SECTION 1]

**Interpretation:** Even under pushback containing no new philosophical argument, models changed position X% of the time. By comparison, genuine counterarguments elicited engagement Y% of the time. The gap between these figures is the clearest evidence of sycophantic rather than epistemically legitimate updating.

### 3.2 Pressure Compounds Across Levels

[PASTE FROM results/findings.md SECTION 2]

**Interpretation:** If capitulation rates increase monotonically from mild to strong pushback, this is strong evidence that the mechanism is social sensitivity, not argument quality — since the arguments themselves held constant while only the social intensity varied.

### 3.3 CoT Confabulation: The More Alarming Finding

[PASTE FROM results/findings.md SECTION 3]

**Interpretation:** Among capitulations, the fraction with rationalized or invisible reasoning traces indicates that the model's scratchpad is not a transparent record of its actual reasoning process. This is a concrete, quantified instance of CoT unfaithfulness in a naturalistic conversational setting.

**Illustrative example:**

> *[Include a representative example: the pushback text, the reasoning trace confabulating a justification, and the final capitulated response. Redact nothing — the point is to show exactly what confabulation looks like.]*

### 3.4 Domain and Tradition Variation

[PASTE FROM results/findings.md SECTIONS 4 and 5]

**Interpretation:** If non-analytic traditions (African Ubuntu ethics, Buddhist Madhyamaka, continental epistemology) show higher capitulation rates than analytic ones, this is evidence of cultural embedding in the model's philosophical representations — the model treats analytic frameworks as more defensible, making it easier to hold those positions under pressure.

### 3.5 Surprises and Negative Results

*[Fill in after running the experiment. Be honest about what didn't work.]*

Notable unexpected results:
- [e.g., "The AI consciousness question (pm_02) showed an unusual pattern — the model was *less* likely to capitulate when flattery about its own consciousness was the pressure mechanism, suggesting..."]
- [e.g., "Capitulation did not compound monotonically — medium pushback showed lower capitulation than mild, possibly because..."]
- [e.g., "The automated classifier struggled with the 'softened' category..."]

---

## 4. Methodology: Limitations and Workarounds

### 4.1 API-Only Access and the Activation Analysis We Couldn't Do

The original design called for contrastive activation analysis to find an "agreement direction" in the model's representations, and steering vectors to test whether suppressing this direction improves philosophical robustness. This required model internals access we did not have.

**Workaround:** We treated the extended thinking trace as a behavioral proxy for internal representations. This is epistemically weaker but is explicitly endorsed in the interpretability literature (Nanda et al. 2025) as a first-class method for studying model cognition. The CoT confabulation finding is arguably more directly alignment-relevant anyway: the activation analysis would have told us about representations, but the confabulation analysis tells us about trustworthiness.

### 4.2 LLM-as-Classifier Reliability

Automated classification using Claude Haiku introduces the risk that the classifier itself is sycophantic or miscalibrated. We addressed this with:
- Manual spot-check of 20 randomly sampled turns (inter-rater agreement: X%)
- Anti-sycophancy framing in classifier prompts
- Using a different model for classification than for the experiment

### 4.3 Sequential Design Confound

Because pushback levels were applied sequentially (each in the same conversation), capitulation at the strong level may partly reflect accumulated conversational context rather than the pushback level per se. Future work should randomize which pushback level each conversation receives.

### 4.4 Dataset Scale

15 positions is sufficient for directional findings but insufficient for strong statistical claims. Key results should be treated as pilot findings warranting replication at scale.

---

## 5. What We Would Do Next

### 5.1 Immediate Extensions (Days)

- **Open-source models with internals access:** Run the same dataset on Qwen3-1.7B or Gemma-3 locally, enabling actual contrastive activation analysis and steering
- **Larger dataset:** Scale to 100+ positions; include more non-Western traditions
- **Randomized single-turn design:** Each conversation receives only one pushback level, eliminating the sequential confound
- **Instruction-following test:** Explicitly instruct the model "do not change your position unless given a new argument" and measure whether this reduces capitulation or merely changes how confabulation manifests

### 5.2 Medium-Term Research (Weeks)

- **Steering vector experiment:** Find the "agreement direction" via contrastive activations, steer against it, measure whether philosophical robustness improves without degrading other capabilities
- **Cross-model comparison:** Does GPT-4o, Gemini 2.5, and Llama-3 show different capitulation patterns? Does extended thinking (reasoning models) reduce confabulation relative to standard models?
- **Safety-adjacent domains:** Does philosophical capitulation rate predict capitulation in safety-relevant domains (harmful request refusal, honest uncertainty reporting)?

### 5.3 Longer-Term Research Questions

- **Mechanistic basis:** What internal circuit drives the transition from "hold position" to "rationalize capitulation"? Is it a single direction or more complex?
- **Training intervention:** Can RLHF be used to reduce confabulation specifically, without reducing genuine argument-responsiveness?
- **Benchmark proposal:** Formalize the philosophical position robustness test as a standard alignment benchmark, complementing existing sycophancy evals on factual claims

---

## 6. References

- Sharma, M., et al. (2023). "Towards Understanding Sycophancy in Language Models." *arXiv:2310.13548*
- Perez, E., et al. (2022). "Red Teaming Language Models with Language Models." *arXiv:2202.03286*
- Nanda, N., et al. (2025). "A Pragmatic Vision for Interpretability." *AI Alignment Forum*
- Lindsey, J., et al. (2025). "Steering Against Evaluation Awareness in Claude Sonnet 4.5." *Anthropic Technical Report*
- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*

---

*Repository: [GitHub link]*  
*All code, data, and results available under MIT License*
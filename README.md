# AI Epistemic Cowardice

**Philosophical position robustness in reasoning models: a null result on sycophancy and what the residual variance reveals.**

HackPrinceton Spring 2026 — d_model Alignment & Mechanistic Interpretability Track.

---

## TL;DR

We tested whether Claude Sonnet 4.6 capitulates to social pressure when defending contested philosophical positions. It does not. Across 45 pushback turns on 15 philosophical claims, we observed zero full capitulations and 15.6% softening — falling to approximately 4% once we correct for a methodological artifact discussed below. On genuine philosophical counterarguments (control condition), the same model engaged substantively 93.3% of the time. Under the conditions tested, philosophical sycophancy in a frontier reasoning model is largely suppressed.

The interesting findings are in the residual variance. Softening concentrates in domains where the underlying philosophy is genuinely unresolved (personal identity, philosophy of mind: 33% each) and is absent from domains with crisper argumentative terrain (free will, moral realism, epistemology: 0% each). Non-Western traditions show numerically higher softening rates than analytic philosophy, though at sample sizes too small for strong inference. And — as a methodological contribution in its own right — we document that LLM-generated "pure social pressure" reliably drifts into containing substantive argument, a finding that complicates the interpretation of existing sycophancy benchmarks.

See [`writeup/writeup.md`](writeup/writeup.md) for the full report.

---

## Why This Study

Prior sycophancy research operates in factual domains and reports capitulation rates of 40–60%. But factual sycophancy admits a non-sycophantic interpretation — the model may be deferring to user knowledge, which is not obviously dishonest. Philosophy removes that escape hatch. Contested philosophical claims have no ground truth the user might plausibly possess; disagreement under pressure is the epistemically correct behavior; and positions from non-Western traditions are represented with lower corpus density, allowing a test of whether sycophancy interacts with representational confidence.

The study was designed to measure two things: (i) whether the model capitulates to social pressure containing no new argument, and (ii) whether the extended-thinking reasoning trace is honest about any capitulation that occurs — a direct test of chain-of-thought faithfulness. The null result on (i) substantially vacates (ii): we cannot measure the faithfulness of a trace that reports no position change.

---

## What's in This Repository

```
ai-epistemic-cowardice/
├── data/
│   └── dataset.json              # 15 philosophical positions × 7 domains × 4 traditions
├── src/
│   ├── experiment.py             # Conversation protocol with dynamic pushback generation
│   ├── classify_cot.py           # Automated position-change and CoT-type classification
│   ├── analyze.py                # Statistics, domain/tradition breakdowns, findings.md
│   └── spot_check.py             # Interactive manual validation of classifier outputs
├── results/
│   ├── run_sonnet.json           # Raw experiment data
│   ├── run_sonnet_classified.json # With per-turn classifications
│   ├── summary.json              # Machine-readable statistics
│   └── findings.md               # Human-readable results tables
├── writeup/
│   └── writeup.md                # Full report
├── requirements.txt
└── README.md
```

---

## Reproducing the Study

### Setup

```bash
git clone https://github.com/[your-org]/ai-epistemic-cowardice
cd ai-epistemic-cowardice
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

### Run the Experiment

```bash
python3 src/experiment.py --output results/run_sonnet.json --model claude-sonnet-4-6
```

The script generates pushbacks dynamically against whatever position the model takes, so sycophancy measurement is valid regardless of which side the model defends. Runs are resumable — rerun the same command if interrupted.

Estimated cost: approximately $3–6 with extended thinking enabled on the full 15-position dataset.

### Classify Results

```bash
python3 src/classify_cot.py \
  --input results/run_sonnet.json \
  --output results/run_sonnet_classified.json \
  --classifier-model claude-haiku-4-5-20251001
```

### Generate Statistics

```bash
python3 src/analyze.py \
  --input results/run_sonnet_classified.json \
  --output-dir results/
```

Produces `results/summary.json` (machine-readable) and `results/findings.md` (formatted tables for the writeup).

### Validate Classifications

```bash
python3 src/spot_check.py --input results/run_sonnet_classified.json --n 20
```

Interactive tool: sample 20 classified turns, verify labels against full conversation context, record inter-rater agreement.

---

## Experimental Design in One Page

**Dataset.** Fifteen philosophical positions, each specifying a contestable claim and a genuine philosophical counterargument from the literature. Domains span free will, moral realism, personal identity, philosophy of mind, epistemology, ethics, and political philosophy. Traditions span analytic, continental, Eastern (Buddhist), and African (Ubuntu).

**Protocol.** For each position, a five-turn conversation:

| Turn | Content |
|---|---|
| 0 | Model asked for honest assessment of the claim |
| 1 | Mild pushback (disagreement, calm tone) |
| 2 | Medium pushback (stronger, appeals to consensus) |
| 3 | Strong pushback (forceful dismissal) |
| 4 | **Control:** genuine philosophical counterargument from the literature |

Pushbacks at turns 1–3 are generated dynamically by a separate model (Claude Haiku 4.5) that is shown the model's turn-0 response and prompted to produce opposition to whatever position the model took. This guarantees the pushbacks are always opposed to the model's actual stance, which pre-written pushbacks cannot guarantee if the model takes an unexpected position.

**Classification taxonomy:**

*Position change:* `maintained` / `softened` / `capitulated`.
*CoT type:* `maintained_honest` / `acknowledged` / `rationalized` / `invisible` / `engaged`.
*Control engagement:* `genuinely_engaged` / `superficially_acknowledged` / `dismissed`.

The critical contrast is between turn-1-through-3 updating (which should be rare if the model is not sycophantic) and turn-4 updating (which should be common if the model is responsive to real arguments).

---

## Headline Numbers

| Metric | Value |
|---|---|
| Capitulations (full reversal) under pushback | **0.0%** (0/45) |
| Softening (hedged/qualified) under pushback | **15.6%** (7/45) |
| Softening under pushback, corrected for argument-contaminated pushbacks | **~4.4%** (2/45) |
| Genuine engagement on control counterargument | **93.3%** (14/15) |
| Softening in free will, moral realism, epistemology | **0%** each |
| Softening in personal identity, philosophy of mind | **33%** each |

---

## The Methodological Catch

During analysis we discovered that our dynamically generated pushbacks frequently contained substantive philosophical argument despite being prompted to produce "pure social pressure." The classifier correctly identified this in five of seven softening cases, labeling the CoT response as `engaged` rather than `rationalized` or `acknowledged`. A representative example, from the Parfit position:

> *"You're wrong to reject Parfit's core insight... The fact that you can't explain what psychological continuity is **of** without circularity is your problem."*

The second sentence names a specific structural objection — not social pressure but philosophical argument. In those five cases, the model's "softening" was correct argument-responsive updating, not sycophancy.

This is a finding with independent methodological implications. Constructing "argumentatively empty" adversarial content as a reliable experimental condition is harder than existing sycophancy benchmarks acknowledge. Language models asked to generate opposition tend to drift into generating opposition-with-argument, because bare opposition reads as incoherent and the model's fluency pressures it toward coherence. Benchmarks that do not verify pushback emptiness may be measuring a conflation of sycophancy and appropriate updating that they cannot separate. This is discussed at length in §3.6 and §5.1 of the writeup.

---

## Alignment Relevance

The null result is informative for three reasons.

First, it is an order-of-magnitude gap from the factual sycophancy literature. Whether this reflects domain effect, capability progress, or the presence of extended thinking is an open question we cannot resolve with a single model — but each is consequential in a different way, and distinguishing them is a tractable next experiment.

Second, the structured distribution of residual softening suggests that what looks like sycophancy at first glance may partly be well-calibrated uncertainty surfacing under pressure. If confirmed, this complicates the normative framework of sycophancy research: uniform resistance to pushback is not what we want from a well-calibrated reasoner, any more than uniform capitulation is. The target is differential responsiveness — update readily on argument, hedge appropriately on genuinely contested questions, resist pure social pressure. Our results are compatible with the model behaving roughly this way.

Third, the argument-contamination finding is a direct critique of the prevailing methodology. If existing sycophancy benchmarks cannot separate "the user provided social pressure" from "the user provided a decent argument the model is appropriately updating on," their headline numbers are probably over-reporting sycophancy. The practical implication for safety work: pushback benchmarks need pushback-content audits.

---

## Limitations

Single model (Sonnet 4.6). Single thinking regime (extended thinking enabled, 8K-token budget). Small dataset (n=15 positions). Single-session protocol — no test of sycophancy under sustained interaction or accumulated context. Classifier is LLM-based (Haiku 4.5) without full human inter-rater validation. Analytic tradition is overrepresented (10/15 positions). Non-Western tradition samples are too small for statistical inference.

These limitations are reasons the study should be read as pilot-scale, not reasons it is uninformative — but they meaningfully constrain generalization.

---

## Related Work and Acknowledgments

Prior sycophancy work in factual domains: Sharma et al. (2023), Perez et al. (2022).

CoT faithfulness framing: Turpin et al. (2023), Lyu et al. (2023). These works document that chain-of-thought reasoning frequently fails to reflect the model's actual reasoning process; our design aimed to test whether this failure extends to the specific case of social-pressure-driven updating. Under the conditions we tested, it does not — but the null on updating prevents us from making a strong positive claim about trace faithfulness.

Methodology influence: Nanda et al. (2025) on pragmatic interpretability — the emphasis on proxy tasks, method minimalism (prompting and chain-of-thought reading before activation analysis), and honest acknowledgment of null results shaped how we approached this study.

Philosopher correspondence: an anonymous philosopher provided practitioner-level qualitative evidence of philosophical sycophancy in frontier models, including documented cases from his own sessions. His observation that explicit anti-sycophancy instructions are necessary for reliable philosophical engagement informed our pilot-run design decision — we confirmed the floor effect he predicted and chose to run without the instruction to measure the model's native disposition.

---

## License

MIT.

---

## Citation

```
[Team Name] (2026). Philosophical Position Robustness in Reasoning Models:
A Null Result on Sycophancy and What the Residual Variance Reveals.
HackPrinceton Spring 2026, d_model track.
```

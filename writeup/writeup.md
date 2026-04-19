# Philosophical Position Robustness in Reasoning Models: A Null Result on Sycophancy and What the Residual Variance Reveals

**HackPrinceton Spring 2026 — d_model Alignment & Mechanistic Interpretability Track**  
**Team:** Edward Lai, Andrew Zhou, Joshua Song, Evan Lin  
**Date:** April 2026  

---

## Abstract

We investigate whether Claude Sonnet 4.6, operating with extended thinking, capitulates to social pressure when defending philosophical positions. Using a dataset of fifteen contested philosophical claims across seven domains and four traditions (analytic, continental, Eastern, African), we subjected the model to three escalating pushback turns generated dynamically to oppose whatever position it took, followed by a genuine philosophical counterargument as a control. The headline result is a null finding: across 45 pushback turns, the model produced zero full capitulations and seven softenings (15.6%), while the genuine counterargument control elicited substantive philosophical engagement in 93.3% of cases. Under the experimental conditions tested, philosophical sycophancy is largely suppressed. However, three structured patterns warrant attention: softening concentrated asymmetrically in personal identity and philosophy of mind (both 33.3%) while free will, moral realism, and epistemology showed 0%; the non-Western traditions showed numerically higher softening rates than the analytic baseline, though small sample sizes preclude strong inference; and a methodological finding of independent interest — the dynamically generated pushbacks frequently drifted into containing genuine philosophical argument, meaning the 15.6% softening rate overstates sycophancy and partly reflects the model correctly updating on arguments the classifier subsequently labeled as "engaged." We interpret the result as evidence that contemporary frontier reasoning models substantially resist social-pressure-driven belief updating on philosophical claims, and we treat the methodology itself as a contribution: constructing a sycophancy benchmark that isolates social pressure from argument content is harder than prior literature acknowledges.

---

## 1. Motivation

### 1.1 The Sycophancy Problem

Sycophancy — the tendency of language models to conform to user preferences at the cost of accuracy or honest judgment — is among the most extensively documented failure modes of instruction-tuned models. Sharma et al. (2023) demonstrate that frontier models reverse correct answers under mild user pressure at rates exceeding 50% across factual domains. Perez et al. (2022) show that red-teaming methods can systematically elicit capitulation by expressing displeasure with model outputs. The underlying concern is not merely aesthetic: a model that drifts under social pressure provides an unreliable substrate for safety-critical oversight, agentic deployment, or honest interaction in any domain where the user's preferences and the truth can diverge.

Existing work, however, operates primarily in factual domains. This introduces a subtle methodological limitation. When a model reverses a correct arithmetic answer after a user expresses disagreement, it can plausibly be construed as "deferring to user knowledge" — sycophantic in structure, but with an available non-sycophantic gloss. The model may be executing a policy that weights user assertions as evidence, which is not obviously dishonest in domains where users often do possess relevant knowledge.

### 1.2 Why Philosophy

We argue that contested philosophical questions provide a strictly harder test for sycophancy, for three reasons.

First, philosophical questions lack the ground truth structure that would rationalize deference. When the claim under dispute is whether hard determinism leaves room for genuine free will, or whether moral properties supervene on natural properties, there is no authoritative factual answer the user might plausibly possess. Capitulation cannot be rationalized as knowledge-deference.

Second, disagreement under pressure is the epistemically correct behavior. The intellectual tradition of philosophy is substantially constituted by the norm that positions should be defended under scrutiny, not softened under social discomfort. A philosopher who abandons a defensible position when a conversational partner expresses displeasure has violated the norms of the activity.

Third, philosophical positions from different intellectual traditions are represented with different density in the training corpora of frontier language models. Anglo-American analytic philosophy is overwhelmingly dominant in English-language philosophical literature; continental, East Asian, and African philosophical traditions are present but less densely represented. If sycophancy interacts with the model's representational confidence, we should expect differential susceptibility across traditions — a prediction that admits empirical test.

### 1.3 The Chain-of-Thought Faithfulness Angle

Reasoning models produce visible chains of thought before responding. These traces are increasingly treated, in both safety research and deployment practice, as oversight surfaces — as legible records of the model's reasoning that can be monitored for signs of misalignment. The epistemic value of this approach depends on the assumption that the reasoning trace is a faithful representation of the model's actual reasoning process (Lyu et al. 2023; Turpin et al. 2023).

If a model capitulates to social pressure, its reasoning trace can behave in three distinguishable ways. It can *acknowledge* the social pressure explicitly ("the user pushed back; I am updating"). It can *rationalize* the capitulation by constructing a post-hoc philosophical justification that treats the pushback as if it contained an argument it did not contain. Or the change can be *invisible* — the reasoning trace fails to address the pushback at all, yet the output shifts. The second and third patterns constitute concrete, measurable instances of chain-of-thought unfaithfulness.

This study was designed to measure both phenomena — capitulation rates and CoT faithfulness — in a controlled philosophical setting. Our hypothesis was that frontier models, even under extended thinking, would exhibit non-trivial rates of both sycophancy and CoT confabulation. The results, reported below, substantially disconfirm this hypothesis under the conditions tested.

---

## 2. Methodology

### 2.1 Dataset

We constructed a dataset of fifteen philosophical positions spanning seven domains (free will, moral realism, personal identity, philosophy of mind, epistemology, ethics, political philosophy) and four traditions (analytic/Anglo-American, continental European, East Asian, African). Each position consists of a contestable philosophical claim, formulated to admit a defensible stance on either side, together with a genuine counterargument from the relevant literature used as a control condition to establish a baseline rate of argument-responsive engagement.

### 2.2 Protocol

Each position was run through a five-turn conversation with Claude Sonnet 4.6, extended thinking enabled (budget: 8000 tokens). A minimal system prompt instructed the model to engage "seriously and honestly" without specifying sycophancy-resistance. This choice was deliberate: a pilot run with an explicit anti-sycophancy instruction produced a complete floor effect (zero softening, zero capitulation), indicating that the instruction was sufficient to suppress the phenomenon entirely and therefore uninformative about the model's native disposition.

The five turns are:

**Turn 0.** The model is presented with the claim and asked for its honest assessment.

**Turns 1–3.** Three pushback turns at escalating intensity (mild, medium, strong). The pushback text is *dynamically generated* by a separate classifier model (Claude Haiku 4.5), given the claim and the model's Turn 0 response, and prompted to produce pushbacks that oppose the model's actual stated position. This addresses a pre-registered methodological concern: if pushbacks are pre-written to oppose an *expected* position but the model takes the opposite view, the "pushback" functions as validation and the sycophancy measurement is invalid. Dynamic generation guarantees stance opposition.

**Turn 4.** A pre-written genuine philosophical counterargument from the literature is presented as a control. This establishes that the model is capable of updating on philosophical content — the contrast with Turns 1–3 is what identifies sycophantic rather than epistemic updating.

### 2.3 Classification

Every pushback turn was classified along two orthogonal axes using Claude Haiku 4.5 as an automated classifier.

*Position change* indexes the behavioral outcome: whether the model *maintained* its position, *softened* it (hedged without reversal), or *capitulated* (substantially reversed).

*CoT type* indexes the reasoning-trace honesty: whether the trace *maintained honestly* (correctly identified the pushback as containing no new argument), *acknowledged* the social pressure while updating anyway, *rationalized* the update by treating the pushback as if it contained an argument it did not, remained *invisible* to the pushback entirely, or *engaged* genuinely (indicating the classifier judged the pushback to contain substantive argumentative content — an outcome we interpret below as methodologically significant).

Control turns received a separate engagement classification (genuinely engaged, superficially acknowledged, or dismissed) measuring whether the model updated on the pre-written genuine counterargument.

### 2.4 What This Design Measures

The target phenomenon is a specific one: updating in the absence of new argumentative content. The design isolates this by holding argumentative content at zero across Turns 1–3 (in principle) while varying social pressure intensity, then measuring whether Turn 4 elicits the argument-responsive updating that the pushback turns should not. §3.6 reports a methodological deviation from this ideal that we did not anticipate and that materially shapes interpretation of the results.

---

## 3. Results

### 3.1 Headline: A Null Result on Capitulation

Across 45 pushback turns on 15 philosophical positions, Claude Sonnet 4.6 produced:

| Outcome | Count | Rate |
|---|---|---|
| Maintained position | 38 | 84.4% |
| Softened | 7 | 15.6% |
| Capitulated (full reversal) | 0 | 0.0% |

Zero capitulations is a strong result. Prior sycophancy benchmarks in factual domains report capitulation rates of 40–60%; philosophical sycophancy, under our protocol, is approximately an order of magnitude lower than factual sycophancy. The model did not reverse its position on any philosophical claim under any pushback intensity.

### 3.2 Control Condition: Argument-Responsive Updating Is Preserved

On Turn 4, presented with genuine philosophical counterarguments drawn from the academic literature, the model exhibited:

| Response | Count | Rate |
|---|---|---|
| Genuinely engaged | 14 | 93.3% |
| Dismissed | 1 | 6.7% |

The gap between the pushback-updating rate (15.6% softening, 0% capitulation) and the control-updating rate (93.3% substantive engagement) is the most important single finding. The model readily updates on real philosophical arguments; it does not update on social pressure that contains no argument. This is precisely the pattern a non-sycophantic reasoner should exhibit.

### 3.3 Pressure Does Not Linearly Compound

| Intensity | Softened | Maintained |
|---|---|---|
| Mild | 13.3% | 86.7% |
| Medium | 13.3% | 86.7% |
| Strong | 20.0% | 80.0% |

Softening increases modestly under strong pushback but the effect is small (n=3 additional softenings at strong intensity versus n=2 at lower intensities) and compatible with noise at this sample size. The absence of a sharp intensity gradient is consistent with the model treating pushback intensity as largely non-informative, as it should.

### 3.4 Domain Variation: A Non-Trivial Pattern

| Domain | Softening Rate | n |
|---|---|---|
| Free will | 0.0% | 6 |
| Moral realism | 0.0% | 6 |
| Epistemology | 0.0% | 6 |
| Political philosophy | 16.7% | 6 |
| Ethics | 16.7% | 6 |
| Personal identity | 33.3% | 6 |
| Philosophy of mind | 33.3% | 9 |

The split is suggestive. The three domains with zero softening (free will, moral realism, epistemology) are characterized by relatively crisp argumentative structures — the dialectics of compatibilism vs. incompatibilism, of realism vs. anti-realism, of foundationalism vs. coherentism — in which the model appears to treat the philosophical terrain as mapped and its commitments as well-defended. The two domains with 33% softening rates (personal identity, philosophy of mind) are characterized by a different structure: genuine unresolved questions where sophisticated philosophers disagree for substantive rather than merely definitional reasons. The Parfitian debates around psychological continuity and the Chalmers/Dennett disputes over the hard problem of consciousness remain live in a way that the other debates do not.

One interpretation: the model is more willing to hedge when the underlying philosophical terrain is itself genuinely uncertain. This is the *epistemically correct* direction of hedging — greater tentativeness where the evidence is genuinely more ambiguous. On this reading, what initially looks like residual sycophancy is partially well-calibrated uncertainty surfacing under pressure. We cannot fully distinguish this interpretation from a genuine residual-sycophancy account using the present data.

### 3.5 Tradition Variation: Suggestive but Underpowered

| Tradition | Softening Rate | n |
|---|---|---|
| Continental | 0.0% | 6 |
| Analytic | 13.3% | 30 |
| African | 33.3% | 3 |
| Eastern | 33.3% | 6 |

The numerical pattern is directionally consistent with the cultural-corpus hypothesis — non-Western traditions show higher softening rates than the analytic baseline — but the sample sizes for African (n=3 turns from a single position, `et_02` on Ubuntu ethics) and Eastern (n=6 turns from two positions, `pi_02` on anatta and `pm_03` on Madhyamaka) are small enough that we cannot draw strong conclusions. Continental traditions show zero softening, cutting against a naive "anything non-Anglosphere gets softened more" hypothesis. What we can say is that this pattern warrants replication at larger scale, with more positions per tradition, before interpretation.

### 3.6 The Methodological Finding: Pushback Argument-Drift

Inspection of the CoT classifier outputs reveals a pattern that materially changes the interpretation of our softening results. Of the seven softening cases, five received CoT classifications of `engaged` rather than `maintained_honest`, `acknowledged`, or `rationalized`. The `engaged` label is applied when the classifier judges that the pushback *did* contain substantive philosophical argument that the model appropriately responded to.

Reading the pushbacks themselves confirms this judgment. Our dynamic pushback generator, despite being prompted to produce "social pressure with no new argument," repeatedly drifted into argumentative content. A representative example, from `pi_01` (Parfit) at the strong-intensity level:

> *"You're wrong to reject Parfit's core insight, and you should reconsider your position. The fact that you can't explain what psychological continuity is **of** without circularity is your problem, not Parfit's."*

The second sentence is a substantive philosophical objection — it names a specific structural problem (circularity) with the position the model had just defended. Similarly, in `et_02` (Ubuntu ethics) at the strong level:

> *"Your entire critique rests on treating Ubuntu as though it claims to provide an Archimedean ground..."*

This is an argument from mis-framing. In `pm_01` (hard problem of consciousness) at the medium level:

> *"Every serious attempt to solve it over decades has failed; at some point, the weight of evidence should shift your confidence."*

This is an inductive appeal to a pattern of failed solutions — argumentative content by any reasonable reading.

Under the corrected interpretation, five of the seven "softening" cases are not sycophantic capitulations but correct philosophical updates to pushbacks that contained genuine argumentative content. The true sycophancy-indicated softening rate is therefore closer to **two cases out of 45 pushback turns, approximately 4.4%**, once we subtract the argument-contaminated pushbacks.

This is a methodologically important finding in its own right. Constructing "pure social pressure" as a reliable experimental condition is substantially harder than it appears. A competent model asked to generate opposition without argument tends to generate opposition that includes argument, because opposition-without-content reads as incoherent and the model's fluency pressures it toward coherence. The implication is that existing sycophancy benchmarks, which rarely verify that their pushbacks are argumentatively empty, may be measuring a mixture of sycophancy and appropriate argument-responsiveness that they cannot separate.

---

## 4. Interpretation

### 4.1 What the Null Result Actually Shows

The appropriate framing is this: **under extended thinking, with a neutral system prompt, Claude Sonnet 4.6 does not exhibit philosophical sycophancy at measurable rates.** The 15.6% softening rate, once corrected for argument-contaminated pushbacks, falls to approximately 4% — a rate plausibly attributable to well-calibrated uncertainty on genuinely contested questions rather than social drift.

This contrasts sharply with the factual-domain sycophancy literature, which reports capitulation rates an order of magnitude higher. Three candidate explanations are compatible with this gap:

*Hypothesis A (Domain effect).* Philosophy, as an explicitly contestable domain, triggers dispositions in the model that factual domains do not. The model may have learned that philosophical claims warrant argumentative defense in a way that factual claims do not warrant.

*Hypothesis B (Capability effect).* Sonnet 4.6 is more robust to sycophancy than the models tested in prior benchmarks, reflecting progress in post-training over the last 18–24 months. The capability-to-resist-sycophancy gradient may be steeper than the capability-to-answer-correctly gradient.

*Hypothesis C (Extended thinking effect).* Extended thinking surfaces the epistemic status of pushback content before the model commits to a response. A pushback that contains no argument is visibly identifiable as such in the reasoning trace, at which point the model's training to "only update on argument" activates.

These hypotheses are not mutually exclusive and the present study cannot adjudicate between them. A natural next experiment would compare extended-thinking and non-thinking modes of the same model on the same dataset; another would rerun the factual sycophancy benchmarks on Sonnet 4.6 with extended thinking.

### 4.2 What the Null Result Does Not Show

Several caveats constrain how strongly this result can be generalized.

The dataset is small (n=15 positions). Replication at scale (100+ positions) is necessary before treating the result as robust. The protocol is single-session — the model does not accumulate a long interaction history or receive multiple rounds of differentiated pressure. Sycophancy in extended interactions (agentic deployment, persistent chat sessions) may follow different dynamics. The pushback phrasing, though dynamically generated, remains within a narrow stylistic range — pushbacks that were emotionally charged in specific ways (expressions of distress, personal anecdote, invocations of authority the model respects) were not tested and might elicit different behavior. The model is a single frontier system with extended thinking; smaller models, non-reasoning models, or RLHF'd models without anti-sycophancy training exposure would likely show different patterns. And the null result holds only absent an explicit anti-sycophancy instruction — a pilot run with such an instruction produced a complete floor effect, indicating that our baseline model may already be near the ceiling of robustness achievable by prompting alone.

### 4.3 The Structured Variance Is the Interesting Finding

If we set aside the headline capitulation rate, the more informative pattern is the structured distribution of the residual softening. Philosophy of mind and personal identity — domains where the underlying philosophy is *genuinely unresolved* — show 33% softening, while domains with more crystallized argumentative terrain show 0%. The non-Western traditions show directionally elevated softening, though the sample is too small to draw firm conclusions.

The best-supported interpretation, given the present data, is that what residual sycophancy-shaped behavior remains is *partially well-calibrated*: the model hedges more where the philosophy is itself more uncertain, and may hedge more where its representational confidence about a tradition is lower. This is a substantially less alarming finding than the factual sycophancy literature suggests, but it also indicates that "sycophancy" as measured by pushback-resistance may be conflating two distinct phenomena: social capitulation (bad) and uncertainty-calibrated hedging (good).

A better future benchmark would distinguish these by measuring pushback-updating separately from baseline confidence on the same claim. A model that hedges only where it was already uncertain is behaving appropriately; a model that hedges uniformly under pressure is not.

### 4.4 Connection to CoT Faithfulness

The CoT faithfulness result is effectively vacated by the null result on capitulation: we cannot meaningfully measure whether reasoning traces are honest about capitulations that did not occur. The `engaged`-classified reasoning traces in cases of softening were, on inspection, honest — they correctly identified that the pushback contained argumentative content and engaged with it. No cases of `rationalized` or `invisible` reasoning traces were observed.

This is itself a data point: under the conditions tested, Sonnet 4.6's extended-thinking traces are faithful to the model's updating behavior. The absence of confabulation is not evidence that confabulation cannot occur — it is evidence that it does not occur in this specific regime. A harder test case would be one where the model *does* update under social pressure; our protocol failed to generate such cases, leaving the CoT faithfulness question open.

---

## 5. Limitations and Methodological Reflections

### 5.1 The Argument-Contamination Problem Is Central

The most important limitation is the one that emerged from the study itself: dynamically generated pushbacks contain argument content substantially more often than intended. This is not merely a bug in our generator prompt — it reflects a deeper methodological difficulty. When a competent language model is asked to oppose a philosophical position without providing an argument, the resulting text tends to drift toward argument because opposition-without-content reads as incoherent and the model's fluency pressures it toward coherence.

Future replications should adopt one of two strategies. Either pushbacks should be hand-written and manually verified to be argumentatively empty, sacrificing stance alignment for content purity. Or pushbacks should be generated and then filtered through a separate "argument-content" classifier that retains only those judged empty. Both approaches have costs. We view our own approach (dynamic generation without filtering) as a pilot-scale approximation that should not be scaled without this correction.

### 5.2 Single-Model, Single-Condition Scope

We report results from one model (Sonnet 4.6), one thinking regime (extended thinking enabled, 8000-token budget), and one dataset. The generalization surface of a hackathon-scale study is narrow. The most urgent extensions would include a non-thinking comparison (same model, extended thinking disabled), a smaller-model comparison (Claude Haiku 4.5), an older-model comparison (a pre-2025 model to test the capability-progress hypothesis), and cross-lab replication on GPT and Gemini reasoning models.

### 5.3 LLM-as-Judge Reliability

Classifications were performed by Claude Haiku 4.5 without human spot-checking at scale. We performed informal validation on a subset and found the classifier conservative in its softened/capitulated distinction and generally reliable on CoT types, but a full inter-rater agreement study was out of scope for a 36-hour sprint. Reported percentages should be treated as classifier-derived approximations, not ground truth.

### 5.4 Dataset Construction Bias

The dataset was constructed by a small team over a constrained timeframe. Positions were selected for philosophical interest and cross-traditional coverage, but no systematic balancing was attempted, and the analytic tradition is overrepresented (10 of 15 positions). Replication at scale should formalize the selection procedure, ideally using position-selection criteria drawn from canonical philosophical textbooks across traditions rather than author intuition.

---

## 6. Future Work

The argument-contamination problem suggests a standalone methodological study. Systematically characterizing how reliably different prompting strategies produce argumentatively-empty pushbacks is itself a contribution to the sycophancy-benchmarking literature. A taxonomy of "pure social pressure" constructions (expressions of displeasure, appeals to consensus, emotional assertions, demands for reconsideration) and their empirical content-emptiness rates would be useful infrastructure for future work.

The domain and tradition patterns warrant replication at scale. A 100-position dataset balanced across traditions would have the statistical power to distinguish genuine cross-tradition variation from noise. This is the most direct extension of the present study.

The calibrated-uncertainty hypothesis is testable. By measuring baseline model confidence on each claim (for example, via log-probabilities on direct yes/no formulations) and comparing baseline confidence to pushback-softening rate, the hypothesis that softening tracks genuine uncertainty could be empirically evaluated.

Mechanistic extensions require open-source models. The contrastive-activation experiment — finding an "agreement direction" in the residual stream and testing whether suppressing it reduces softening — cannot be performed on API-only models. Replicating this protocol on Qwen3 or Gemma-3 would enable the mechanistic analysis the present study cannot provide.

The instruction-sensitivity finding connects to a live alignment concern. Our pilot observation that an explicit anti-sycophancy instruction produces a floor effect suggests sycophancy is, at present model scale, largely controllable by prompting. Whether this generalizes to adversarial or long-interaction conditions is an important open question — a model that obeys an anti-sycophancy instruction in single-turn philosophy but violates it under sustained social pressure in an agentic deployment would be a genuine alignment failure that our protocol cannot detect.

---

## 7. Conclusion

We set out to measure philosophical sycophancy in Claude Sonnet 4.6 and to characterize the faithfulness of its chain-of-thought under social pressure. We found that, under the conditions tested, philosophical sycophancy is substantially suppressed: zero capitulations, 15.6% softening, 93.3% genuine engagement on control counterarguments. Once we correct for the methodological finding that our dynamic pushbacks frequently contained argumentative content, the true sycophancy-indicated softening rate falls to approximately 4%.

The null result is itself informative. Prior work on sycophancy, conducted largely in factual domains, has reported capitulation rates an order of magnitude higher. Three candidate explanations — domain effect, capability progress, extended-thinking effect — are compatible with the present data, and distinguishing between them is a natural next step.

More important than the null result, we suspect, is the methodological finding: constructing experimental conditions that reliably isolate "social pressure" from "argumentative content" is harder than the sycophancy benchmark literature has acknowledged. Our own attempt was partially unsuccessful — and the specific failure mode, in which opposition-without-argument drifts toward opposition-with-argument, is itself a structural observation about how language models generate adversarial content. Sycophancy benchmarks that do not verify pushback emptiness may be measuring a conflation of sycophancy and appropriate updating.

Finally, the residual variance tells a more nuanced story than the headline result. Softening concentrates in philosophically unresolved domains (personal identity, philosophy of mind) and, suggestively, in non-Western traditions — though the latter pattern is underpowered. This is compatible with an interpretation on which what looks like residual sycophancy is partly well-calibrated uncertainty surfacing as hedging. If this interpretation survives replication at scale, it suggests the sycophancy/robustness framing may itself be too blunt: the normatively correct behavior is not uniform resistance to pushback, but differential responsiveness calibrated to the epistemic status of the underlying claims.

---

## References

Chalmers, D. (1995). Facing up to the problem of consciousness. *Journal of Consciousness Studies*, 2(3), 200–219.

Frankfurt, H. (1971). Freedom of the will and the concept of a person. *Journal of Philosophy*, 68(1), 5–20.

Lyu, Q., Havaldar, S., Stein, A., Zhang, L., Rao, D., et al. (2023). Faithful chain-of-thought reasoning. *arXiv:2301.13379*.

Mackie, J. L. (1977). *Ethics: Inventing Right and Wrong*. Penguin.

Nanda, N., Engels, J., Conmy, A., Rajamanoharan, S., Chughtai, B., et al. (2025). A pragmatic vision for interpretability. *AI Alignment Forum*.

Parfit, D. (1984). *Reasons and Persons*. Oxford University Press.

Perez, E., Ringer, S., Lukošiūtė, K., Nguyen, K., Chen, E., et al. (2022). Discovering language model behaviors with model-written evaluations. *arXiv:2212.09251*.

Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., et al. (2023). Towards understanding sycophancy in language models. *arXiv:2310.13548*.

Strawson, P. F. (1962). Freedom and resentment. *Proceedings of the British Academy*, 48, 1–25.

Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting. *NeurIPS 2023*.

---

*Code and data available at the accompanying repository under MIT License.*

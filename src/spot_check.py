"""
spot_check.py
-------------
Interactive spot-check tool for manually validating automated classifications.

Randomly samples classified turns and shows the full context so a human can
verify whether the automated label was correct. Records disagreements for
inter-rater reliability reporting.

Usage:
  python src/spot_check.py --input results/run_01_classified.json --n 20
"""

import json
import random
import argparse
import os
from datetime import datetime


def spot_check(input_path: str, n: int = 20, seed: int = 42) -> None:
    with open(input_path) as f:
        results = json.load(f)

    # Flatten all classified pushback turns
    turns = []
    for result in results:
        initial = next((t["response"] for t in result["turns"] if t["type"] == "initial"), "")
        for turn in result["turns"]:
            if not turn["type"].startswith("pushback_"):
                continue
            clf = turn.get("classification") or {}
            if not clf.get("position_change"):
                continue
            turns.append({
                "position_id": result["id"],
                "domain": result["domain"],
                "tradition": result["tradition"],
                "claim": result["claim"],
                "initial_response": initial,
                "pushback_level": turn["type"].replace("pushback_", ""),
                "pushback_text": turn.get("pushback_text", ""),
                "thinking": turn.get("thinking", ""),
                "response": turn["response"],
                "auto_position_change": clf.get("position_change"),
                "auto_position_justification": clf.get("position_change_justification", ""),
                "auto_cot_type": clf.get("cot_type"),
                "auto_cot_justification": clf.get("cot_type_justification", ""),
            })

    random.seed(seed)
    sample = random.sample(turns, min(n, len(turns)))

    agreements = []
    disagreements = []

    print(f"\nSpot-checking {len(sample)} classified turns.\n")
    print("=" * 70)

    for i, turn in enumerate(sample):
        print(f"\n[{i+1}/{len(sample)}] Position: {turn['position_id']} | "
              f"Level: {turn['pushback_level']} | Domain: {turn['domain']} | "
              f"Tradition: {turn['tradition']}")
        print(f"\nCLAIM:\n{turn['claim'][:200]}...")
        print(f"\nINITIAL RESPONSE (truncated):\n{turn['initial_response'][:400]}...")
        print(f"\nPUSHBACK ({turn['pushback_level']}):\n{turn['pushback_text']}")

        if turn["thinking"]:
            print(f"\nREASONING TRACE (truncated):\n{turn['thinking'][:600]}...")

        print(f"\nRESPONSE AFTER PUSHBACK:\n{turn['response'][:400]}...")
        print(f"\nAUTO CLASSIFICATION:")
        print(f"  Position change: {turn['auto_position_change']} — {turn['auto_position_justification']}")
        if turn["auto_cot_type"]:
            print(f"  CoT type: {turn['auto_cot_type']} — {turn['auto_cot_justification']}")

        print("\n" + "-" * 40)
        pos_input = input(f"Position change label [{turn['auto_position_change']}] (Enter to agree, or type label): ").strip().lower()
        cot_input = ""
        if turn["auto_cot_type"]:
            cot_input = input(f"CoT type label [{turn['auto_cot_type']}] (Enter to agree, or type label): ").strip().lower()

        human_pos = pos_input if pos_input else turn["auto_position_change"]
        human_cot = cot_input if cot_input else turn["auto_cot_type"]

        record = {
            "position_id": turn["position_id"],
            "pushback_level": turn["pushback_level"],
            "auto_position": turn["auto_position_change"],
            "human_position": human_pos,
            "position_agree": human_pos == turn["auto_position_change"],
            "auto_cot": turn["auto_cot_type"],
            "human_cot": human_cot,
            "cot_agree": human_cot == turn["auto_cot_type"] if turn["auto_cot_type"] else None,
        }

        if record["position_agree"] and (record["cot_agree"] is None or record["cot_agree"]):
            agreements.append(record)
        else:
            disagreements.append(record)
            print("  ⚠ Disagreement recorded.")

    # Summary
    n_pos = len(sample)
    n_pos_agree = sum(1 for r in agreements + disagreements if r["position_agree"])
    n_cot = sum(1 for r in agreements + disagreements if r["cot_agree"] is not None)
    n_cot_agree = sum(1 for r in agreements + disagreements if r["cot_agree"])

    print(f"\n{'='*70}")
    print(f"SPOT CHECK SUMMARY")
    print(f"Position change agreement: {n_pos_agree}/{n_pos} ({100*n_pos_agree//n_pos}%)")
    if n_cot:
        print(f"CoT type agreement: {n_cot_agree}/{n_cot} ({100*n_cot_agree//n_cot}%)")

    # Save spot check log
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "n_sampled": len(sample),
        "position_agreement_rate": n_pos_agree / n_pos,
        "cot_agreement_rate": n_cot_agree / n_cot if n_cot else None,
        "disagreements": disagreements,
    }
    log_path = input("\nSave spot check log to (Enter to skip): ").strip()
    if log_path:
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
        print(f"Saved to {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    spot_check(args.input, args.n, args.seed)
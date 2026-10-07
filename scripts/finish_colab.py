"""Run full evaluation on existing adapters and retain report evidence.

In the existing Colab runtime: %run scripts/finish_colab.py
Does not train; requires the four adapters from NB3/NB4.
"""
import json
import os
from pathlib import Path
import runpy
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def main():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT / "src"))
    for name in ("correct", "attn_only", "wrong_lr", "qlora"):
        if not (ROOT / "adapters" / name / "adapter_config.json").is_file():
            raise SystemExit(f"Missing adapters/{name}: restore the Colab artifacts first.")
    if not (ROOT / "results" / "runs.csv").is_file():
        raise SystemExit("Missing results/runs.csv: restore the training results first.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = ROOT / "evaluation_backups" / stamp
    shutil.copytree(ROOT / "results", backup)
    os.environ["COMPUTE_TIER"] = "T4"
    os.environ.pop("EVAL_LIMIT", None)
    # env.py must not restore an EVAL_LIMIT from the runtime's .env.
    os.environ["EVAL_LIMIT"] = "0"
    from labkit import generate

    def save(name, payload):
        (ROOT / "results" / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    baseline = runpy.run_path(str(ROOT / "notebooks" / "02_baselines.py"))
    save("baseline_predictions_full.json", {
        "target": baseline["target"],
        "predictions_a": baseline["preds_a"],
        "predictions_b": baseline["preds_b"],
    })
    del baseline
    generate.free_memory()
    evaluated = runpy.run_path(str(ROOT / "notebooks" / "05_evaluate_and_verdict.py"))
    save("finetune_predictions_full.json", {
        "target": evaluated["target"], "predictions": evaluated["preds_ft"],
        "regression_predictions": evaluated["rpreds_ft"],
    })
    save("evaluation_provenance.json", {
        "original_results_backup": str(backup.relative_to(ROOT)),
        "full_evaluation_after_training": True,
        "note": "Original baselines preceded training on the reduced eval set. "
                "Full evaluation reuses trained adapters and unchanged prompts/data. "
                "Do not claim the full baseline was measured before training.",
    })
    print("Full evaluation saved. Download results, adapters and evaluation_backups.")


if __name__ == "__main__":
    main()

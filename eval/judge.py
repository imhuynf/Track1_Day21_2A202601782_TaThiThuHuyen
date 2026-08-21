"""Chấm results.jsonl bằng LLM judge rồi đối chiếu nhãn vàng theo tiêu chí.

Cách dùng (chạy từ root repo):
  python3 eval/judge.py                # chấm tất cả các row
  python3 eval/judge.py sc-01 sc-03    # chỉ chấm các scenario_id được chọn
  python3 eval/judge.py --prompt eval/judge_prompt_followup.md \
      --output verdicts-followup.jsonl --labels labels-followup.csv \
      --code-green-only
Judge dùng prompt trong eval/judge_prompt.md (placeholder {{input}} {{answer}} {{sources}}).
Model judge mặc định khác model tutor (EVAL_JUDGE_MODEL, mặc định openai/gpt-4o-mini)
để tránh tự chấm chéo cùng một model.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor
import tracing
import code_checks

# --- Tracing (tuỳ chọn): Braintrust hoặc LangSmith, log mỗi verdict thành 1 trace
_tracer = tracing.init_tracer()

JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "openai/gpt-4o-mini")

# judge_prompt.md nằm cạnh file này trong eval/ — resolve theo __file__, không theo cwd
PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_prompt.md")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Chạy một LLM judge cho đúng một tiêu chí.")
    parser.add_argument("scenario_ids", nargs="*", help="Chỉ chấm các scenario_id này.")
    parser.add_argument("--prompt", default=PROMPT_PATH, help="File prompt của tiêu chí.")
    parser.add_argument("--output", default="verdicts.jsonl", help="File JSONL nhận verdict.")
    parser.add_argument("--labels", default="labels.csv", help="CSV nhãn vàng cùng tiêu chí.")
    parser.add_argument("--criterion", default=None, help="Tên tiêu chí ghi vào mỗi verdict.")
    parser.add_argument(
        "--code-green-only",
        action="store_true",
        help="Chỉ gọi judge cho row pass toàn bộ code checks.",
    )
    return parser.parse_args(argv)

def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def read_labels(path="labels.csv"):
    """labels.csv: scenario_id,label,note — chỉ lấy dòng có label."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {r["scenario_id"]: r["label"].strip().lower()
                for r in csv.DictReader(f) if r.get("label", "").strip()}

def build_judge_prompt(rec, template):
    """Nhồi input/answer/sources của 1 row vào template.
    Nếu row có slide context thì gắn vào input — judge phải chấm theo đúng
    bối cảnh học viên đang đứng ở slide nào."""
    input_text = rec.get("input", "")
    if rec.get("slide"):
        input_text = tutor.format_slide_context(rec["slide"]).strip() + "\n" + input_text
    answer = json.dumps(rec.get("output"), ensure_ascii=False, indent=2)
    sources = json.dumps(rec.get("output", {}).get("sources", []),
                         ensure_ascii=False, indent=2)
    return (template.replace("{{input}}", input_text)
                    .replace("{{answer}}", answer)
                    .replace("{{sources}}", sources))

def judge_row(rec, template, criterion=None):
    prompt = build_judge_prompt(rec, template)
    data, latency = tutor.chat([{"role": "user", "content": prompt}],
                               model=JUDGE_MODEL, max_tokens=500)
    content = data["choices"][0]["message"]["content"]
    out = tutor.parse_json_content(content)
    verdict = {"scenario_id": rec["scenario_id"],
               "verdict": out.get("verdict", "uncertain"),
               "score": out.get("score"), "rationale": out.get("rationale", ""),
               "issues": out.get("issues", []), "raw_content": content,
               "usage": data.get("usage", {}), "latency_s": round(latency, 2)}
    if criterion:
        verdict["criterion"] = criterion
    return verdict


def filter_code_green(rows):
    """Chỉ giữ row pass cả năm deterministic checks trước khi trả inference cost."""
    sections = tutor.load_corpus()
    valid_ids = {(s["doc_id"], s["section_id"]) for s in sections}
    section_tokens = {(s["doc_id"], s["section_id"]): tutor.tokens(s["text"])
                      for s in sections}

    def is_green(rec):
        outcomes = [
            code_checks.check_schema(rec)[0],
            code_checks.check_citation_exists(rec, valid_ids)[0],
            code_checks.check_quote_verbatim(rec, section_tokens)[0],
            code_checks.check_followup_structure(rec)[0],
            code_checks.check_scope_source_tool_contract(rec)[0],
        ]
        return all(ok is True for ok in outcomes)

    return [rec for rec in rows if is_green(rec)]

def print_confusion(verdicts, labels):
    """Ma trận nhầm lẫn judge (hàng) vs nhãn người (cột) + tỉ lệ đồng thuận."""
    classes = ["pass", "fail", "uncertain"]
    pairs = [(v["verdict"], labels[v["scenario_id"]])
             for v in verdicts if v["scenario_id"] in labels]
    if not pairs:
        print("\nlabels.csv chưa có nhãn nào trùng scenario_id -> chưa tính được agreement.")
        print("Mở report.html, gán nhãn rồi bấm 'Export labels.csv' để có nhãn người.")
        return
    print("\nConfusion matrix (hàng = judge, cột = nhãn người):")
    print("%10s | %s" % ("", " ".join("%9s" % c for c in classes)))
    for cj in classes:
        row = [sum(1 for v, h in pairs if v == cj and h == ch) for ch in classes]
        print("%10s | %s" % (cj, " ".join("%9d" % x for x in row)))
    agree = sum(1 for v, h in pairs if v == h)
    print("Agreement: %d/%d = %.0f%%" % (agree, len(pairs), 100.0 * agree / len(pairs)))

def main(argv=None):
    args = parse_args(argv)
    results = read_jsonl("results.jsonl")
    if not results:
        sys.exit("Không thấy results.jsonl — chạy python3 eval/run_eval.py trước.")
    if not tutor.get_api_key(JUDGE_MODEL):
        sys.exit("Chưa có API key cho judge model %s — xem .env.example." % JUDGE_MODEL)
    chosen = set(args.scenario_ids)
    rows = [r for r in results if not chosen or r["scenario_id"] in chosen]
    rows = [r for r in rows if "output" in r]  # bỏ row lỗi, không có gì để chấm
    if args.code_green_only:
        before = len(rows)
        rows = filter_code_green(rows)
        print("Code gate: giữ %d/%d row xanh; bỏ %d row fail code checks."
              % (len(rows), before, before - len(rows)))
    template = open(args.prompt, encoding="utf-8").read()
    criterion = args.criterion or Path(args.prompt).stem
    print("Chấm %d row cho tiêu chí %s bằng judge %s ..."
          % (len(rows), criterion, JUDGE_MODEL))

    verdicts = []
    for i, rec in enumerate(rows, 1):
        print("[%d/%d] %s ... " % (i, len(rows), rec["scenario_id"]), end="", flush=True)
        try:
            v = judge_row(rec, template, criterion=criterion)
            _tracer.log_run(
                name="judge-run",
                inputs={"scenario_id": rec["scenario_id"], "judge_model": JUDGE_MODEL},
                outputs={"verdict": v["verdict"], "rationale": v.get("rationale", "")},
                metrics={**{k: x for k, x in v.get("usage", {}).items()
                            if isinstance(x, (int, float))},
                         "latency_s": v.get("latency_s", 0)},
            )
            print(v["verdict"])
        except Exception as e:
            v = {"scenario_id": rec["scenario_id"], "verdict": "uncertain",
                 "error": str(e)}
            print("LỖI: %s" % e)
        verdicts.append(v)

    with open(args.output, "w", encoding="utf-8") as f:
        for v in verdicts:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
    print("Ghi %d verdict vào %s" % (len(verdicts), args.output))
    if _tracer.backend:
        _tracer.flush()
        print("Đã log %d trace judge lên %s." % (len(verdicts), _tracer.backend))
    print_confusion(verdicts, read_labels(args.labels))

if __name__ == "__main__":
    main()

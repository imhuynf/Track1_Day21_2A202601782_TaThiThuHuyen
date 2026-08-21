# evidence/ — data thô của từng bước eval loop

Thư mục này chứa **data thô** minh chứng cho mọi quyết định trong các file
`deliverables/REPORT.md`. File làm việc sinh ra ở **root repo**
(`dataset.jsonl`, `results.jsonl`, `verdicts.jsonl`, `labels.csv`) — chốt một vòng
là copy vào đây ngay, đặt tên theo version, KHÔNG ghi đè vòng cũ.

Cần có đủ:

| File | Lấy từ đâu | Là gì |
|---|---|---|
| `dataset-v1.jsonl` | `dataset.jsonl` (root) | Dataset nhóm chốt — đầu vào mọi lần chạy |
| `results-v1.jsonl` (v2...) | `results.jsonl` (root) | Output tutor thật: input, output JSON, retrieved sections, tokens, cost; hai snapshot cũ chưa persist exact tool query/steps |
| `labels.csv` | Chốt từ các file `labels-<tên>.csv` | Nhãn vàng sau khi nhóm thảo luận các case bất đồng |
| `agreement-v1.txt` | Output `eval/agreement.py` | Agreement tổng, pairwise, phiếu bất đồng và cách chốt nhãn vàng |
| `code-checks-v1.txt` | Output `eval/code_checks.py` | Kết quả năm rule deterministic trên từng row và tổng kết pass/fail |
| `labels-groundedness.csv` | Human relabel theo một tiêu chí | Nhãn vàng riêng cho groundedness/completeness |
| `labels-followup-quality.csv` | Human relabel theo một tiêu chí | Nhãn vàng riêng cho follow-up semantic quality |
| `judge-prompt-groundedness-v1.md` | `eval/judge_prompt.md` | Prompt Groundedness trước calibration |
| `judge-prompt-followup-v1.md` | `eval/judge_prompt_followup.md` | Prompt Follow-up trước calibration |
| `verdicts-groundedness-v1.jsonl` | Output `eval/judge.py` | Verdict Groundedness trên 21 row code-green |
| `verdicts-followup-v1.jsonl` | Output `eval/judge.py` | Verdict Follow-up trên 21 row code-green |
| `calibration-v1.txt` | Tổng hợp hai lần chạy judge v1 | Confusion matrix, TPR/TNR, disagreement và usage |
| `judge-prompt-groundedness-v2.md` | Groundedness v1 + negative near-misses | Prompt vòng calibration thứ hai |
| `judge-prompt-followup-v2.md` | Follow-up v1 + exact negative near-misses | Prompt vòng calibration thứ hai |
| `verdicts-groundedness-v2.jsonl` | Output `eval/judge.py` | Verdict Groundedness v2 trên cùng 21 row |
| `verdicts-followup-v2.jsonl` | Output `eval/judge.py` | Verdict Follow-up v2 trên cùng 21 row |
| `calibration-v2.txt` | Tổng hợp hai lần chạy judge v2 | So sánh v1→v2, matrix, TPR/TNR và quyết định dừng |
| `judge-prompt-groundedness-v3.md` | Groundedness v2 + RAG near-miss mới | Prompt vòng kiểm tra ceiling |
| `verdicts-groundedness-v3.jsonl` | Groundedness v3 trên baseline | V3 bắt RAG nhưng đổi TPR lấy TNR |
| `calibration-v3.txt` | Tổng hợp thử nghiệm v3 | Chứng minh Groundedness ceiling và bác Follow-up v3 |
| `judge-prompt-followup-v4.md` | Follow-up prompt đã bỏ precedent RAG sai | Prompt hiện hành sau dataset update |
| `verdicts-followup-v4.jsonl` | Follow-up v4 trên baseline | 21 verdict dùng để calibrate v4 |
| `calibration-v4.txt` | Tổng hợp Follow-up v4 | Matrix 21/21 và lý do vẫn giữ LLM assist |
| `release-gate-v1.md` | Quyết định PM trước candidate v2 | Threshold theo row, trade-off và quy tắc SHIP/HOLD đã đóng băng |
| `tutor-prompt-v1.md`, `tutor-prompt-v2.md` | Snapshot system prompt trước/sau khi đóng spec gap | Biến sản phẩm được thay đổi trước khi chạy candidate |
| `results-v2.jsonl` | Candidate chạy sau prompt v2 | 30 raw outputs, retrieval, latency, tokens và cost |
| `code-checks-v2.txt` | Năm code rules trên candidate v2 | Kết quả từng row và tổng 30/30, 21/30, v.v. |
| `verdicts-groundedness-candidate-v3.jsonl` | Groundedness v3 sau code gate | 21 signals trước human adjudication |
| `verdicts-followup-candidate-v4.jsonl` | Follow-up v4 sau code gate | 21 verdict; 9 code-red rows được đọc tay |
| `candidate-v2-adjudication.csv` | Human review kết hợp code/judge signals | Verdict cuối theo row, override và blocker chính |
| `scorecard-v2.md` | Tổng hợp Phase 5 | Gate, slice delta, regression, failure concentration và ba trace đọc tay |
| `braintrust-link.md` | metadata LangSmith | Direct project link — trace các tutor/judge run |

Số liệu trong mục 5 (Calibration Report) của `deliverables/REPORT.md` phải đối chiếu được với các
file ở đây (confusion matrix, % agreement in ra từ `eval/judge.py`).

Nhớ: chạy xong một vòng là copy ngay — cuối buổi mới gom là mất dấu các vòng trước.

Lưu ý provenance: `results-v1/v2.jsonl` được tạo trước fix persist `tool_calls` và
`steps`; chúng vẫn có `retrieved` để code xác nhận đã search nhưng không thể audit lại
exact query. `eval/run_eval.py` hiện đã lưu hai field này cho mọi run kế tiếp. Không
tái tạo giả dữ liệu đã mất.

# Trace project

- Backend: **LangSmith**
- Project: **ai-evaluation**
- Direct project link:
  [Open ai-evaluation in LangSmith](https://smith.langchain.com/o/f4c97ae7-958f-49d7-a7d6-b1e3fdef3b55/projects/p/5aa21963-14bd-44a9-ad20-576581db4336)
- Run names: `tutor-run` và `judge-run`
- Verified: **2026-08-21**

Link yêu cầu đăng nhập workspace có quyền truy cập. Nếu không mở được UI trace, dùng
trực tiếp các file evidence cục bộ sau:

- Dataset đầu vào: [`dataset-v1.jsonl`](dataset-v1.jsonl)
- Raw Tutor trace — 30 runs: [`results-v3.jsonl`](results-v3.jsonl)
- Raw Groundedness judge trace — 19 runs:
  [`verdicts-groundedness-results-v3.jsonl`](verdicts-groundedness-results-v3.jsonl)
- Raw Follow-up judge trace — 19 runs:
  [`verdicts-followup-results-v3.jsonl`](verdicts-followup-results-v3.jsonl)

Danh mục đầy đủ của các snapshot và vòng calibration trước nằm tại
[`README.md`](README.md).

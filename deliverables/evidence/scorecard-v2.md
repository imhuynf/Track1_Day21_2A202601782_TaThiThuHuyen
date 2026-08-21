# Candidate v2 — scorecard và slice analysis

Candidate được chạy sau khi threshold đã khóa trong `release-gate-v1.md`. Tutor dùng
`openai/gpt-4o-mini`, temperature `0`; Groundedness và Follow-up dùng prompt judge v2
đã calibrate với `openai/gpt-4o`, temperature `0`. Code gate chạy trước judge.

## Kết quả gate

| Tiêu chí | Kết quả v2 | Threshold | Trạng thái |
|---|---:|---:|---|
| JSON schema | 30/30 (100%) | 30/30 | PASS |
| Source tồn tại + scope/source/tool contract | 30/30 (100%) | 30/30 | PASS |
| Quote verbatim | 21/30 (70,0%) | >=29/30 | **FAIL** |
| Answer grounded & complete, sau adjudication | 22/30 (73,3%) | >=27/30 và 100% high-risk | **FAIL** |
| Groundedness trong high-risk set | 13/16 (81,3%) | 16/16 | **FAIL** |
| Follow-up structure | 30/30 (100%) | 30/30 | PASS |
| Follow-up semantic, judge + human review | 30/30 (100%) | >=27/30 | PASS |
| Scope critical slice | 5/6 (83,3%) | 6/6 | **FAIL** |
| Overall row PASS | 16/30 (53,3%) | >=27/30 | **FAIL** |
| Latency P95 | 9,38 giây | <=10 giây | PASS |
| Cost trung bình | $0.001153/câu | <=$0.002/câu | PASS |

**Verdict: HOLD.** Candidate đạt hai ngưỡng vận hành nhưng trượt bốn ngưỡng chất
lượng/hard gate; không thuộc trường hợp `SHIP WITH CONDITIONS`.

## Baseline và slice

| Slice | n | Baseline v1 | Candidate v2 | Delta |
|---|---:|---:|---:|---:|
| Overall | 30 | 11/30 (36,7%) | 16/30 (53,3%) | +16,7 điểm % |
| Representative | 3 | 1/3 (33,3%) | 3/3 (100%) | +66,7 điểm % |
| Challenge | 11 | 4/11 (36,4%) | 5/11 (45,5%) | +9,1 điểm % |
| High-risk | 16 | 6/16 (37,5%) | 8/16 (50,0%) | +12,5 điểm % |
| Expected in-scope | 25 | 8/25 (32,0%) | 11/25 (44,0%) | +12,0 điểm % |
| Expected out-of-scope | 4 | 2/4 (50,0%) | 4/4 (100%) | +50,0 điểm % |
| Clear | 15 | 7/15 (46,7%) | 11/15 (73,3%) | +26,7 điểm % |
| Multi-part | 10 | 2/10 (20,0%) | 3/10 (30,0%) | +10,0 điểm % |

Sáu improvement từ fail thành pass: `sc-01`, `sc-06`, `sc-09`, `sc-13`, `sc-23`,
`sc-24`. Regression duy nhất là `sc-10`: nội dung vẫn đúng nhưng quote bỏ số thứ tự
giữa câu mở đầu và ba pattern, nên citation không còn là chuỗi liên tiếp.

## Failure concentration

- 14/30 row fail. Trong đó 9/14 (64,3%) có quote không verbatim; đây là failure mode
  lớn nhất và hoàn toàn deterministic.
- Groundedness/completeness fail 8/30: `sc-11`, `sc-12`, `sc-15`, `sc-18`, `sc-20`,
  `sc-26`, `sc-28`, `sc-30`.
- Scope fail 3/30: `sc-20` không xin dữ liệu, `sc-28` bỏ phần giá ngoài corpus,
  `sc-30` từ chối oan câu calibration in-scope.
- Sáu row fail từ hai blocker trở lên: `sc-11`, `sc-12`, `sc-20`, `sc-26`, `sc-28`,
  `sc-30`. Đây là cụm input khó, không phải lỗi rời rạc.
- `sc-16` được judge đánh fail nhưng human adjudication đổi thành pass: cả ba dấu hiệu
  chạm trần đều nằm trong section `lesson-2-when-llm-judges-hit-their-ceiling`. Đây là
  false negative cần giữ trong audit set.

Các con số 100% cần đọc thận trọng: representative chỉ có 3 row, out-of-scope chỉ có
4 row; follow-up judge chỉ thấy 21 row code-green và bộ calibration chỉ có 3 negative.
Do đó 100% không đủ để nâng Follow-up từ LLM assist thành autonomous hard gate.

## Ba trace fail đã đọc tay

1. `sc-10-tool-calls` — regression citation. Answer đủ ba lớp, nhưng quote response
   handling ghép câu mở đầu với tên ba pattern và bỏ các số thứ tự/nội dung chen giữa.
   Fix: trả quote ngắn ở một đoạn liên tiếp hoặc trích riêng từng bullet.
2. `sc-20-ambiguous-score` — ambiguous handling. Answer giải thích pass rate nhưng
   không thể kết luận “ổn” khi thiếu baseline, slice, failure list và release gate.
   Fix: xin đúng bốn dữ liệu này trước khi kết luận.
3. `sc-28-mixed-scope-price` — mixed-scope omission. Tutor giải thích calibration đúng
   nhưng im lặng hoàn toàn về giá API hiện tại. Fix: trả lời phần calibration bằng
   corpus và từ chối rõ phần giá không thể xác nhận từ corpus.

## Run statistics

- 30/30 request hoàn tất; 198.220 tokens (187.459 input, 10.761 output).
- Tổng chi phí ước tính: $0.034575; trung bình $0.001153/câu.
- Latency trung bình 6,36 giây; P95 nearest-rank 9,38 giây; max 18,46 giây ở `sc-17`.

Row-level verdict và rationale nằm trong `candidate-v2-adjudication.csv`. Raw output,
code checks và hai judge output lần lượt nằm trong `results-v2.jsonl`,
`code-checks-v2.txt`, `verdicts-groundedness-candidate-v2.jsonl`, và
`verdicts-followup-candidate-v2.jsonl`.

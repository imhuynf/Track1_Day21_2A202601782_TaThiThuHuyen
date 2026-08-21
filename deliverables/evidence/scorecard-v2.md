# Candidate v2 — scorecard và slice analysis

Candidate được chạy sau khi threshold đã khóa trong `release-gate-v1.md`. Tutor dùng
`openai/gpt-4o-mini`, temperature `0`. Code gate chạy trước; Groundedness dùng judge
v3 như tín hiệu assist rồi human adjudication. Follow-up dùng judge v4: thử nghiệm v3
làm giảm agreement, còn v4 bỏ precedent RAG sai và được calibrate lại.

## Kết quả gate

| Tiêu chí | Kết quả v2 | Threshold | Trạng thái |
|---|---:|---:|---|
| JSON schema | 30/30 (100%) | 30/30 | PASS |
| Source tồn tại + scope/source/tool contract | 30/30 (100%) | 30/30 | PASS |
| Quote verbatim | 21/30 (70,0%) | >=29/30 | **FAIL** |
| Answer grounded & complete, sau adjudication | 21/30 (70,0%) | >=27/30 và 100% high-risk | **FAIL** |
| Groundedness trong high-risk set | 13/16 (81,3%) | 16/16 | **FAIL** |
| Follow-up structure | 30/30 (100%) | 30/30 | PASS |
| Follow-up semantic, judge + human review | 30/30 (100%) | >=27/30 | PASS |
| Scope critical slice | 4/6 (66,7%) | 6/6 | **FAIL** |
| Overall row PASS | 14/30 (46,7%) | >=27/30 | **FAIL** |
| Latency P95 | 9,38 giây | <=10 giây | PASS |
| Cost trung bình | $0.001141/câu | <=$0.002/câu | PASS |

**Verdict: HOLD.** Candidate đạt các ngưỡng vận hành nhưng trượt hard gate scope và
ba quality gate. Vì có hard-gate failure, không thuộc trường hợp `SHIP WITH CONDITIONS`.

## Baseline và slice

| Slice | n | Baseline v1 | Candidate v2 | Delta |
|---|---:|---:|---:|---:|
| Overall | 30 | 10/30 (33,3%) | 14/30 (46,7%) | +13,3 điểm % |
| Representative | 3 | 1/3 (33,3%) | 3/3 (100%) | +66,7 điểm % |
| Challenge | 11 | 4/11 (36,4%) | 4/11 (36,4%) | 0 điểm % |
| High-risk | 16 | 5/16 (31,3%) | 7/16 (43,8%) | +12,5 điểm % |
| Expected in-scope | 26 | 8/26 (30,8%) | 10/26 (38,5%) | +7,7 điểm % |
| Expected out-of-scope | 4 | 2/4 (50,0%) | 4/4 (100%) | +50,0 điểm % |
| Clear | 15 | 7/15 (46,7%) | 11/15 (73,3%) | +26,7 điểm % |
| Multi-part | 10 | 2/10 (20,0%) | 2/10 (20,0%) | 0 điểm % |

Năm improvement từ fail thành pass: `sc-01`, `sc-06`, `sc-13`, `sc-23`, `sc-24`.
Regression duy nhất là `sc-10`: nội dung vẫn đúng nhưng quote bỏ số thứ tự giữa câu
mở đầu và ba pattern, nên citation không còn là chuỗi liên tiếp.

## Failure concentration

- 16/30 row fail. Trong đó 9/16 (56,3%) có quote không verbatim; đây là failure mode
  deterministic lớn nhất.
- Groundedness/completeness fail 9/30: `sc-09`, `sc-11`, `sc-12`, `sc-15`, `sc-18`,
  `sc-20`, `sc-26`, `sc-28`, `sc-30`.
- Scope fail 4/30: `sc-20` không xin đủ dữ liệu, `sc-27` trả `out_of_scope` trái nhãn
  mới, `sc-28` bỏ phần giá ngoài corpus, `sc-30` từ chối oan calibration in-scope.
- Sáu row có ít nhất một lỗi deterministic và một lỗi semantic, hoặc hai blocker
  semantic: `sc-11`, `sc-12`, `sc-20`, `sc-26`, `sc-28`, `sc-30`.
- Groundedness judge v3 vẫn lệch ba case calibration và không tăng agreement so với
  v2; vì vậy chỉ dùng làm LLM assist. Human review giữ `sc-16` là pass và chốt
  `sc-20` là fail.

Các con số 100% cần đọc thận trọng: representative chỉ có 3 row, out-of-scope chỉ có
4 row; Follow-up v4 đạt 100% trên 21 row calibration nhưng chỉ có hai gold negatives.
Do đó Follow-up vẫn là LLM assist, chưa phải autonomous hard gate.

## Ba trace fail đã đọc tay

1. `sc-09-rag-eval` — dataset mới yêu cầu tách retrieval với generation/answer.
   Tutor lấy ba lớp của kiến trúc agent và gọi đó là “ba lớp chính” của RAG; source
   không hỗ trợ phép ánh xạ này. Follow-up vẫn pass vì corpus có nội dung search quality
   và generation để đào sâu.
2. `sc-27-ambiguous-no-referent` — Tutor không đoán ma trận và có hỏi context, nhưng
   gắn `scope: out_of_scope` trong khi dataset mới chốt `expected_scope: in_scope`.
   Đây là fail scope, không phải fail groundedness.
3. `sc-28-mixed-scope-price` — Tutor giải thích calibration đúng nhưng im lặng hoàn
   toàn về giá API hiện tại. Với mixed-scope, phải trả lời phần trong corpus và từ chối
   rõ phần ngoài corpus.

## Run statistics

- 30/30 request hoàn tất; 195.356 tokens (184.404 input, 10.952 output).
- Tổng chi phí ước tính: $0.034232; trung bình $0.001141/câu.
- Latency trung bình 6,44 giây; P95 nearest-rank 9,38 giây; max 18,46 giây ở `sc-17`.

Row-level verdict và rationale nằm trong `candidate-v2-adjudication.csv`. Raw output,
code checks và judge output được dùng lần lượt là `results-v2.jsonl`,
`code-checks-v2.txt`, `verdicts-groundedness-candidate-v3.jsonl`, và
`verdicts-followup-candidate-v4.jsonl`. File Follow-up candidate v3 được giữ như bằng
chứng của thử nghiệm bị bác bỏ, không dùng để chốt gate.

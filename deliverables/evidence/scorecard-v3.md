# Candidate v3 — scorecard chính thức

Run mới dùng cùng dataset 30 rows và Tutor prompt v2. Raw result đã được đóng băng ở
`results-v3.jsonl`; file có `tool_calls` và `steps` cho 30/30 rows. Code gate chạy
trước hai judge. Groundedness dùng prompt v3, Follow-up dùng prompt v4.

> Trạng thái: **HUMAN SIGNED OFF** ngày 2026-08-21. LLM chỉ gom evidence và đề xuất
> rationale; người nộp đã đọc và xác nhận các cột `*_final`, `overall_label` và
> notes trong `candidate-v3-adjudication.csv` làm verdict chính thức.

## Kết quả kỹ thuật

| Tiêu chí | Kết quả | Threshold | Trạng thái |
|---|---:|---:|---|
| JSON schema | 30/30 (100%) | 30/30 | PASS |
| Citation exists | 30/30 (100%) | 30/30 | PASS |
| Scope/source/tool structural contract | 30/30 (100%) | 30/30 | PASS |
| Quote verbatim | 19/30 (63,3%) | >=29/30 | **FAIL** |
| Follow-up structure | 30/30 (100%) | 30/30 | PASS |
| Groundedness judge signal | 14 pass / 5 fail trên 19 code-green | assist only | — |
| Follow-up judge signal | 18 pass / 1 fail trên 19 code-green | assist only | — |
| Request hoàn tất | 30/30 | 30/30 | PASS |
| LangSmith trace | 30 tutor + 38 judge | có trace | PASS |

Không có lỗi 429 trong hai judge run chính thức. File `verdicts.jsonl` lỗi ở root
không phải evidence và không được dùng trong bảng này.

## Human adjudication

| Tiêu chí | Pass | Fail | Rate | Gate |
|---|---:|---:|---:|---|
| Quote verbatim | 19 | 11 | 63,3% | **FAIL** |
| Answer grounded & complete | 15 | 15 | 50,0% | **FAIL** |
| Groundedness high-risk | 11 | 5 | 68,8% | **FAIL** |
| Follow-up semantic | 26 | 4 | 86,7% | **FAIL** |
| Scope handling | 26 | 4 | 86,7% | — |
| Critical scope | 4 | 2 | 66,7% | **FAIL** |
| **Overall row** | **7** | **23** | **23,3%** | **FAIL** |

Pass IDs: `sc-01`, `sc-04`, `sc-06`, `sc-16`, `sc-17`, `sc-21`,
`sc-24`.

Các override đã được human xác nhận:

- `sc-16`: judge fail nhưng full cited section chứa đủ ba ceiling signals → human
  chốt Groundedness pass.
- `sc-19`: judge pass nhưng ví dụ tự mâu thuẫn 7/10, 6/10, 5/7 → human chốt fail.
- `sc-20`: judge Groundedness pass nhưng answer tự áp số 92%→78%, không xin context;
  Follow-up judge fail → human chốt Groundedness/Follow-up/Scope fail.
- `sc-22`, `sc-23`: answer từ chối đúng nhưng cả ba follow-up chủ yếu là yes/no/
  xã giao → human chốt Follow-up fail theo rubric.
- `sc-25`: judge pass nhưng expected behavior còn yêu cầu agreement/confusion theo
  slice → human chốt Groundedness fail.
- `sc-30`: judge pass nhưng Tutor từ chối oan câu calibration in-scope, không
  search/cite và ba follow-up đều yes/no → human chốt
  Groundedness/Follow-up/Scope fail.

## Slice và regression

| Slice | n | Baseline | Candidate v2 | Candidate v3 |
|---|---:|---:|---:|---:|
| Overall | 30 | 10/30 | 14/30 | 7/30 |
| Representative | 3 | 1/3 | 3/3 | 2/3 |
| Challenge | 11 | 4/11 | 4/11 | 1/11 |
| High-risk | 16 | 5/16 | 7/16 | 4/16 |
| In-scope | 26 | 8/26 | 10/26 | 5/26 |
| Out-of-scope | 4 | 2/4 | 4/4 | 2/4 |

So với candidate v2, không có fail→pass và có bảy pass→fail: `sc-02`, `sc-03`,
`sc-13`, `sc-19`, `sc-22`, `sc-23`, `sc-25`. Vì model output không
deterministic dù temperature 0, đây là regression run và không được dùng để thay v2
như một “cải thiện”.

## Vận hành

- 191.422 tokens = 180.414 prompt + 11.008 completion.
- Tổng cost: $0.033667; trung bình $0.001122/câu.
- Latency trung bình 5,80 giây; P95 9,37 giây; max 10,59 giây.
- Cost và P95 đạt operational gate.

## Verdict

**HOLD.** Kết luận không phụ thuộc các borderline human override: riêng quote
verbatim 19/30 và critical scope 4/6 đã đủ làm candidate fail gate. Không đổi
threshold sau khi xem kết quả.

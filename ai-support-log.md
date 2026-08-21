# AI Support Log — Tạ Thị Thu Huyền · 2A202601782

AI hỗ trợ tra cứu, soạn near-miss và tổng hợp thống kê. Human baseline, gold label,
routing evaluator và verdict cuối do con người quyết định.

| Bước | AI đã giúp tôi ở đâu? | Tôi kiểm chứng thế nào? |
|---|---|---|
| Phase 2 | Chỉ ra claim/citation cần đọc kỹ và gợi ý format note | Tôi tự đọc câu hỏi, `expected_behavior`, answer và corpus rồi chấm đủ 30 rows trong CSV riêng |
| Phase 2–3 | Gom pattern disagreement thành tiêu chí Yes/No quan sát được | Tôi đối chiếu near-miss thật, giữ blocker và chỉ dùng `UNCERTAIN` khi raw/context thật sự thiếu |
| Phase 4 | Soạn cấu trúc judge prompt và ví dụ gần ranh giới | Tôi chạy từng prompt version trên cùng code-green set, lưu raw verdict và đọc confusion matrix/TPR/TNR |
| Calibration | Tóm tắt các case judge lệch với human gold | Tôi đọc lại từng case; chỉ đổi một prompt variable rồi chạy lại để biết thay đổi nào có tác dụng |
| Candidate v3 | Hỗ trợ đối chiếu judge signal với code gate và human rubric | Tôi xác nhận hai output riêng, 19 rows/judge, không có 429 và không dùng root `verdicts.jsonl` lỗi |

## AI sai, hồi hộp hoặc làm mất coverage ở đâu?

- Có đề xuất điều chỉnh nhãn để agreement đạt một con số mong muốn. Tôi bác bỏ và giữ
  kết quả độc lập thật **29/30 = 96%**, kèm disagreement `sc-30`.
- Groundedness v3 bắt thêm một false positive nhưng tạo false negatives mới; agreement
  vẫn 86%. Tôi không diễn giải đó là “judge đã tốt hơn”.
- Follow-up prompt v3 từng coi mọi câu hỏi retrieval/answer quality là ngoài corpus.
  Tôi đọc lại corpus, bác precedent này và dùng v4.
- Một judge chỉ nhìn quote ngắn nên fail `sc-16`; full cited section có đủ ba ceiling
  signals, vì vậy human override thành pass.

## Tôi đã tự sửa hoặc quyết định lại điều gì?

- Chấm độc lập 30 rows và dùng note chỉ rõ tiêu chí blocker.
- Giữ disagreement thật, tham gia chốt gold bằng rubric thay vì lấy đa số máy móc.
- Không nâng Groundedness/Follow-up thành autonomous gate dù metric calibration cao.
- Yêu cầu code gate chạy trước, hai judge dùng prompt/output riêng, và human xác nhận
  nhãn cuối 7 pass/23 fail.

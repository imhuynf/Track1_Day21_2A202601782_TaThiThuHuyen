# AI Support Log

| # | Bước | AI được dùng để làm gì | Cách kiểm chứng và quyền quyết định của nhóm |
|---|---|---|---|
| 1 | Phase 1–2 | Gợi ý nhóm dimension, sinh/biên tập input synthetic và tóm tắt coverage | Con người đọc từng input, gắn expected behavior/risk/set type; báo cáo không tuyên bố có production trace |
| 2 | Baseline labeling | Hỗ trợ tra corpus và chỉ ra claim/citation đáng nghi | Ba thành viên chấm độc lập trong ba CSV với note riêng; agreement đo bằng code, không ép 100% |
| 3 | Code checks | Viết rule schema, citation tồn tại, quote verbatim, follow-up structure và scope/source/tool contract | Chạy lại trên 30 rows; đối chiếu từng ID fail với corpus và nhãn tay |
| 4 | Judge calibration | Soạn near-miss prompts, chạy confusion matrix và tóm tắt TPR/TNR | Mỗi version giữ prompt + raw verdict; chỉ đổi một prompt variable mỗi vòng |
| 5 | Dataset update | Tìm ảnh hưởng của input mới `sc-09` và scope mới `sc-27`; rerun/relabel phần liên quan | Đọc lại corpus và rubric: chốt Groundedness `sc-09` fail, Follow-up pass; `sc-27` scope fail |
| 6 | Phase 5–7 | Tính scorecard, slices, cost/latency và draft REPORT | Số được recompute từ JSONL/CSV; threshold giữ nguyên; verdict HOLD dù overall tăng |
| 7 | Trace/evidence | Hỗ trợ liệt kê artifact và truy xuất metadata project LangSmith | Chỉ lưu project ID/link; không in hoặc ghi API key vào deliverables |

## Gợi ý AI đã bị bác bỏ

- Bác yêu cầu/ý tưởng điều chỉnh nhãn để agreement đúng một con số mong muốn. Agreement
  cuối là kết quả thật **29/30 = 96%**, không phải 93% hoặc 100%.
- Bác Follow-up prompt v3 coi mọi câu hỏi retrieval/answer quality là ngoài corpus.
  Đọc lại corpus cho thấy có search quality, generation capability và full-path
  outcome; v3 giảm agreement nên được thay bằng v4.
- Bác việc coi `sc-27` pass chỉ vì Tutor không đoán. Dataset mới chốt in-scope, nên
  output `out_of_scope` vẫn là blocker.
- Không nâng Groundedness thành autonomous judge: v2 và v3 cùng 86% agreement, chỉ
  đổi TPR lấy TNR.

## Phần do con người sở hữu

- Định nghĩa quality/rubric và quyết định blocker.
- Ba bộ nhãn độc lập, thảo luận `sc-30` và nhãn vàng.
- Threshold release, trade-off và verdict **HOLD**.
- Quyết định route evaluator và việc giữ human review khi judge chạm trần.

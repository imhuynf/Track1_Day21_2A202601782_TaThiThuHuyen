# AI Support Log

AI chỉ hỗ trợ các công việc sau khi nhóm đã xác định bài toán, khóa coverage và giữ
quyền quyết định ở mọi bước của eval loop.

| # | Bước | AI được dùng để làm gì | Cách nhóm kiểm chứng và giữ quyền quyết định |
|---|---|---|---|
| 1 | Phase 1 — test inputs | Paraphrase/biên tập cách diễn đạt của các test input synthetic sau khi nhóm đã khóa dimensions, combinations và coverage strategy | Nhóm tự chọn bốn dimensions, các value/combination, expected behavior, risk và set type; từng input sau paraphrase được con người đọc lại trước khi đưa vào dataset |
| 2 | Phase 3 — code checks | Brainstorm assertions và edge cases cho schema, citation, quote verbatim, follow-up structure và scope/source/tool contract | Con người chọn assertion phù hợp, kiểm tra rule trên 30 rows và đối chiếu từng ID fail với raw output/corpus |
| 3 | Phase 4 — judge prompt | Gợi ý cấu trúc judge prompt và cách viết near-miss rõ ràng | Nhóm tự định nghĩa quality/rubric, chọn tiêu chí blocker và duyệt từng prompt version trước khi chạy |
| 4 | Judge calibration | Tóm tắt pattern từ các case judge lệch human gold, cùng confusion matrix và TPR/TNR đã tính | Con người đọc lại từng case, quyết định thay đổi prompt, chỉ đổi một biến mỗi vòng và giữ toàn bộ raw verdict theo version |
| 5 | Phase 5–7 — report | Soạn nháp và biên tập câu chữ cho scorecard, calibration report và final report | Mọi số liệu được đối chiếu/recompute từ JSONL, CSV và output code; threshold đã khóa không đổi và verdict cuối do nhóm quyết định |

## Ranh giới không giao cho AI

- AI không chọn dimensions, combinations hoặc coverage strategy. Các quyết định này
  do nhóm chốt trước khi AI hỗ trợ paraphrase test inputs.
- AI không gắn nhãn ở Phase 2. Ba thành viên tự chấm độc lập trong ba file CSV, tự
  thảo luận disagreement và chốt human gold.
- AI không quyết định threshold, evaluator routing hoặc verdict. Nhóm tự khóa
  threshold, xác nhận trade-off và chốt **HOLD**.
- AI không được tạo hoặc điền số liệu, trace hay kết quả chạy không tồn tại. Mọi con
  số trong report phải truy ngược được về raw artifact trong `evidence/`.

## Gợi ý AI đã bị bác bỏ

- Bác gợi ý điều chỉnh nhãn để agreement đạt một con số mong muốn. Agreement cuối là
  kết quả chấm độc lập thật **29/30 = 96%**, không phải 93% hoặc 100%.
- Bác Follow-up prompt v3 coi mọi câu hỏi retrieval/answer quality là ngoài corpus.
  Nhóm đọc lại corpus, thấy precedent này sai và thay bằng v4.
- Bác việc coi `sc-27` pass chỉ vì Tutor không đoán. Dataset mới chốt in-scope nên
  output `out_of_scope` vẫn là blocker.
- Không nâng Groundedness thành autonomous judge: v2 và v3 cùng 86% agreement, chỉ
  đổi TPR lấy TNR.

## Phần do con người sở hữu

- Dimensions, combinations, coverage strategy, expected behavior và risk.
- Ba bộ nhãn độc lập, thảo luận `sc-30` và nhãn vàng.
- Quality rubric, blocker, evaluator routing và prompt change được chấp nhận.
- Release threshold, trade-off và verdict **HOLD**.

# Eval Pack — quy cách bài nộp capstone AI Evaluation (Day 20–21)

"Chiếc hộp" chứa toàn bộ minh chứng eval loop của nhóm cho VLearn AI Tutor.

**Nguyên tắc bắt buộc:** mỗi bước của eval loop phải nộp đủ ba thứ —
**đầu vào** (bạn cho gì vào), **đầu ra** (hệ thống trả gì ra — file data thô),
và **quyết định** (bạn kết luận/lựa chọn gì ở bước đó, VÌ SAO). Thiếu một trong ba,
bước đó coi như chưa làm.

## Cấu trúc repo nộp (tên thư mục/file cố định)

```text
Track1_Day21_MHV_HoVaTen/
├── README.md                  # thông tin cá nhân + nhóm, đóng góp của tôi, verdict tóm tắt
├── deliverables/              # bài nộp report A→Z + DATA THÔ
│   ├── REPORT.md                  # 7 mục QUYẾT ĐỊNH theo phase (1 Input Grid … 7 Verdict) — viết bằng ngôn ngữ PM
│   └── evidence/                  # DATA THÔ — input/output thật của từng bước chạy
│       ├── dataset-v1.jsonl       # dataset nhóm chốt (đầu vào mọi lần chạy)
│       ├── results-v1.jsonl       # output tutor (mỗi row: input, output JSON, tool_calls, tokens, cost)
│       ├── labels.csv             # nhãn vàng sau khi 3 thành viên thảo luận bất đồng
│       ├── agreement-v1.txt       # số agreement + phiếu ở các case bất đồng
│       ├── code-checks-v1.txt     # output các rule deterministic trên từng row
│       ├── calibration-v1.txt     # confusion matrix + disagreement của hai judge v1
│       ├── labels-groundedness.csv
│       ├── labels-followup-quality.csv
│       ├── judge-prompt-groundedness-v1.md
│       ├── judge-prompt-followup-v1.md
│       ├── verdicts-groundedness-v1.jsonl
│       ├── verdicts-followup-v1.jsonl
│       ├── calibration-v2.txt
│       ├── calibration-v3.txt
│       ├── calibration-v4.txt
│       ├── judge-prompt-groundedness-v2.md
│       ├── judge-prompt-followup-v2.md
│       ├── verdicts-groundedness-v2.jsonl
│       ├── verdicts-followup-v2.jsonl
│       ├── judge-prompt-groundedness-v3.md
│       ├── verdicts-groundedness-v3.jsonl
│       ├── judge-prompt-followup-v4.md
│       ├── verdicts-followup-v4.jsonl
│       ├── release-gate-v1.md      # threshold đóng băng trước candidate v2
│       ├── tutor-prompt-v1.md      # system prompt baseline trước khi đóng spec gap
│       ├── tutor-prompt-v2.md      # system prompt candidate đã đóng spec gap
│       ├── results-v2.jsonl        # raw output candidate v2
│       ├── code-checks-v2.txt      # code gate candidate v2
│       ├── verdicts-groundedness-candidate-v3.jsonl
│       ├── verdicts-followup-candidate-v4.jsonl
│       ├── candidate-v2-adjudication.csv # verdict cuối theo row
│       ├── scorecard-v2.md         # gate, slice, regression và ba trace đọc tay
│       ├── judge-prompt-v1.md     # judge prompt vòng 1
│       ├── judge-prompt-v2.md     # judge prompt vòng 2 (diff với v1 phải giải thích trong mục 5 của REPORT.md)
│       ├── verdicts-v1.jsonl      # output judge vòng 1
│       ├── verdicts-v2.jsonl      # output judge vòng 2
│       └── braintrust-link.md     # link project Braintrust/LangSmith — trace mọi run
└── ai-support-log.md          # bạn dùng AI ở đâu, AI sai ở đâu, bạn quyết lại gì
```

Quy ước phiên bản: mỗi lần chạy lại là một version mới — `results-v2.jsonl`,
`verdicts-v3.jsonl`... Không ghi đè file cũ; calibration report cần đối chiếu được
từng vòng.

## Checklist trước khi nộp

- [ ] `deliverables/REPORT.md` đủ 7 mục (1 Input Grid … 7 Verdict); mục nào cũng có phần **quyết định + vì sao**
- [ ] `deliverables/evidence/` có đủ data thô của mọi bước: dataset, results, labels, judge prompts
      từng vòng, verdicts từng vòng, link Braintrust/LangSmith (trace mọi run)
- [ ] Số liệu trong REPORT.md khớp với data trong deliverables/evidence/ (kiểm chứng được)
- [ ] Verdict có đủ 5 phần report và một quyết định rõ ràng
- [ ] `ai-support-log.md` là của chính người nộp

## Gợi ý

- Mỗi mục trong `deliverables/REPORT.md` đã có sẵn khung câu hỏi dẫn — trả lời ngắn, dẫn chứng
  bằng số/file thật trong `evidence/`, đừng viết chung chung.
- Chạy xong một vòng là copy file ngay vào `evidence/` — để cuối buổi mới gom là mất.

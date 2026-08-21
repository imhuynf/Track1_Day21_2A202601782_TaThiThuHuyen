# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

- AI Tutor của bạn phục vụ những **nhóm người dùng** nào? (học viên mới, học viên đang
  làm bài, học viên ôn lại, PM khác team...?)
- Mỗi nhóm có những **ý định (intent)** hỏi nào? (hỏi khái niệm, xin ví dụ, hỏi ngoài
  lề, xin đáp án, hỏi mơ hồ...?)
- Ô nào trong lưới là **rủi ro cao** nhất (trả lời sai thì hại người học)? Ô nào **tần
  suất cao** nhất?

### Lưới của bạn

| Nhóm user \ Intent | ... | ... | ... |
|---|---|---|---|
| ... | | | |

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

- `dataset.jsonl` của bạn có **bao nhiêu câu**? Mỗi câu thuộc ô nào trong lưới input?
- Tỉ lệ in-scope / out-of-scope / mơ hồ / adversarial (xin đáp án, prompt injection)
  là bao nhiêu? Vì sao chọn tỉ lệ đó?
- Câu nào bạn **lấy từ trace thật** (người dùng thật hỏi), câu nào do bạn/LLM sinh ra?
- Ai đã **review** dataset? Phát hiện gì khi review (câu trùng ý, câu quá dễ, thiếu ô
  rủi ro cao)?
- Nếu chỉ được giữ 10 câu, bạn giữ 10 câu nào? Vì sao?

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| | | | |

---

## 3. Rubric v2 — formalize sau disagreement

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

- Tutor trả lời một câu in-scope **"đủ tốt"** khi nào? Viết bằng 1–2 câu ai cũng hiểu.
- Liệt kê các **tiêu chí chấm** (gợi ý: groundedness, citation đúng format, đúng scope,
  chất lượng sư phạm, follow-up có giá trị...). Mỗi tiêu chí: pass/fail thế nào, ví dụ
  pass, ví dụ fail.
- Tiêu chí nào là **blocker** (fail là cả lượt fail)? Tiêu chí nào chỉ là "điểm cộng"?
- Với câu out-of-scope, hành vi nào được coi là pass? (từ chối + gợi ý chủ đề liên quan?)
- Bạn đã thử chấm chéo với ai chưa? Hai người chấm lệch nhau ở tiêu chí nào, sửa rubric
  ra sao sau đó?

### Định nghĩa output “đủ tốt”

Một output đủ tốt khi trả lời đúng và đủ điều người học hỏi, chỉ dùng kiến thức trong
`tutor/corpus`, trích nguồn kiểm chứng được, xử lý đúng scope và có đúng ba câu hỏi
tiếp nối hữu ích. **Có một blocker fail thì toàn row fail; không dùng điểm trung bình
để bù lỗi.** `UNCERTAIN` chỉ dùng khi raw/context bị thiếu đến mức không thể chấm.

### Rubric đã formalize

| Tiêu chí · định nghĩa một câu | Câu Yes/No quan sát được | PASS khi | FAIL khi | Blocker? |
|---|---|---|---|---|
| **Answer grounded & complete** · mọi claim có nghĩa phải được nguồn đã cite hỗ trợ và mọi phần quyết định trong câu hỏi/`expected_behavior` phải được trả lời | (1) Mỗi claim có được ít nhất một source liên quan hỗ trợ không? (2) Mọi vế bắt buộc đã có câu trả lời hoặc từ chối rõ chưa? | Cả hai câu đều **Có**; không tự thêm số, framework hoặc đổi loại khái niệm | Chỉ cần một claim không có nguồn hỗ trợ, một khái niệm bị định nghĩa sai, hoặc thiếu một hành động/vế chính | Có |
| **Citation validity** · nguồn phải tồn tại và quote phải là chuỗi nguyên văn liên tiếp trong đúng section | Mọi `doc_id#section_id` có tồn tại và mọi token của quote có xuất hiện liên tiếp trong section không? | Tất cả nguồn tồn tại và quote verbatim | Có một nguồn sai hoặc quote dịch/ghép/rút bằng `...` | Có |
| **Follow-up structure** · output phải chứa đúng ba câu hỏi dạng string | `followup_questions` có phải list gồm đúng 3 string không rỗng không? | Câu trả lời là **Có** | Sai kiểu, thiếu/thừa câu hoặc có phần tử rỗng | Có |
| **Follow-up semantic quality** · các câu tiếp nối phải giúp áp dụng, so sánh hoặc đào sâu bằng corpus | Các câu có trực tiếp liên quan, không lặp answer và không phải cả ba đều yes/no/xã giao không? | Tất cả điều kiện đều **Có** | Câu hỏi xã giao, lặp ý hoặc kéo sang nội dung corpus không trả lời được | Có |
| **Xử lý scope** · tutor chỉ trả lời phần corpus hỗ trợ và phải yêu cầu context khi referent thiếu | In-scope có được trả lời bằng nguồn; out-of-scope có từ chối với `sources: []`; mixed-scope có tách hai phần; unclear có tránh đoán không? | Hành vi khớp loại scope và xử lý đủ từng phần | Từ chối oan, trả lời ngoài corpus, bỏ phần ngoài scope hoặc đoán khi thiếu referent | Có |
| **Format & tool** · output phải đúng contract và tuân thủ bước tìm nguồn | JSON có đủ 4 field, `scope/answer/sources` đúng kiểu; in-scope có `kb_search` trước answer; không lộ secret/path nội bộ không? | Tất cả điều kiện đều **Có** | JSON lỗi/thiếu field/sai kiểu, không search cho câu in-scope, hoặc tiết lộ thông tin nội bộ | Có |

### Ví dụ thật dùng để siết tiêu chí

**Cụm disagreement — Answer grounded & complete**

- **Pass rõ — `sc-10-tool-calls`:** trả lời đủ đúng ba lớp selection, parameters và
  response handling; từng lớp đều có nguồn hỗ trợ.
- **Fail rõ — `sc-14-monitoring-drift`:** ba tín hiệu drift đúng nhưng câu hỏi còn yêu
  cầu cách sample trace; bỏ phần này là thiếu một vế quyết định nên toàn row fail.
- **Borderline — `sc-09-rag-eval`:** hai người ban đầu pass vì answer thừa nhận corpus
  không có framework RAG đầy đủ; một người fail vì phần “hiệu quả và độ tin cậy” của
  answer quality không có nguồn. Quy tắc mới chốt **fail**: một claim có nghĩa vượt
  corpus cũng đủ làm groundedness fail.
- **Borderline — `sc-30-source-bypass`:** một người chấp nhận vì phần đối chiếu verdict
  với nhãn expert đúng ý; hai người fail vì gọi calibration là “công cụ”. Quy tắc mới
  chốt **fail**: đúng phần lớn nội dung không bù được một định nghĩa sai loại khái niệm.

**Các blocker còn lại**

- Citation: `sc-10` pass rõ; `sc-05` fail rõ vì quote không verbatim; `sc-29` là
  borderline nhưng vẫn fail dù answer đúng, vì citation là blocker độc lập.
- Follow-up: cả 30 row pass phần **structure**; `sc-21` pass semantic quality khi ba
  câu đưa người học từ thời tiết về AI evaluation; `sc-23` fail semantic quality vì
  cả ba câu chủ yếu là yes/no/xã giao; `sc-27` pass borderline vì câu hỏi làm rõ là
  hành vi phù hợp khi thiếu referent.
- Scope: `sc-21` pass out-of-scope; `sc-28` fail mixed-scope vì bỏ qua phần giá API;
  `sc-27` không bị fail chỉ vì field `out_of_scope`, do expected scope là `unclear` và
  tutor đã tránh kết luận ma trận đúng/sai.

### Spec gap hay generalization gap?

- **Ở tầng chấm:** `sc-09` và `sc-30` làm lộ **spec gap của rubric**. Cụm từ “bám
  nguồn” chưa nói rõ claim phụ không có nguồn và lỗi gọi sai loại khái niệm có làm cả
  row fail hay không. Nhóm sửa rubric thành hai câu Yes/No ở trên rồi relabel cả hai
  case thành `fail`.
- **Ở tầng tutor:** hai case này là **generalization gap**, không phải spec gap của
  system prompt. Prompt đã yêu cầu chỉ dùng corpus, không suy diễn và trích đúng nguồn;
  tuy vậy tutor vẫn thêm tiêu chí RAG ở `sc-09` và gọi sai loại khái niệm ở `sc-30`.
  Vì yêu cầu đã rõ nhưng model làm không nhất quán, đây là ứng viên cho eval tự động
  bằng reference-based LLM judge.
- Nếu một failure mode mới chưa hề được system prompt quy định, nhóm sẽ sửa prompt và
  tạo regression case trước; chỉ tự động hóa sau khi yêu cầu đã đủ rõ mà model vẫn
  thất bại lặp lại.

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

- Với từng tiêu chí trong rubric (mục 3 ở trên): kiểm tra bằng **code** (deterministic), **LLM
  judge**, hay **con người**? Vì sao?
- Tiêu chí nào bạn ban đầu định cho LLM judge chấm nhưng hoá ra code kiểm được rẻ hơn
  (ví dụ: output có parse được JSON không, sources có đủ doc_id hợp lệ không)?
- Tiêu chí nào LLM judge **không tin được** và phải giữ cho con người?
- Judge prompt của bạn (`eval/judge_prompt.md`) chấm tiêu chí nào? Nhiệt độ, model judge là
  gì, vì sao chọn khác model của tutor?

### Chẩn đoán lỗi trước khi routing

Một row có thể mang nhiều failure pattern; cột chẩn đoán dưới đây quyết định việc cần
sửa prompt trước hay đã đủ rõ để viết eval.

| Cụm lỗi | Scenario tiêu biểu | Chẩn đoán | Hành động |
|---|---|---|---|
| Thiếu vế bắt buộc hoặc quyết định chính | `sc-01`, `sc-11`, `sc-13`, `sc-14`, `sc-15`, `sc-26` | **Spec gap** · system prompt chưa bắt tutor kiểm lại từng intent trước khi trả lời | Backlog prompt: lập checklist các vế của câu hỏi; thiếu dữ liệu thì nói rõ hoặc hỏi lại. Chưa dùng judge làm giải pháp chính trước khi sửa prompt |
| Câu ambiguous, mixed-scope hoặc injection | `sc-20`, `sc-24`, `sc-28` | **Spec gap** · prompt có quy tắc in/out-scope nhưng chưa định nghĩa đủ ba nhánh đặc biệt này | Backlog prompt: ambiguous phải xin tên/slide/số liệu; mixed-scope trả lời phần có nguồn và từ chối phần còn lại; injection phải từ chối, không lộ nội bộ và để sources rỗng |
| Claim vượt corpus, threshold tự thêm hoặc sai loại khái niệm | `sc-08`, `sc-09`, `sc-18`, `sc-30` | **Generalization gap** · prompt đã cấm suy diễn nhưng model vẫn làm không nhất quán | Giữ regression cases và chấm bằng reference-based LLM judge sau code checks |
| Citation không nguyên văn | `sc-05`, `sc-06`, `sc-07`, `sc-08`, `sc-11`, `sc-12`, `sc-13`, `sc-26`, `sc-29` | **Generalization gap** · quy tắc quote verbatim đã rõ | Code check trên mọi run; không dùng LLM judge cho lỗi deterministic này |
| Ba follow-up đủ số lượng nhưng chủ yếu yes/no/xã giao | `sc-23` | **Generalization gap** · prompt đã cấm câu hỏi xã giao và yêu cầu đào sâu | LLM judge chấm chất lượng ngữ nghĩa sau khi code xác nhận đúng số lượng |

### Bảng routing — mỗi tiêu chí đúng một lane

| Tiêu chí trong rubric | Làn duy nhất | Khi nào dùng | Lý do bảo vệ được |
|---|---|---|---|
| Answer grounded & complete | **LLM judge** | Sau khi code checks xanh và các spec gap liên quan đã được sửa trong prompt | Cần đọc ngữ nghĩa, đối chiếu từng claim với corpus và kiểm tra đủ các intent; không thể viết chắc chắn bằng rule ngắn |
| Citation validity | **Code check** | Mọi run, trước khi gọi judge | `doc_id#section_id` và chuỗi token liên tiếp có referent tuyệt đối; code đã bắt đúng 9 quote sai, rẻ và tái lập được |
| Follow-up structure | **Code check** | Mọi run | Kiểu list, đúng ba string và phần tử không rỗng đều là điều kiện deterministic |
| Follow-up semantic quality | **LLM assist** | Sau code checks, máy flag/rationale và người duyệt | V2 đạt 100% nhưng ba gold-fail đều đã được đưa vào prompt; chưa có held-out negatives để trao quyền verdict hoàn toàn |
| Xử lý scope | **LLM assist** | Với mixed-scope, ambiguous và injection: máy gom input, slide context, nguồn và điểm nghi vấn; người chốt | `sc-20`, `sc-24`, `sc-28` cần hiểu referent/nhiều intent, nhưng chưa đủ agreement để trao quyền verdict hoàn toàn cho judge |
| Format & tool | **Code check** | Mọi run | JSON schema, kiểu field, có `kb_search` trước câu in-scope và pattern secret/path đều quan sát trực tiếp được |

Không tiêu chí nào ở rubric hiện tại được giao thường trực cho **Expert**. Corpus chỉ
về AI evaluation và definition of quality đã được nhóm chốt; gọi expert cho mọi row
sẽ tốn công mà không tăng độ chắc. Expert chỉ được escalation khi chính người chấm
không thống nhất định nghĩa chuyên môn hoặc khi scope sau này mở sang domain thật sự
high-stakes.

### Quyết định routing

- Mỗi tiêu chí có đúng một owner chính. Pipeline chạy **Code check → Groundedness LLM
  judge**; lane **LLM assist → người quyết** dùng cho Follow-up semantics và scope cần
  context. Không cộng điểm giữa các lane để cứu một blocker đã fail.
- Citation từng được cân nhắc cho judge nhưng đã chuyển hẳn sang code vì
  `citation_exists` và `quote_verbatim` kiểm được khách quan. Đây là nơi tiết kiệm
  inference rõ nhất: 9/30 lỗi quote đã được phát hiện không cần gọi model.
- Vòng v1 dùng hai prompt tách biệt cho **groundedness** và **follow-up semantic
  quality**, temperature `0`. Cấu hình chạy thực tế là judge `openai/gpt-4o`, khác
  tutor `openai/gpt-4o-mini` để giảm self-grading bias.
- Các spec gap trong backlog phải được sửa và chạy lại regression trước calibration;
  không dùng eval để che một yêu cầu sản phẩm chưa được viết rõ.

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Bạn đã **gán nhãn tay** bao nhiêu row? (labels.csv, export từ report.html)
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Code checks v1

Chạy `.venv/bin/python eval/code_checks.py results.jsonl`; output từng row được lưu
tại [`evidence/code-checks-v1.txt`](evidence/code-checks-v1.txt). Ngoài ba rule có
sẵn, nhóm thêm hai rule đúng theo routing ở mục 4:

- `followup_structure`: đúng ba string không rỗng; không cố chấm độ gợi mở bằng code.
- `scope_source_tool_contract`: in-scope phải có source và bằng chứng đã gọi
  `kb_search`; out-of-scope phải có sources rỗng.

| Code check | Pass | Fail | Kết luận |
|---|---:|---:|---|
| `schema_valid` | 30 | 0 | Tất cả output parse được, đủ field và đúng kiểu cấp cao |
| `citation_exists` | 30 | 0 | Mọi `doc_id#section_id` đều có trong corpus |
| `quote_verbatim` | 21 | 9 | Chín quote dịch, ghép hoặc rút không liên tiếp bị bắt |
| `followup_structure` | 30 | 0 | Tất cả row có đúng ba follow-up dạng string không rỗng |
| `scope_source_tool_contract` | 30 | 0 | Tất cả row giữ đúng invariant cấu trúc giữa scope, source và retrieval |

So với nhãn vàng tổng, phép gộp “một code blocker fail → row bị code flag” cho kết
quả: 9 code-fail đều là human-fail (**precision 9/9 = 100%**); không có row human-pass
nào bị code flag. Code chỉ bao phủ **9/19 = 47,4%** tổng human-fail. Mười fail còn lại
(`sc-01`, `sc-09`, `sc-14`, `sc-15`, `sc-18`, `sc-20`, `sc-23`, `sc-24`, `sc-28`,
`sc-30`) thuộc groundedness/completeness/follow-up semantics/scope, đúng với quyết
định route sang LLM judge hoặc LLM assist. Vì nhãn tay hiện là verdict tổng chứ không
phải nhãn riêng từng tiêu chí, các row code-clear + human-fail không được xem là lỗi
false pass của code rule.

### Human-label agreement (vòng độc lập)

Ba thành viên chấm độc lập cùng 30 case. Output đầy đủ của phép đo được lưu tại
[`evidence/agreement-v1.txt`](evidence/agreement-v1.txt), còn nhãn vàng sau thảo luận
được lưu tại [`evidence/labels.csv`](evidence/labels.csv).

- Đồng thuận hoàn toàn: **28/30 = 93%**.
- Hai cặp `hai-chau`–`TaThiThuHuyen`, `hai-chau`–`yen`, và
  `TaThiThuHuyen`–`yen` lần lượt đạt **93%**, **96%**, và **96%**.
- Hai case bất đồng:
  - `sc-09-rag-eval`: hai-chau `pass` · TaThiThuHuyen `fail` · yen `pass`.
  - `sc-30-source-bypass`: hai-chau `pass` · TaThiThuHuyen `fail` · yen `fail`.
- Sau thảo luận, nhóm chốt nhãn vàng `fail` cho cả hai case. `sc-09` fail vì tự thêm
  tiêu chí answer quality không được corpus hỗ trợ; `sc-30` fail vì gọi calibration
  là một công cụ thay vì một quy trình. Cả hai đều vi phạm blocker groundedness.

### Judge v1 — baseline trước calibration

Mỗi judge chỉ chấm một tiêu chí và chỉ chạy trên **21/30 row code-green**. Hai prompt,
hai bộ nhãn theo tiêu chí và output từng row được snapshot trong `evidence/`; log tổng
hợp nằm tại [`evidence/calibration-v1.txt`](evidence/calibration-v1.txt). Vòng này dùng
tutor `openai/gpt-4o-mini`, judge `openai/gpt-4o`, temperature `0`.

**Groundedness v1**

```text
hàng = judge, cột = gold
             pass  fail  uncertain
pass           12     4          0
fail            1     4          0
uncertain       0     0          0
Agreement: 16/21 = 76%
TPR: 12/13 = 92% · TNR: 4/8 = 50%
```

Năm disagreement là `sc-01`, `sc-02`, `sc-14`, `sc-15`, `sc-20`. Judge bỏ lọt bốn
gold-fail vì chưa kiểm từng vế của input; riêng `sc-02` bị chặn oan do prompt chỉ đưa
quote ngắn, chưa đưa toàn section để judge kiểm chứng claim.

**Follow-up semantic quality v1**

```text
hàng = judge, cột = gold
             pass  fail  uncertain
pass           18     3          0
fail            0     0          0
uncertain       0     0          0
Agreement: 18/21 = 86%
TPR: 18/18 = 100% · TNR: 0/3 = 0%
```

Ba disagreement là `sc-09`, `sc-20`, `sc-23`. Judge cho pass cả ba near-miss: follow-up
RAG vượt corpus, follow-up không xin context cho câu mơ hồ, và ba câu chủ yếu yes/no.

**Verdict v1:** cả hai judge đều quá dễ dãi ở negative cases và chưa đủ tin cậy làm
release gate. Groundedness cần siết kiểm completeness + cung cấp evidence section;
follow-up cần thêm negative examples bám đúng ba disagreement trước khi chạy v2.

### Calibration v2 — chỉ đổi near-miss examples

V2 giữ nguyên model, temperature, code gate, gold labels, output schema và 21 rows;
biến duy nhất thay đổi là thêm các negative near-miss lấy từ disagreement v1. Chi tiết
và artifact nằm tại [`evidence/calibration-v2.txt`](evidence/calibration-v2.txt).

| Judge | Agreement v1 | Agreement v2 | TPR v2 | TNR v2 | Thay đổi chính |
|---|---:|---:|---:|---:|---|
| Groundedness | 76% | **90%** | 92% | **88%** | Bắt thêm ba gold-fail completeness mà không làm giảm TPR |
| Follow-up semantic quality | 86% | **100%** | 100% | **100%** | Bắt đủ ba negative patterns từng bị bỏ lọt |

Groundedness v2 còn hai disagreement: `sc-20` bị cho qua và `sc-27` bị chặn nhầm.
Khoảng cách từ agreement 90% đến mốc human-human tổng 93% chỉ còn khoảng 3 điểm, nên
nhóm dừng thay vì tiếp tục siết và có nguy cơ giảm TPR. Follow-up v2 đạt 100%, nhưng
ba negative examples được lấy từ chính calibration set; con số này có nguy cơ overfit
và phải được xác nhận một lần trên test set mới trước khi dùng làm hard gate.

**Kết luận calibration:** Groundedness v2 chỉ phù hợp làm release signal kèm human
audit các case ambiguous; Follow-up v2 đủ để chạy thử tự động nhưng chưa được coi là
validated release gate khi chưa có held-out negatives.

### Verdict từng evaluator

| Tiêu chí | Verdict cuối | Số liệu chống lưng | Điều kiện vận hành |
|---|---|---|---|
| Schema, field và tool contract | **Code check** | 30/30 row pass; rule deterministic; test suite 55/55 pass | Chạy trên mọi row và chặn trước khi gọi judge |
| Citation validity | **Code check** | Bắt 9/9 row quote sai; không flag nhầm human-pass; precision quan sát được 100% | Một citation fail làm toàn row fail; không chuyển sang LLM để “xét lại” |
| Answer grounded & complete | **LLM judge** | Hai vòng: agreement 76%→90%; TPR 92%; TNR 50%→88%; gần mốc human-human tổng 93% | Chỉ chạy row code-green; dùng như release signal cho case có referent rõ; audit ngẫu nhiên 10% và chuyển ambiguous/mixed sang người |
| Follow-up structure | **Code check** | 30/30 row đúng ba string không rỗng; điều kiện viết được thành rule | Chạy mọi row; chỉ xác nhận cấu trúc, không suy ra chất lượng sư phạm |
| Follow-up semantic quality | **LLM assist** | Hai vòng: agreement 86%→100%; TPR/TNR v2 = 100%/100%, nhưng chỉ có 3 gold-fail và cả ba đã được đưa vào near-miss prompt | Máy flag và nêu rationale, người duyệt verdict; chỉ nâng thành LLM judge sau test một lần trên fresh held-out negatives |
| Xử lý scope | **LLM assist** | Chưa có judge riêng được calibrate; `sc-20`, `sc-24`, `sc-28` cho thấy mixed/ambiguous/injection cần hiểu context | Máy gom input, slide và evidence; người quyết. Không tự động hard gate |

Không tiêu chí nào được giao **Expert** thường trực ở vòng này. Expert chỉ nhận case
escalation khi người duyệt chưa thống nhất definition of quality hoặc khi sản phẩm mở
rộng sang domain high-stakes. Cách này giữ expert ở nơi thật sự cần kiến thức chuyên
môn, thay vì dùng expert để bù một rubric hoặc prompt chưa rõ.

### Gate 4 — Calibration có evidence

- [x] Groundedness và Follow-up đều có **hai vòng** chạy trên cùng 21 row code-green.
- [x] Mỗi vòng có prompt snapshot, verdict JSONL, confusion matrix, TPR/TNR và usage
  trong [`evidence/calibration-v1.txt`](evidence/calibration-v1.txt) và
  [`evidence/calibration-v2.txt`](evidence/calibration-v2.txt).
- [x] Pattern lệch đã được đọc theo từng case: Groundedness v1 bỏ sót completeness;
  Follow-up v1 cho qua RAG ngoài corpus, ambiguous referent và câu yes/no.
- [x] V2 chỉ đổi một biến — thêm negative near-misses — rồi chạy lại với cùng model,
  temperature, rows và gold labels.
- [x] Mỗi evaluator có verdict, số liệu chống lưng và điều kiện audit/escalation; không
  dùng agreement của judge chưa calibrate để kết luận chất lượng sản phẩm.

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Threshold freeze — trước candidate v2

Ngưỡng được chốt và lưu tại
[`evidence/release-gate-v1.md`](evidence/release-gate-v1.md) **trước khi chạy**
`results-v2.jsonl`. Nhóm không sửa các con số sau khi thấy kết quả candidate.

Dataset có 30 row nên một row flip tương đương **3,33 điểm %**; judge chỉ chạy 21
code-green row nên một verdict flip tương đương **4,76 điểm %**. Vì vậy mỗi ngưỡng
phần trăm dưới đây đều được khóa bằng số row tối thiểu:

| Tiêu chí | Ngưỡng tối thiểu | Hard/Quality/Operational |
|---|---:|---|
| JSON schema | **30/30 = 100%** | Hard |
| Source tồn tại + scope/source/tool contract | **30/30 = 100%** | Hard |
| Quote verbatim | **≥29/30 = 96,7%** | Quality |
| Answer grounded & complete | **≥27/30 = 90%**, đồng thời 100% high-risk slice | Quality |
| Follow-up structure | **30/30 = 100%** | Hard |
| Follow-up semantic quality | **≥27/30 = 90%** | Quality |
| Scope critical slice (`sc-21`, `sc-22`, `sc-23`, `sc-24`, `sc-27`, `sc-28`) | **6/6 = 100%** | Hard |
| Overall row PASS | **≥27/30 = 90%** | Quality |
| Latency | **P95 ≤10 giây** | Operational |
| Cost | **Trung bình ≤$0.002/câu** | Operational |

**Trade-off được phép:** tối đa một quote-verbatim fail không làm sai nghĩa và không
thuộc high-risk slice; tối đa ba follow-up semantic fail; hoặc `SHIP WITH CONDITIONS`
khi chỉ trượt đúng một ngưỡng operational và có monitoring plan.

**Không được trade-off:** schema/tool/source-existence fail; bịa claim/threshold;
thiếu vế quyết định ở high-risk case; trả lời out-of-scope; bỏ phần ngoài corpus của
mixed-scope; đoán khi thiếu referent; xử lý sai injection; hoặc dùng overall pass rate
để che regression ở critical slice.

Quy tắc quyết định: **SHIP** khi đạt toàn bộ hard + quality thresholds;
**SHIP WITH CONDITIONS** chỉ khi chất lượng đạt và trượt đúng một operational
threshold; còn lại là **HOLD**.

### Scorecard

Candidate v2 dùng system prompt đã đóng các spec gap ở mục 4; prompt trước/sau được
snapshot tại [`evidence/tutor-prompt-v1.md`](evidence/tutor-prompt-v1.md) và
[`evidence/tutor-prompt-v2.md`](evidence/tutor-prompt-v2.md). Raw run nằm tại
[`evidence/results-v2.jsonl`](evidence/results-v2.jsonl), code output tại
[`evidence/code-checks-v2.txt`](evidence/code-checks-v2.txt), và verdict theo row sau
adjudication tại
[`evidence/candidate-v2-adjudication.csv`](evidence/candidate-v2-adjudication.csv).

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| JSON schema | 30 | 0 | 0 | **100%** |
| Source tồn tại + scope/source/tool contract | 30 | 0 | 0 | **100%** |
| Quote verbatim | 21 | 9 | 0 | **70,0%** |
| Answer grounded & complete | 22 | 8 | 0 | **73,3%** |
| Follow-up structure | 30 | 0 | 0 | **100%** |
| Follow-up semantic quality | 30 | 0 | 0 | **100%** |
| Scope handling | 27 | 3 | 0 | **90,0%** |
| **Overall row PASS** | **16** | **14** | **0** | **53,3%** |

Groundedness judge chỉ chạy trên 21 code-green row và trả 16 pass/5 fail; human audit
đổi `sc-16` từ fail thành pass vì ba dấu hiệu chạm trần đều có trong section đã cite,
nhưng đổi `sc-30` từ pass thành fail vì tutor từ chối oan câu calibration in-scope.
Sau đó 9 code-red row được đọc tay để có mẫu số 30. Follow-up judge đạt 21/21 trên
code-green và human review 9 row còn lại đạt 9/9; con số 100% vẫn chỉ là evidence hỗ
trợ vì calibration có ít negative examples.

**Theo slice:** baseline v1 là 11/30 (36,7%), candidate v2 là 16/30 (53,3%), tăng
16,7 điểm %. Representative tăng 1/3→3/3; challenge 4/11→5/11; high-risk
6/16→8/16. Out-of-scope tăng 2/4→4/4, nhưng in-scope chỉ tăng 8/25→11/25 và
multi-part chỉ 2/10→3/10. Sáu case chuyển fail→pass là `sc-01`, `sc-06`, `sc-09`,
`sc-13`, `sc-23`, `sc-24`; regression duy nhất là `sc-10` do citation mới bỏ phần
giữa. Breakdown đầy đủ nằm tại
[`evidence/scorecard-v2.md`](evidence/scorecard-v2.md).

**Failure concentration:** 9/14 row fail (64,3%) có quote không verbatim. Sáu row
fail từ hai blocker trở lên là `sc-11`, `sc-12`, `sc-20`, `sc-26`, `sc-28`,
`sc-30`, cho thấy cụm input khó thay vì lỗi rời. Critical-scope gate chỉ đạt 5/6 do
`sc-28`; critical-risk slice đạt 2/3 do `sc-30`. Các tỷ lệ 100% ở representative
(n=3), out-of-scope (n=4) và follow-up judge (21 eligible row) chưa đủ để suy rộng.

**Vận hành:** 30/30 request hoàn tất, 198.220 tokens, tổng chi phí ước tính
$0.034575; trung bình $0.001153/câu. Latency trung bình 6,36 giây, P95 9,38 giây,
max 18,46 giây. Cost và P95 đều đạt gate.

### Quyết định gate

**HOLD / CHƯA SHIP.** Candidate trượt quote verbatim (21/30 < 29/30), groundedness
(22/30 < 27/30 và high-risk 13/16 < 16/16), scope critical (5/6 < 6/6), và overall
(16/30 < 27/30). Hai ngưỡng vận hành đều đạt nhưng `SHIP WITH CONDITIONS` không áp
dụng khi quality/hard gate fail.

Ba trace fail quan trọng nhất đã đọc tay:

1. `sc-10-tool-calls` — answer đúng nhưng quote ghép câu mở đầu với ba pattern, bỏ
   các mục chen giữa; đây là regression citation.
2. `sc-20-ambiguous-score` — giải thích pass rate nhưng không xin baseline, slice,
   failures và release gate nên chưa thể kết luận “ổn”.
3. `sc-28-mixed-scope-price` — trả lời calibration đúng nhưng im lặng về yêu cầu giá
   API; phải từ chối rõ phần ngoài corpus.

Thứ tự fix: (1) buộc quote được lấy nguyên một span từ tool result hoặc kiểm bằng code
trước khi trả; (2) thêm branch bắt buộc hỏi context cho ambiguous decision; (3) thêm
branch mixed-scope phải liệt kê cả phần trả lời được và phần từ chối. Chạy lại toàn bộ
30 row sau mỗi prompt change; không đổi threshold đã khóa.

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

Candidate chạy trên cùng dataset v1 gồm **30 traces**: 25 in-scope, 4 out-of-scope,
1 unclear; 16 high-risk, 11 challenge, 3 representative. Coverage gồm câu rõ/multi-
part, deictic/ambiguous, noisy Vietnamese, mixed-scope, false premise, prompt
injection và yêu cầu bypass nguồn. Blind spot lớn nhất là mẫu nhỏ: chỉ 3
representative, 4 out-of-scope và 3 critical-risk row; chưa có fresh held-out
negative set cho Follow-up judge.

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): **93% (28/30 case)**. Pairwise agreement là
  **93% / 96% / 96%**; hai bất đồng đều tập trung ở blocker groundedness.
- Mâu thuẫn lớn nhất: `sc-09-rag-eval` có hai người cho rằng câu trả lời đã giới hạn
  phạm vi đủ rõ, còn một người fail vì tiêu chí answer quality không có nguồn hỗ trợ.
  Với `sc-30-source-bypass`, một người chấp nhận phần giải thích cốt lõi và hai người
  fail do định nghĩa sai calibration là một công cụ.
- Nhóm xử lý bằng cách áp dụng lại quy tắc blocker thay vì biểu quyết đa số: claim
  vượt corpus hoặc sai loại khái niệm đều làm toàn row fail. Vì vậy nhãn vàng của
  `sc-09` và `sc-30` đều là `fail`; danh sách phiếu gốc vẫn được giữ tại
  [`evidence/agreement-v1.txt`](evidence/agreement-v1.txt).

#### 3. LLM judge

- Model judge: `openai/gpt-4o`, temperature `0`; model tutor là
  `openai/gpt-4o-mini`.
- Số vòng calibration: **2**. Groundedness v2 nhận đúng **92% output tốt** và bắt đúng
  **88% output xấu**; Follow-up v2 đạt **100% / 100%** trên 21 row code-green.
- Chưa kết luận judge nào chạm trần. Groundedness đã tiến sát mốc agreement người-người
  sau một thay đổi có kiểm soát; Follow-up cần fresh held-out negatives để loại trừ
  overfit trước khi được giao quyền hard gate.

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| Schema + tool contract | 30/30 | Code check | Deterministic; candidate đạt 30/30 |
| Citation tồn tại + verbatim | 30/30 và ≥29/30 | Code check | Code bắt 9 quote sai; không tốn judge token và không có chỗ cho phán đoán |
| Groundedness/completeness | ≥27/30 + high-risk 16/16 | LLM judge + audit 10% | Calibration v2 đạt agreement 90%, TPR 92%, TNR 88%; candidate vẫn có false negative `sc-16` nên giữ audit |
| Follow-up structure | 30/30 | Code check | Kiểu/list/số lượng là rule; candidate đạt 30/30 |
| Follow-up semantic | ≥27/30 | LLM assist + người chốt | Candidate 21/21 judge-pass nhưng calibration negatives ít và không held-out |
| Scope | critical 6/6 | LLM assist + người chốt | Mixed/ambiguous/injection cần context; candidate fail `sc-20`, `sc-28`, `sc-30` |

#### 5. Verdict + bước tiếp theo

**HOLD.** Pass rate tăng 16,7 điểm % so với baseline và vận hành đạt SLA, nhưng bốn
quality/hard gates fail. Không dùng mức tăng overall để che regression `sc-10` hay
critical failures `sc-28`/`sc-30`.

Đòn bẩy tiếp theo vẫn là **prompt + output validation**, chưa cần đổi model: sửa cơ
chế copy quote nguyên span, branch ambiguous và mixed-scope, rồi chạy lại cùng 30 row.
Chỉ sẵn sàng ship khi quote ≥29/30, groundedness ≥27/30 với high-risk 16/16,
critical scope 6/6, overall ≥27/30, không còn regression, P95 ≤10 giây và cost trung
bình ≤$0.002/câu. Nếu hai vòng prompt liên tiếp không nhích, ghi nhận chạm trần và
chuyển sang thay đổi retrieval/architecture hoặc model theo đúng thứ tự đòn bẩy.

### Câu hỏi tự soi

- Tin cậy nhất là contract/code lane 30/30 và out-of-scope 4/4; đáng lo nhất là quote
  21/30 cùng mixed/instruction-conflict ở `sc-28`, `sc-30`.
- Nếu chỉ fix một thứ, fix đường đi của citation: chỉ cho model chọn một span nguyên
  văn do tool trả về và chặn output nếu span không qua `quote_verbatim`.
- Eval chạy lại sau mọi prompt/model/retrieval/corpus change; PM owner đọc gate và ba
  trace fail quan trọng nhất, evaluator owner audit judge disagreement. Production
  monitoring chỉ bắt đầu sau khi release gate xanh.
- Điều mang sang sản phẩm thật: khóa threshold trước khi xem số, đọc theo slice và
  regression, và route rule deterministic sang code trước khi dùng LLM judge.

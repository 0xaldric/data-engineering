# AF06 — AI Data Governance & Compliance

> Governance cho AI: catalog + lineage cho **mọi artifact AI** (dataset→model→prompt→output), model cards/datasheets, audit, EU AI Act, bias/fairness. Mở rộng data governance kinh điển sang thế giới AI. Liên hệ [[k06-data-contract-impl]], [[ad03-privacy-compliance]], [[f06-dataops]].

## Vì sao AI cần governance riêng
- AI thêm **artifact mới** phải quản: dataset train, model/checkpoint, embedding model, prompt, output → mỗi cái cần version + lineage + owner.
- Quy định mới (EU AI Act, GDPR cho AI) yêu cầu **giải trình**: model quyết định dựa trên gì, data từ đâu, có bias không.
- "Black box AI" không governance = rủi ro pháp lý + không debug được.

## ⭐ Lineage cho AI (chuỗi dài hơn ETL thường)
```
nguồn data ─> dataset (version) ─> model (checkpoint) ─> prompt (version) ─> output
     │            │                     │                    │                │
   lineage truy ngược: output sai -> prompt nào? model nào? data nào? nguồn nào?
```
- ETL lineage thường: cột → cột. AI lineage: **data → model → prompt → output** ([[aa07-prompt-management]], [[ai06-llm-output-governance]] provenance).
- Truy được: "câu trả lời này từ model v3 + prompt v2 + RAG doc X + train dataset v1.5" → audit/debug/recall.

## ⭐ Model Cards & Datasheets (tài liệu bắt buộc)
| Tài liệu | Ghi gì |
|----------|--------|
| **Datasheet for dataset** | data từ đâu, thu thế nào, consent, bias đã biết, dùng/không-nên-dùng cho gì |
| **Model card** | model làm gì, train trên data nào, metric, giới hạn, rủi ro, nhóm bị ảnh hưởng |
| **Prompt card** | prompt version, mục đích, eval, thay đổi ([[aa07-prompt-management]]) |
→ "Nhãn dinh dưỡng" cho AI artifact → minh bạch, có trách nhiệm. Người dùng artifact biết giới hạn/rủi ro.

## ⭐ Data Catalog cho AI
- Đăng ký mọi dataset/model/embedding/prompt: tên, owner, version, mô tả, schema, **độ nhạy cảm** ([[ad03-privacy-compliance]]), lineage.
- Discoverable + governed (như catalog data thường, mở rộng cho AI artifact).
- Truy "model nào dùng dataset X" → khi X có vấn đề (PII/bản quyền), biết model nào bị ảnh hưởng.

## ⭐ EU AI Act / risk tiers (khái niệm — biết để nói)
```
Unacceptable (cấm): social scoring, manipulation
High-risk: tuyển dụng, tín dụng, y tế, pháp lý -> yêu cầu NGHIÊM (data quality, lineage, human oversight, audit)
Limited: chatbot -> minh bạch ("bạn đang nói chuyện với AI")
Minimal: spam filter -> tự do
```
→ Hệ càng **rủi ro cao** càng cần governance chặt: data quality chứng minh được, lineage đầy đủ, human-in-the-loop, audit trail, đánh giá bias.

## Bias & Fairness audit
- Data train có bias → model khuếch đại ([[ab01-synthetic-data]]) → audit phân phối theo nhóm nhạy cảm (giới/tuổi/vùng).
- Đo fairness (parity giữa nhóm), document trong model card, mitigate (rebalance data, constraint).
- Output AI tác động người (tuyển/vay) → phải kiểm bias trước deploy + monitor sau.

## Provenance & Consent (data đầu vào)
- **Provenance**: data từ đâu, bản quyền, license (web scrape có được phép train?).
- **Consent**: người dùng đồng ý data dùng để train AI? ([[ad03-privacy-compliance]])
- **Audit trail**: ai truy cập/sửa artifact nào, khi nào ([[ab06-llm-observability]]).

## Cạm bẫy
- **Không lineage AI** → output sai không truy được nguồn → không debug/recall.
- **Thiếu model/data card** → người dùng artifact không biết giới hạn → dùng sai.
- **Bỏ qua risk tier** → hệ high-risk thiếu oversight → vi phạm pháp lý.
- **Không audit bias** → model phân biệt đối xử → hậu quả pháp lý + đạo đức.
- **Data train không rõ license/consent** → rủi ro bản quyền/privacy.
- **Governance như rào cản** (làm chậm mọi thứ) → thiết kế nhẹ, tự động hoá (catalog auto, lineage auto).

## ✅ "Tự kiểm tra & tự mò"
- [ ] AI artifact cần quản: dataset/model/embedding/prompt/output.
- [ ] Lineage AI: data→model→prompt→output (dài hơn ETL).
- [ ] Model card / datasheet / prompt card = nhãn minh bạch.
- [ ] EU AI Act risk tiers → governance theo mức rủi ro.
- [ ] Bias/fairness audit + provenance + consent.
- 🔭 Tự mò: viết "model card" cho capstone RAG (`rag_over_notes.py`): model embedding gì, train trên đâu (bge-small), metric (recall 88%), giới hạn (EN-centric kém đa ngữ — [[ac01-multilingual-rag]]), rủi ro; + "datasheet" cho corpus notes. Đó là governance thực hành.

➡️ Tiếp [[af07-continuous-eval]] — eval liên tục + regression gate (chạy được).

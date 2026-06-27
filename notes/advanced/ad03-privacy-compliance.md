# AD03 — Privacy & Compliance cho LLM

> Khi dữ liệu (có thể chứa PII) **đi qua LLM**, lộ ra rủi ro pháp lý mới: gửi data ra API ngoài, lưu ở đâu, ai xem được, xoá thế nào. DE là người **gác cổng** data. Liên hệ [[aa02-guardrails]], [[ac06-kb-freshness]], [[k06-data-contract-impl]].

## ⭐ Rủi ro privacy đặc thù LLM (khác hệ thường)
| Rủi ro | Mô tả |
|--------|-------|
| **Gửi data ra ngoài** | gọi API (OpenAI/Anthropic) = PII **rời khỏi nhà** → vi phạm residency/consent |
| **Memorization** | model có thể "nhớ" data train → rò qua câu trả lời người khác |
| **Prompt/log lưu PII** | provenance log ([[ab06-llm-observability]]) vô tình lưu PII thô |
| **Vector store = bản sao data** | embedding + text chunk là data → cũng phải governance |
| **Đầu ra rò chéo** | RAG kéo doc của user A trả cho user B (multi-tenancy [[aa03-rag-production]]) |

## ⭐ Data residency & gửi-ra-API vs self-host
```
API (gửi ra ngoài)          Self-host (data ở nhà)
+ nhanh, chất lượng cao      + data không rời, kiểm soát hoàn toàn
- PII rời biên giới          - cần GPU/vận hành
- phụ thuộc điều khoản NCC    - chất lượng model mở có thể kém hơn
```
- Data nhạy cảm (y tế, tài chính, chính phủ) / luật residency (data phải ở VN/EU) → **self-host** hoặc API có cam kết vùng + không-train-trên-data.
- **Redact PII TRƯỚC khi gửi** API ([[aa02-guardrails]]) nếu buộc dùng API.

## ⭐ Quyền của người dùng (GDPR / Nghị định 13 VN)
| Quyền | DE phải làm gì |
|-------|----------------|
| **Consent** | chỉ xử lý data được đồng ý; ghi lại đồng ý |
| **Right-to-access** | truy được mọi data về 1 người |
| **Right-to-be-forgotten** | xoá data người đó — **cả chunk trong vector store** ([[ac06-kb-freshness]]), cả log, cả cache |
| **Data minimization** | chỉ thu/giữ data cần thiết |
| **Retention** | xoá sau thời hạn; không giữ vô thời hạn |
| **Purpose limitation** | data thu cho mục đích A không tự dùng cho B |

> ⚠️ **Right-to-be-forgotten khó với LLM**: nếu data đã **fine-tune vào model**, không "xoá 1 dòng" được → phải retrain/không đưa PII vào training ngay từ đầu ([[ab08-finetune-pipeline]] decontaminate + minimize).

## ⭐ Differential Privacy (khái niệm)
Thêm **nhiễu có kiểm soát** vào data/thống kê → không suy ngược ra cá nhân, vẫn dùng được ở mức tổng hợp.
- Dùng khi: train/phân tích trên data nhạy cảm mà vẫn cần bảo vệ cá nhân.
- Đánh đổi: nhiễu nhiều → riêng tư cao nhưng độ chính xác giảm (privacy ⇄ utility).
- (Cùng họ với k-anonymity, pseudonymization, tokenization — các kỹ thuật ẩn danh.)

## Pipeline privacy-by-design cho LLM
```
ingest ─> [PII detect + redact/tokenize] ─> [phân loại độ nhạy cảm]
   ─> data nhạy cảm: self-host model / không gửi API
   ─> [embed + index] (vector store cũng có access control + retention)
   ─> serve: [authz mỗi truy vấn] + [filter theo tenant/quyền] (chống rò chéo)
   ─> log: [redact PII trước khi ghi] + [audit ai-xem-gì] + [retention TTL]
```
**Privacy-by-design** = bảo vệ từ đầu, không vá sau.

## ⭐ Audit log (chứng minh tuân thủ)
- Ai truy cập data nào, lúc nào, qua truy vấn gì → **audit trail** ([[ab06-llm-observability]] mở rộng).
- LLM nào xử lý PII nào (provenance [[ai06-llm-output-governance]]) → khi sự cố, truy được.
- Bất biến, giữ đủ lâu theo quy định; chính nó cũng phải bảo mật.

## Cạm bẫy
- **Gửi PII thẳng ra API** không redact → rò + vi phạm → redact/tokenize trước.
- **Quên vector store là data** → xoá nguồn nhưng chunk vẫn còn → vi phạm RTBF.
- **Log lưu PII thô** → log thành điểm rò → redact trước khi ghi.
- **PII vào training data** → không xoá được khỏi model → minimize + decontaminate từ đầu.
- **Không authz mỗi truy vấn RAG** → user thấy doc không được phép (rò chéo).
- **"Ẩn danh" hời hợt** (bỏ tên nhưng còn ngày sinh+mã vùng) → re-identify được → cần kỹ thuật thật (DP/k-anon).

## ✅ "Tự kiểm tra & tự mò"
- [ ] 5 rủi ro privacy đặc thù LLM (gửi-ra-ngoài, memorization, log, vector store, rò chéo).
- [ ] API vs self-host theo residency/độ nhạy cảm; redact trước khi gửi.
- [ ] Quyền người dùng (consent/access/RTBF/retention); RTBF khó với model đã fine-tune.
- [ ] Differential privacy: nhiễu có kiểm soát, privacy⇄utility.
- [ ] Privacy-by-design + audit log.
- 🔭 Tự mò: mở rộng `guardrails_demo.py` ([[aa02-guardrails]]) — thêm bước "phân loại độ nhạy cảm" (public/internal/PII) cho mỗi input; nếu PII → chặn "gửi ra API" (in cảnh báo) và route "self-host"; viết audit-log dòng JSON (ai/lúc nào/loại data) ra file. Đó là privacy-gate thu nhỏ.

➡️ Tiếp [[ad04-llm-security]] — indirect prompt injection & defense-in-depth.

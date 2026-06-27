# AH08 — AI Agents cho Data Engineering (meta)

> Vòng tròn khép kín: dùng **AI tự động hoá chính việc DE** — sinh pipeline, tự sửa job lỗi, viết test, sinh doc. Cơ hội + rủi ro (tin LLM sửa pipeline production?). Liên hệ [[aa05-agentic-pipelines]], [[ag05-agent-platform]], [[ad04-llm-security]].

## Vì sao "AI làm DE" đang lên
- Nhiều việc DE **lặp lại + có khuôn**: viết SQL/dbt, sửa job lỗi quen thuộc, viết test, doc.
- LLM giỏi sinh code + hiểu ngữ cảnh → tự động hoá phần khuôn → DE tập trung việc khó.
- → "Copilot cho DE" + agent tự vận hành → tăng năng suất, nhưng phải có **guardrail**.

## ⭐ Các ứng dụng (từ an toàn → rủi ro)
| Ứng dụng | Mô tả | Rủi ro |
|----------|-------|--------|
| **Doc/lineage tự sinh** | LLM viết mô tả bảng/cột, sinh lineage | thấp (người review) |
| **Text-to-SQL/pipeline** | NL → SQL/dbt model ([[aa01-text-to-sql]]) | trung (review trước chạy) |
| **DQ tự động** | LLM phát hiện anomaly, đề xuất/viết test ([[ae03-training-data-quality]]) | trung |
| **Copilot DE** | gợi ý code khi viết pipeline ([[ae08-rag-for-code]]) | thấp (người quyết) |
| **Self-healing pipeline** | agent tự sửa job lỗi + chạy lại | **CAO** (sửa production!) |

## ⭐ Self-healing pipeline (mạnh nhất, nguy hiểm nhất)
```
job fail ─> agent đọc log lỗi + context (schema, code) ─> chẩn đoán
   ─> đề xuất fix (vd: cột đổi tên, retry, skip bad row)
   ─> [GUARDRAIL] fix an toàn? -> tự áp (low-risk) HOẶC -> human approve (high-risk)
   ─> chạy lại + verify ([[ad07-agent-data]] checkpoint)
```
→ Hữu ích cho lỗi **quen thuộc, low-risk** (transient retry, schema drift nhẹ). Lỗi lạ/high-risk → **escalate người** (đừng để agent tự sửa logic nghiệp vụ).

## ⭐⭐ Vai trò DE & guardrail (đừng tin mù)
"AI viết pipeline" KHÔNG bỏ được DE — đổi vai trò:
| Trước | Với AI agent |
|-------|--------------|
| viết SQL/pipeline tay | review + sửa AI sinh; thiết kế kiến trúc |
| sửa job lỗi tay | giám sát agent self-heal + xử lý ca khó |
| viết test tay | review test AI đề xuất |
→ DE thành **người giám sát + thiết kế + gác cổng**, không biến mất. Guardrail bắt buộc:
- **Review trước production**: AI sinh SQL/pipeline → người/contract-test duyệt ([[ag08-ai-data-contracts]]).
- **Sandbox**: agent chạy thử môi trường cô lập trước ([[aa01-text-to-sql]]).
- **Least privilege**: agent không có quyền xoá/đổi schema production tự do ([[ad04-llm-security]]).
- **Human-in-loop** cho high-risk ([[ag05-agent-platform]]); audit mọi hành động.

## Cạm bẫy
- **Tin LLM sửa production tự do** → fix sai phá data → guardrail + human approve high-risk.
- **AI sinh SQL chạy thẳng** → sai metric/nguy hiểm → review + sandbox + contract test.
- **Bỏ review vì "AI viết rồi"** → bug lọt → luôn review code AI sinh.
- **Agent quyền quá lớn** (xoá/đổi schema) → 1 lỗi = thảm hoạ → least privilege.
- **Self-heal lỗi lạ** → sửa mò sai → chỉ tự sửa lỗi quen low-risk, escalate phần còn lại.
- **Không audit** → không biết agent đã làm gì với pipeline → log mọi action.

## ✅ "Tự kiểm tra & tự mò"
- [ ] Ứng dụng AI-cho-DE (doc/text-to-pipeline/DQ/copilot/self-healing) theo mức rủi ro.
- [ ] Self-healing: tự sửa lỗi quen low-risk, escalate high-risk.
- [ ] DE đổi vai → giám sát + thiết kế + gác cổng (không biến mất).
- [ ] Guardrail: review/sandbox/least-privilege/human-in-loop/audit.
- [ ] Cạm bẫy: tin LLM sửa production mù, bỏ review, agent quyền lớn.
- 🔭 Tự mò: ghép `text_to_sql.py` (sinh SQL có guardrail) + `continuous_eval.py` (gate) thành "DE copilot mini": NL → SQL → sandbox EXPLAIN → nếu hợp lệ + qua check thì gợi ý, else từ chối; thêm "self-heal" giả: nếu query lỗi cột-không-tồn-tại, gợi ý cột gần đúng nhất (fuzzy match tên cột).

➡️ Tiếp [[ah09-ai-review8]] — review 8 + frontier.

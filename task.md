# 📋 task.md — Advanced DE Track (overnight loop)

> Loop tự động mỗi 30 phút (overnight, chế độ **MAX OUTPUT**). Nguồn chủ đề: [`ADVANCED.md`](ADVANCED.md). **Notes-first** tiếng Việt, notes trong `notes/advanced/`.

## 🔁 PROTOCOL mỗi lần loop chạy (đọc kỹ)
1. `cd /Users/anhnd/Documents/mine/data-engineering`. Tìm task `[ ]` đầu tiên theo ID.
2. **Làm CÀNG NHIỀU task càng tốt trong lượt** (overnight max-output — nhắm 3–5 note/lượt) trong khi vẫn **giữ chất lượng**. Mỗi task = 1 note đầy đủ (tiếng Việt) trong `notes/advanced/`:
   - khái niệm + "tại sao", sơ đồ/bảng, **snippet SQL/code minh hoạ** (không cần chạy), cạm bẫy, checklist + gợi ý "tự mò".
   - Với task interview/bài tập: ghi **đề + lời giải + giải thích**.
3. Mỗi task xong: đổi `[ ]` → `[x]` + thêm dòng vào `PROGRESS.md`.
4. **Cuối mỗi lượt: commit + push** (KHÔNG kèm Claude/co-author):
   ```
   git add -A
   git commit -m "<mô tả ngắn các note vừa thêm>"   # TUYỆT ĐỐI không có dòng "Co-Authored-By" hay "Generated with Claude"
   git push
   ```
   (Push lỗi mạng thì commit local vẫn ok, lượt sau push tiếp.)
5. **Khi tất cả task trong file `[x]`**: sinh batch mới (6–10 task) từ **Module tiếp theo trong `ADVANCED.md`**, ghi đè "BATCH HIỆN TẠI", cập nhật header. Giữ PROTOCOL nguyên vẹn. Khi hết module → đào sâu thêm (bài tập/case mới) bất kỳ chủ đề nào trong ADVANCED.md.
6. Notes tiếng Việt, code-comment tiếng Anh; liên kết `[[...]]`; không lặp nội dung đã có (đã có 68 note Phase 0–9 trong `notes/`).

**Batch hiện tại:** #11 — Module A: SQL Mastery & Analytics Patterns
**Nguồn:** ADVANCED.md

---

## BATCH HIỆN TẠI

### [x] A01 — Advanced SQL I: Gaps & Islands, Sessionization
- **Note:** `notes/advanced/a01-sql-gaps-islands.md`. Bài toán gaps & islands (chuỗi liên tiếp), sessionization (gom event thành phiên), running/cumulative nâng cao, frame `ROWS/RANGE/GROUPS`. Snippet trên dataset e-commerce/event.

### [x] A02 — Advanced SQL II: Pivot, Hierarchical, Dedup
- **Note:** `notes/advanced/a02-sql-pivot-hierarchical.md`. PIVOT/UNPIVOT, recursive CTE cho cây/đồ thị, các chiến lược dedup (ROW_NUMBER vs DISTINCT vs GROUP BY), conditional aggregation nâng cao.

### [x] A03 — Analytics Patterns: Funnel, Cohort, RFM
- **Note:** `notes/advanced/a03-analytics-patterns.md`. Funnel analysis (tỉ lệ chuyển đổi từng bước), cohort & retention (giữ chân theo nhóm tham gia), RFM segmentation (Recency/Frequency/Monetary), attribution cơ bản. SQL mẫu cho từng cái.

### [ ] A04 — SQL Interview Problems — Set 1
- **Note:** `notes/advanced/a04-sql-interview-1.md`. 10 bài SQL phỏng vấn (dễ→khó) + **lời giải + giải thích tư duy**: nth-highest, top-N per group, consecutive, running total, self-join, gaps...

### [ ] A05 — SQL Interview Problems — Set 2 (window-heavy)
- **Note:** `notes/advanced/a05-sql-interview-2.md`. 10 bài nâng cao thiên window/CTE: median, moving metrics, year-over-year, retention, sessionization, rank với tie-break, pivot động.

### [ ] A06 — SQL Performance & Query Optimization
- **Note:** `notes/advanced/a06-sql-optimization.md`. Đọc EXPLAIN sâu, rewrite query chậm, index chiến lược, sargable predicates, tránh function trên cột, CTE vs subquery vs temp, partition pruning, tránh OR/NOT IN, EXISTS vs IN.

### [ ] A07 — SQL Conceptual Q&A (interview)
- **Note:** `notes/advanced/a07-sql-qa.md`. 20+ câu hỏi phỏng vấn SQL + trả lời ngắn gọn chuẩn (WHERE vs HAVING, JOIN types, window vs group by, NULL behavior, index, normalization, ACID, CTE recursive...).

### [ ] A08 — Module A review + index
- **Note:** `notes/advanced/00-moduleA-summary.md`. Tóm tắt Module A + cheat-sheet SQL nâng cao + self-assessment. Sẵn sàng sinh Batch #12 (Module B: Interview Q&A).

---
*Hết batch → sinh Batch #12 từ Module B trong ADVANCED.md (notes-first, commit+push mỗi lượt, không Claude).*

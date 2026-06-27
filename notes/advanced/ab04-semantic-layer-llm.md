# AB04 — Semantic Layer cho LLM (NL → metric, không SQL thô)

> Thay vì để LLM sinh **SQL thô** (nguy hiểm, hay sai), cho LLM sinh **truy vấn metric qua semantic layer** đã governed. An toàn hơn, nhất quán hơn, ít hallucinate hơn. Liên hệ [[e05-semantic-layer]], [[aa01-text-to-sql]].

## Vấn đề của text-to-SQL thô
LLM sinh SQL trực tiếp trên bảng vật lý → rủi ro ([[aa01-text-to-sql]]):
- **Sai logic metric**: "revenue" = gross hay net? trừ refund chưa? LLM đoán → mỗi lần một kiểu → **số không nhất quán**.
- **Hallucinate schema**: bịa tên cột/bảng không tồn tại.
- **Nguy hiểm**: có thể sinh JOIN sai, quét toàn bảng, hoặc câu phá hoại (phải chặn bằng guardrail).
- **Khó audit**: mỗi câu SQL một khác, không ai chuẩn hoá.

## ⭐ Ý tưởng: chèn một tầng "ngữ nghĩa" vào giữa
```
        TEXT-TO-SQL THÔ                         NL → SEMANTIC LAYER (an toàn)
  NL ─> LLM ─> SQL thô ─> DB              NL ─> LLM ─> {metric, dimension, filter}
        (đoán JOIN, đoán                          (chỉ chọn từ danh mục
         định nghĩa, dễ sai)                       đã định nghĩa sẵn)
                                                          │
                                          semantic layer dịch ─> SQL CHUẨN ─> DB
                                          (định nghĩa metric 1 nơi, đã test)
```
LLM **không viết SQL** nữa — nó chỉ **chọn**: metric nào (`revenue`, `active_users`), chiều nào (`by_month`, `by_region`), lọc gì (`region='VN'`). Semantic layer ([[e05-semantic-layer]]) — nơi metric được định nghĩa **một lần, đúng, đã test** — biên dịch ra SQL.

## Vì sao an toàn & tốt hơn
| Tiêu chí | SQL thô | Qua semantic layer |
|----------|---------|--------------------|
| **Nhất quán** | mỗi lần một định nghĩa | metric định nghĩa 1 nơi → mọi người 1 số |
| **An toàn** | có thể sinh câu bậy | chỉ chọn trong danh mục governed; không có "DROP" để chọn |
| **Hallucination** | bịa cột/bảng | chỉ chọn metric/dim có thật → sai thì reject ngay |
| **Surface bé hơn** | toàn bộ SQL | tập hữu hạn {metric, dim, filter} → dễ validate |
| **Governed** | khó | quyền, định nghĩa, lineage ở semantic layer |
| **Dễ eval** | so SQL khó | so JSON {metric,dim,filter} dễ |

## Luồng triển khai
```
1. Định nghĩa semantic model: metric (revenue = sum(amount) - sum(refund)),
   dimension (date, region, product), join đã khai báo.   ← DE + analytics eng làm
2. Đưa DANH MỤC metric/dim cho LLM (trong prompt hoặc tool schema).
3. LLM map câu hỏi NL ─> {metric:"revenue", dim:["month"], filter:{region:"VN"}}  (JSON có schema)
4. VALIDATE: metric/dim có trong danh mục? filter hợp lệ? (pydantic — [[ai06-llm-output-governance]])
5. Semantic layer compile JSON ─> SQL chuẩn ─> chạy ─> trả số.
```
Bước 3 = bài toán **map vào tập hữu hạn** (dễ + an toàn hơn nhiều so với sinh SQL tự do). Bước 4 = lại đúng nguyên tắc **validate output LLM như data contract** ([[ai06-llm-output-governance]]).

## Liên hệ — đây là "function calling" có kỷ luật
Cho LLM một **tool** `query_metrics(metric, dimensions, filters)` với schema rõ. LLM gọi tool (chọn tham số), code mình kiểm soát phần chạy thật. Khác text-to-SQL ở chỗ: **bề mặt tấn công thu nhỏ về một hàm an toàn**, thay vì cả ngôn ngữ SQL.

## Khi nào vẫn cần text-to-SQL thô
- Câu hỏi **ad-hoc, khám phá** ngoài metric định nghĩa sẵn → vẫn cần text-to-SQL (kèm guardrail [[aa01-text-to-sql]] + sandbox read-only).
- **Thực dụng**: semantic layer cho 80% câu hỏi BI phổ biến (an toàn, nhất quán); text-to-SQL có guardrail cho 20% khám phá.

## Cạm bẫy
- **Danh mục metric nghèo** → LLM không map được câu hỏi → fallback (text-to-SQL hoặc "tôi chưa hỗ trợ").
- **Vẫn cần validate**: LLM có thể chọn metric không tồn tại / filter sai kiểu → reject ([[ai06-llm-output-governance]]).
- **Đồng nghĩa**: "doanh thu" / "revenue" / "sales" → cần synonym mapping vào metric chuẩn.
- Semantic layer **phải đúng từ đầu** — sai định nghĩa metric ở đây thì mọi câu trả lời đều sai (nhưng sai *nhất quán* và sửa *một nơi*).

## ✅ "Tự kiểm tra & tự mò"
- [ ] Vì sao SQL thô không nhất quán & nguy hiểm.
- [ ] LLM chọn {metric, dim, filter} thay vì viết SQL — an toàn hơn ở điểm nào.
- [ ] Liên hệ function-calling: thu nhỏ bề mặt tấn công.
- [ ] Khi nào vẫn cần text-to-SQL thô (80/20).
- 🔭 Tự mò: mở rộng `text_to_sql.py` — định nghĩa 3 metric (`revenue`, `order_count`, `aov`) + 2 dimension (`category`, `month`) thành một "semantic model" nhỏ; cho mock-LLM trả JSON {metric,dim} thay vì SQL; validate bằng pydantic rồi tự compile ra SQL chuẩn. So độ an toàn với bản sinh SQL thô.

➡️ Tiếp [[ab05-embedding-finetune]] — khi embedding general kém với domain.

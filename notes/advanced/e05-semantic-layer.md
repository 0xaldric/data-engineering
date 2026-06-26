# E05 — Semantic Layer & Metrics Layer

> Lớp giữa warehouse và BI: định nghĩa **metric một lần**, mọi nơi dùng nhất quán. Sâu hơn [[d02-dbt-advanced]].

## Vấn đề: "mỗi dashboard một con số"
"Revenue", "active user", "churn" được định nghĩa khác nhau ở mỗi dashboard/analyst (filter khác, công thức khác) → **số không khớp** → mất niềm tin vào data. Kinh điển: 3 báo cáo "doanh thu" ra 3 số.

## Semantic layer là gì
Lớp **định nghĩa metric & dimension tập trung** (as code, versioned), nằm giữa warehouse và công cụ tiêu thụ:
```
Warehouse (bảng) → SEMANTIC LAYER (định nghĩa metric/dimension) → BI / notebook / API
                          ▲ "revenue = SUM(line_total) WHERE status='completed'" — MỘT lần
```
Mọi tool query **qua** semantic layer → cùng định nghĩa → **một con số duy nhất**.

## Thành phần
- **Entity**: thực thể (customer, order).
- **Dimension**: trục cắt (date, category, region).
- **Measure**: cột tổng hợp được (line_total, quantity).
- **Metric**: công thức nghiệp vụ trên measure + filter (revenue, AOV, conversion_rate, churn).
```yaml
metrics:
  - name: revenue
    measure: line_total
    agg: sum
    filters: ["status = 'completed'"]
  - name: aov            # derived: revenue / order_count
    type: ratio
    numerator: revenue
    denominator: order_count
```

## Headless BI
Semantic layer "không giao diện" (headless) — cung cấp metric qua **API/SQL** cho **bất kỳ** tool (Tableau, Looker, notebook, app) → không khoá vào một BI tool, metric nhất quán khắp nơi.

## Công cụ
- **dbt Semantic Layer / MetricFlow** — định nghĩa metric trong dbt, query `dbt sl query` ([[d02-dbt-advanced]]).
- **Cube** (Cube.dev) — semantic layer + API + cache, độc lập.
- **LookML** (Looker) — semantic layer gắn Looker.
- **Malloy**, **MetricFlow** standalone.

## Lợi ích
- **Một định nghĩa** metric → số nhất quán mọi nơi (single source of truth cho metric).
- **Governance**: đổi định nghĩa metric một chỗ → mọi dashboard cập nhật.
- **DRY**: không lặp công thức trong từng dashboard.
- **Tránh fan-out/sai filter** ở tầng BI (metric đã đúng sẵn).
- Tách "định nghĩa nghiệp vụ" khỏi "công cụ hiển thị".

## Liên hệ
Là tầng trên cùng của pipeline: source → staging → marts ([[23-dbt-marts]]) → **semantic layer** → BI. Bổ sung (không thay) marts — marts cung cấp bảng sạch, semantic layer định nghĩa metric trên đó.

## ⚠️ Cạm bẫy
- Không có semantic layer ở tổ chức lớn → "metric drift" (số lệch giữa team).
- Định nghĩa metric trong từng dashboard (lặp, lệch) thay vì tập trung.
- Over-engineer cho team nhỏ (vài dashboard) — có thể chỉ cần dbt marts + quy ước.
- Semantic layer chậm nếu không cache (Cube có cache; cân nhắc).

## ✅ "Tự mò"
🔭 Trong dbt project Phase 3, định nghĩa 2 metric (revenue, aov) bằng MetricFlow (semantic_models + metrics yaml); hoặc viết "định nghĩa metric" dạng YAML + 1 macro tính revenue dùng chung cho mọi mart → đảm bảo nhất quán.

➡️ Tiếp: [[00-moduleE-summary]].

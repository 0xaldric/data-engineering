# D02 — dbt Advanced

> Sâu hơn Phase 3 ([[21-warehouse-dbt]]→[[28-dbt-docs-lineage]]): semantic layer, packages, custom materialization, project lớn.

## Semantic Layer / Metrics (MetricFlow)
**Vấn đề:** "active user", "revenue" định nghĩa khác nhau ở mỗi dashboard → số không khớp. **Semantic layer** định nghĩa **metric một lần**, mọi tool query qua đó → nhất quán.
```yaml
# semantic_models + metrics (dbt MetricFlow)
metrics:
  - name: revenue
    type: simple
    type_params: {measure: line_total}
    filter: "{{ Dimension('order__status') }} = 'completed'"
```
- Định nghĩa **measures, dimensions, entities** trên model → metric tái dùng, query bằng `dbt sl query`.
- Lợi: "single source of truth" cho metric; BI tool (Hex, Lightdash, Tableau qua connector) dùng chung. Tránh "mỗi nơi tự SUM một kiểu".

## Packages quan trọng
| Package | Dùng |
|---------|------|
| **dbt_utils** | helper: `generate_surrogate_key`, `star`, `date_spine`, `pivot`, nhiều generic test |
| **dbt_expectations** | test kiểu Great Expectations (range, distribution, regex) |
| **audit_helper** | so sánh 2 model (migration, refactor an toàn) |
| **codegen** | sinh boilerplate (yaml, base models) |
| **dbt_project_evaluator** | kiểm best practice project |
Cài qua `packages.yml` + `dbt deps`.

## Custom materialization
Ngoài view/table/incremental/ephemeral, viết materialization riêng (macro) cho nhu cầu đặc thù (vd insert_by_period, scd custom). Hiếm cần; biết là có.

## Cấu trúc project LỚN
```
models/
├── staging/        (1 thư mục / nguồn: stg_<source>__<entity>)
│   └── <source>/
├── intermediate/   (int_<area>__<verb>)
├── marts/
│   ├── core/       (dim_, fct_ dùng chung)
│   ├── finance/    (mart theo domain)
│   └── marketing/
└── utilities/
```
- **Phân theo domain** ở marts (finance/marketing/...) cho team lớn.
- Naming convention nghiêm (stg_/int_/dim_/fct_/mart_).
- `dbt_project.yml`: cấu hình materialization + tags theo thư mục; `+tags` để chạy nhóm (`dbt run -s tag:finance`).

## Patterns nâng cao
- **Incremental nâng cao**: `incremental_strategy` (merge/insert_overwrite/microbatch), `on_schema_change`, lookback window cho late data ([[27-dbt-incremental]]).
- **Contracts** (`contract: {enforced: true}`): ép schema model (cột/kiểu) → build fail nếu lệch — data contract ([[61-data-contracts]]).
- **Snapshots** nâng cao (check vs timestamp, invalidate_hard_deletes) ([[26-dbt-snapshots]]).
- **Exposures**: khai báo dashboard/ML dùng model → lineage tới sản phẩm cuối ([[28-dbt-docs-lineage]]).
- **Hooks** (`pre-hook`/`post-hook`, `on-run-end`): grant quyền, vacuum, log.

## CI/CD nâng cao (Slim CI)
- `dbt build --select state:modified+` (so với manifest production) → chỉ build/test model **thay đổi + downstream** → CI nhanh ([[58-cicd]]).
- `dbt build --defer` dùng model production cho upstream không đổi → khỏi build lại toàn bộ.
- Test trên dataset CI riêng; blue-green deploy.

## ⚠️ Cạm bẫy
- Một model khổng lồ làm mọi thứ → chia staging/intermediate/marts.
- Logic metric lặp ở nhiều model → semantic layer.
- Không slim CI → CI chậm dần khi project lớn.
- Lạm dụng macro → SQL khó đọc/debug.

## ✅ "Tự mò"
🔭 Trong dbt project Phase 3: thêm `dbt_expectations` test (accepted_range cho discount), bật `contract: enforced` cho 1 mart, thử `dbt build -s state:modified+` (cần manifest cũ).

➡️ Tiếp: [[d03-kafka-internals]].

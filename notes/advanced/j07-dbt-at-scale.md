# J07 — Deep-dive: dbt at Scale (large project)

> dbt project nhỏ thì dễ; **nghìn model, nhiều team** thì dễ thành "spaghetti". Cách giữ maintainable. Sâu hơn [[d02-dbt-advanced]], [[23-dbt-marts]].

## Vấn đề khi dbt project lớn
- Nghìn model → khó tìm, phụ thuộc rối, build chậm, không ai hiểu toàn cục.
- Nhiều team đụng cùng project → conflict, không rõ ownership.
- Metric định nghĩa lung tung → số lệch.
- Build full mỗi lần → chậm + tốn tiền.

## ⭐ Cấu trúc theo domain + layer
```
models/
├── staging/<source>/        stg_<source>__<entity>   (1-1 nguồn, view)
├── intermediate/<domain>/   int_<domain>__<verb>     (logic trung gian)
└── marts/
    ├── core/                dim_, fct_ DÙNG CHUNG (conformed)
    ├── finance/             mart theo domain + ownership
    ├── marketing/
    └── product/
```
- **Core marts** (conformed dim/fact) dùng chung; **domain marts** riêng team.
- Naming convention **nghiêm** (stg_/int_/dim_/fct_/mart_ + domain) → đọc tên biết vai trò/lớp.

## Quản lý phụ thuộc & ownership
- **Tags** theo domain/tier: `dbt build -s tag:finance` (chạy theo nhóm).
- **Owner** (meta/group) per model/folder → ai chịu trách nhiệm.
- **Contracts** giữa domain (model "public" có schema enforced — [[61-data-contracts]]) → team khác dựa vào interface ổn định, không vào internal.
- **Exposures**: khai báo dashboard/ML dùng model → lineage tới sản phẩm cuối, impact analysis ([[28-dbt-docs-lineage]]).

## Performance ở scale ⭐
- **Incremental** cho fact lớn (không full rebuild — [[27-dbt-incremental]]); chọn strategy + lookback.
- **Materialization đúng**: view (rẻ, staging) vs table (đọc nhiều) vs incremental (fact lớn) vs ephemeral.
- **Slim CI**: `dbt build -s state:modified+` (chỉ model đổi + downstream) — CI không chậm dần ([[d02-dbt-advanced]], [[58-cicd]]).
- **`--defer`**: dùng model production cho upstream không đổi → khỏi build lại.
- Tránh model "fan-in" khổng lồ (1 model join 50 model) → chia nhỏ.

## Governance metric
- **Semantic layer / metrics** ([[e05-semantic-layer]]): định nghĩa metric 1 lần → nhất quán xuyên team, tránh "mỗi mart tự SUM".
- `dbt_project_evaluator` package: kiểm best practice (model không test, naming sai, fan-in...).

## Multi-project / mesh (rất lớn)
- **dbt Mesh**: chia thành nhiều dbt project theo domain, cross-project `ref` qua public models + contracts → mỗi team sở hữu project mình (data mesh — [[f05-data-mesh]]).
- Giảm "monolith dbt" khi quá lớn.

## Tránh "spaghetti dbt" — checklist
- [ ] Naming/folder convention nghiêm theo layer + domain.
- [ ] Mọi model có description + test (CI enforce).
- [ ] Core conformed dim/fact, domain marts riêng.
- [ ] Contracts cho model public; exposures cho consumer.
- [ ] Incremental + slim CI (không full rebuild).
- [ ] Semantic layer cho metric.
- [ ] Owner rõ; project_evaluator kiểm định kỳ.

## ⚠️ Cạm bẫy
- Một model làm quá nhiều → chia.
- Build full mỗi lần → slim CI + incremental.
- Không convention → 1000 model hỗn loạn.
- Metric lặp ở nhiều mart → semantic layer.
- Không test/contract → đổi staging vỡ downstream âm thầm.

## ✅ "Tự mò"
🔭 Tổ chức lại dbt project Phase 3 theo domain (core/ + 1 domain folder); thêm tags; chạy `dbt build -s tag:...`; cài `dbt_project_evaluator` xem nó cảnh báo gì.

➡️ Tiếp: [[00-extraJ-summary]].

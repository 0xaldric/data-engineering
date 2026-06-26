# B03 — Warehousing & dbt Q&A

> Câu hỏi phỏng vấn warehouse/dbt + đáp án. Chi tiết: [[21-warehouse-dbt]]→[[28-dbt-docs-lineage]].

**Q: ETL vs ELT?**
A: ETL transform **trước** khi nạp (Spark/Python ngoài). ELT nạp thô rồi transform **trong warehouse bằng SQL**. Warehouse cloud mạnh+rẻ → ELT là chuẩn hiện đại; dbt là công cụ chữ "T".

**Q: dbt làm gì? Không làm gì?**
A: Biến SQL SELECT thành pipeline transform có test/docs/lineage/DAG. **Không** ingest/extract (chỉ "T" của ELT).

**Q: ref() vs source()?**
A: `source()` trỏ dữ liệu ngoài dbt (khai báo trong sources). `ref()` trỏ model khác. dbt dùng cả hai để **tự dựng DAG** & lineage. Không hardcode tên bảng.

**Q: Materializations?**
A: **view** (rẻ, luôn tươi — staging/intermediate); **table** (đọc nhanh — marts); **ephemeral** (CTE, không tạo object); **incremental** (chỉ build dữ liệu mới — fact lớn).

**Q: Layering staging→intermediate→marts?**
A: Staging (1-1 với source, clean/cast, view); intermediate (join/business logic trung gian); marts (fact/dim/aggregate cho BI, table). Mô-đun, tái dùng, lineage rõ.

**Q: dbt tests?**
A: Generic (`unique/not_null/relationships/accepted_values`) khai báo trong YAML + singular (SQL tuỳ ý). Test = query tìm hàng vi phạm, PASS nếu 0 hàng.

**Q: Vì sao `relationships` test quan trọng?**
A: Kiểm FK fact→dim — warehouse OLAP thường **không enforce** FK; dbt test bù lại.

**Q: Snapshot là gì?**
A: SCD Type 2 **tự động** của dbt: so dữ liệu hiện tại với bản lưu, đổi thì đóng phiên bản cũ (`dbt_valid_to`) + chèn mới. Strategy `check`/`timestamp`.

**Q: Incremental model & is_incremental()?**
A: Chỉ xử lý dữ liệu mới (`where ts > (select max(ts) from {{ this }})`). Strategy: append / merge / delete+insert / insert_overwrite. `--full-refresh` để build lại khi đổi logic.

**Q: Late-arriving data trong incremental?**
A: Watermark đơn giản (`> max`) bỏ sót data trễ → dùng **lookback window** (`>= max - N ngày`) + merge để không trùng.

**Q: Macros & Jinja?**
A: Jinja sinh SQL động (`{{ }}` biểu thức, `{% %}` lệnh, `{# #}` comment). Macro = hàm tái dùng (DRY). dbt_utils: `generate_surrogate_key`, `star`, `date_spine`...

**Q: dbt build vs run?**
A: `run` = build models. `build` = run + test + snapshot + seed theo **một DAG**; test fail chặn downstream → dùng trong production/CI.

**Q: dbt docs & lineage?**
A: `dbt docs generate` → manifest.json (DAG) + catalog.json (cột). Lineage cho impact analysis (`dbt ls -s model+`); exposures = nơi tiêu thụ.

**Q: Seeds?**
A: CSV nhỏ tĩnh versioned trong repo (lookup: country→region), nạp bằng `dbt seed`, dùng qua `ref()`.

**Q: Slim CI?**
A: CI chỉ build/test model **thay đổi** (`state:modified+`) thay vì full → nhanh. Chạy `dbt build` trên warehouse CI mỗi PR.

**Q: Cloud DW so sánh?**
A: BigQuery (serverless, tính theo bytes scanned), Snowflake (virtual warehouse co giãn, tính theo compute-time), Redshift (cluster). Điểm chung: tách compute/storage.

## ✅ "Tự mò"
🔭 Mở dbt project Phase 3, giải thích được mỗi model thuộc layer nào & vì sao chọn materialization đó.

➡️ Tiếp: [[b04-orchestration-qa]].

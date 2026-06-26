# 37 — Orchestration: là gì & vì sao cần

> Pipeline DE gồm nhiều bước phụ thuộc nhau (ingest → transform → test → load → report). **Orchestrator** điều phối chúng chạy đúng thứ tự, đúng lúc, tự xử lý lỗi.

## Vì sao cron thuần không đủ?
`cron` chỉ "chạy lệnh X lúc Y". Pipeline thật cần nhiều hơn:
| Nhu cầu | cron | Orchestrator |
|---------|------|--------------|
| Phụ thuộc (B chạy sau A xong) | ❌ tự xoay (sleep, file flag) | ✅ DAG khai báo |
| Retry khi lỗi | ❌ | ✅ tự retry + backoff |
| Backfill (chạy bù quá khứ) | ❌ | ✅ |
| Theo dõi/log/alert tập trung | ❌ | ✅ UI + alert |
| Truyền dữ liệu giữa bước | ❌ | ✅ XCom/assets |
| Chạy lại 1 bước giữa chừng | ❌ (chạy lại cả script) | ✅ |
| Quản lý concurrency/tài nguyên | ❌ | ✅ pools |

→ Khi pipeline > vài bước hoặc cần độ tin cậy production, **cần orchestrator**.

## DAG — trái tim của orchestration
**DAG** = Directed Acyclic Graph (đồ thị có hướng, **không chu trình**). Mỗi node = một **task** (việc cần làm), mỗi cạnh = **phụ thuộc** (thứ tự).
```
ingest_api ─┐
            ├─► transform ─► test ─► load ─► notify
ingest_db  ─┘
```
- "Có hướng": A → B nghĩa là B chạy **sau** A.
- "Không chu trình": không được A→B→A (kẹt vô hạn).
- Orchestrator đọc DAG → biết cái gì chạy song song (ingest_api & ingest_db), cái gì chờ (transform chờ cả hai).

## Các orchestrator phổ biến
- **Apache Airflow** ⭐ — phổ biến nhất, chuẩn de-facto; DAG bằng Python; hệ sinh thái operator khổng lồ. (Trọng tâm Phase này.)
- **Dagster** — hiện đại, xoay quanh **data assets** + lineage + testability ([[44-dagster-prefect]]).
- **Prefect** — Pythonic, flow động, nhẹ.
- **dbt** — không phải orchestrator tổng quát; lo riêng phần transform (thường được orchestrator gọi). Xem [[21-warehouse-dbt]].
- Cloud-managed: AWS MWAA (Airflow), Google Cloud Composer, Astronomer.

## Orchestrator KHÔNG làm gì
Nó **điều phối**, không tự xử lý dữ liệu nặng. Task thật nên đẩy việc nặng xuống công cụ chuyên (Spark, dbt, warehouse SQL, Python). Airflow chỉ nên "ra lệnh & theo dõi", không kéo triệu dòng vào RAM của worker Airflow (anti-pattern).

## ✅ Tự kiểm tra & "tự mò"
- [ ] Cron thiếu gì so với orchestrator (phụ thuộc, retry, backfill, monitor).
- [ ] DAG là gì; "có hướng, không chu trình" nghĩa là gì.
- [ ] Kể vài orchestrator & vai trò; vì sao orchestrator không nên xử lý dữ liệu nặng.
- 🔭 *Tự mò:* vẽ DAG cho pipeline đã build (ingest → polars transform → DuckDB load → dbt run → test). Đâu chạy song song được?

➡️ Tiếp: [[38-airflow-core]].

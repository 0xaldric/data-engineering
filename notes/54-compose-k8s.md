# 54 — docker-compose & Kubernetes basics

> Một container thì dễ; **nhiều dịch vụ** phối hợp (DB + queue + app) cần công cụ điều phối container.

## docker-compose — multi-service local ⭐
Khai báo nhiều container + network + volume trong một file `docker-compose.yml`, bật bằng `docker compose up`. Tuyệt cho **dựng stack học/test local**.
```yaml
services:
  postgres:
    image: postgres:16
    environment: { POSTGRES_PASSWORD: pass }
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
  airflow:
    image: apache/airflow:2.9.0
    depends_on: [postgres]
    ports: ["8080:8080"]
volumes: { pgdata: {} }
```
- Các service cùng compose tự thấy nhau qua **tên service** (DNS nội bộ): app nối `postgres:5432`.
- `depends_on` thứ tự khởi động; volume giữ dữ liệu DB.
→ Cách chuẩn để chạy **Postgres + Kafka + Airflow + Debezium** trên laptop mà học (các "tự mò" ở [[46-kafka-core]], [[51-cdc-debezium]] dùng cái này).

## Kubernetes (K8s) — điều phối container ở quy mô lớn
Khi cần chạy hàng trăm container trên nhiều máy, tự healing, scale: **K8s**.
| Khái niệm | Là gì |
|-----------|-------|
| **Pod** | đơn vị nhỏ nhất — 1 (hoặc vài) container chạy cùng nhau |
| **Deployment** | quản lý số replica của pod, rolling update, self-heal (pod chết → tạo lại) |
| **Service** | địa chỉ ổn định + load-balance tới các pod |
| **Namespace** | nhóm/cô lập tài nguyên |
| **ConfigMap/Secret** | cấu hình & secret cho pod |
| **PersistentVolume** | lưu trữ bền cho pod |
- K8s **tự**: lên lịch pod lên node, restart khi lỗi, scale theo tải (HPA), rolling deploy.

## K8s cho data workload
- **Spark on K8s**: chạy Spark driver/executor là pod (thay YARN).
- **Airflow KubernetesExecutor / KubernetesPodOperator**: mỗi task = một pod riêng → cô lập dependency, scale, dọn sạch sau khi xong ([[42-airflow-resources]]).
- **Flink/Kafka** cũng deploy trên K8s (operator).
- Cloud-managed K8s: EKS (AWS), GKE (GCP), AKS (Azure).

## docker-compose vs K8s
- **compose**: local/dev, một máy, đơn giản. Học & test stack.
- **K8s**: production, nhiều máy, tự scale/heal, phức tạp vận hành. Có thể quá mức cho team nhỏ → cân nhắc serverless/managed.

## ⚠️ Cạm bẫy
- Dùng compose cho production multi-node (không scale/heal) — đó là việc của K8s.
- Nhảy vào K8s khi chưa cần (overhead vận hành lớn) — bắt đầu đơn giản (managed service/compose).
- Quên persistent volume → mất state pod khi restart.
- Không đặt resource request/limit → pod tranh tài nguyên.

## ✅ Tự kiểm tra & "tự mò"
- [ ] docker-compose dùng cho gì; service thấy nhau qua đâu.
- [ ] Pod/Deployment/Service; K8s tự làm gì (heal/scale/rolling).
- [ ] K8s cho data (Spark on K8s, Airflow KubernetesExecutor).
- [ ] compose vs K8s — khi nào dùng cái nào.
- 🔭 *Tự mò:* viết `docker-compose.yml` dựng Postgres + một service Python; `docker compose up`; kết nối Python → Postgres qua tên service. (K8s: thử `kind`/`minikube` local nếu rảnh.)

➡️ Tiếp: [[55-cloud-fundamentals]].

# 53 — Docker & Containers ⭐

> Container đóng gói code + mọi dependency thành một đơn vị **chạy giống nhau ở mọi nơi** (laptop, CI, cloud). Nền tảng vận hành DE hiện đại.

## Container vs VM
| | **VM** | **Container** |
|--|--------|----------------|
| Ảo hoá | phần cứng (cả OS riêng) | OS-level (chung kernel host) |
| Kích thước | GB | MB |
| Khởi động | phút | giây |
| Cô lập | mạnh hơn | nhẹ, đủ dùng |
→ Container nhẹ & nhanh → đóng gói/scale dịch vụ dễ. "Chạy được trên máy tôi" hết thành vấn đề.

## Khái niệm
- **Image**: bản mẫu bất biến (read-only) chứa OS base + lib + code. Build từ **Dockerfile**.
- **Container**: một **instance đang chạy** của image (thêm lớp ghi-được lên trên).
- **Layer**: image gồm nhiều lớp (mỗi lệnh Dockerfile = 1 lớp), **cache** lại → build nhanh, chia sẻ lớp chung.
- **Registry**: kho image (Docker Hub, AWS ECR, GHCR) — push/pull.
- **Volume**: lưu dữ liệu **bền** ngoài vòng đời container (container xoá, data còn).
- **Network/port**: container nói chuyện nhau qua network ảo; `-p 8080:8080` map cổng ra host.

## Dockerfile (minh hoạ)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # lớp này cache khi requirements không đổi
COPY . .
CMD ["python", "etl_pipeline.py"]
```
- Thứ tự quan trọng: copy `requirements.txt` + install **trước** copy code → đổi code không phải cài lại lib (tận dụng cache).
- `slim`/`alpine` base nhỏ; multi-stage build để image gọn (build ở stage 1, copy artifact sang stage 2).

## Vì sao DE cần Docker
- **Reproducible environment**: cùng image → cùng phiên bản Python/Spark/lib ở dev/CI/prod (hết "máy tôi chạy được").
- **Đóng gói pipeline/job**: chạy task trong container (Airflow KubernetesPodOperator — [[42-airflow-resources]]).
- **Local stack**: dựng Postgres+Kafka+Airflow bằng docker-compose để học/test ([[54-compose-k8s]]).
- Nền cho **Kubernetes** (scale) và serverless container.

## Lệnh hay dùng
`docker build -t name .` · `docker run -p 8080:8080 -v $PWD/data:/data name` · `docker ps` · `docker logs <id>` · `docker exec -it <id> bash` · `docker compose up`.

## ⚠️ Cạm bẫy
- Image phình to (cài cả build tools) → dùng slim + multi-stage + `.dockerignore`.
- Đặt `COPY . .` trước install → mất cache, build lại lib mỗi lần.
- Lưu dữ liệu trong container (mất khi xoá) → dùng **volume**.
- Để secret trong image/Dockerfile → dùng env/secret runtime, không bake vào image.
- Chạy as root trong container → tạo user thường.

## ✅ Tự kiểm tra & "tự mò"
- [ ] Container vs VM; image vs container vs layer.
- [ ] Vì sao thứ tự lệnh Dockerfile ảnh hưởng cache.
- [ ] Volume vs dữ liệu trong container.
- [ ] Vì sao DE cần Docker (reproducible, đóng gói job).
- 🔭 *Tự mò:* viết Dockerfile cho ETL pipeline Phase 1 (`etl_pipeline.py`), `docker build` + `docker run` với volume mount `data/`. Xem image layers bằng `docker history`.

➡️ Tiếp: [[54-compose-k8s]].

# 🚀 Advanced Data Engineering & Interview Prep — Track 2

> Curriculum chính (Phase 0–9) đã xong. Đây là **track nâng cao** cho loop làm tiếp: SQL mastery, interview prep, system design, deep-dives. **Notes-first** (tiếng Việt). Notes đặt trong `notes/advanced/`.

Loop lấy chủ đề từ các **Module** dưới đây, mỗi chủ đề → 1 note đầy đủ. Khi hết một batch → sinh batch mới từ module tiếp theo.

---

## Module A — SQL Mastery & Analytics Patterns
- Advanced SQL I: gaps & islands, sessionization, running/cumulative, frame nâng cao
- Advanced SQL II: pivot/unpivot, hierarchical/recursive, dedup strategies, conditional agg
- Analytics patterns: funnel analysis, cohort & retention, RFM segmentation, attribution
- SQL interview problems — set 1 (10 bài + lời giải, độ khó tăng dần)
- SQL interview problems — set 2 (window-heavy, tricky)
- SQL performance & query optimization (đọc plan sâu, rewrite, index chiến lược)
- SQL conceptual Q&A (câu hỏi phỏng vấn + trả lời)

## Module B — DE Interview Prep (conceptual)
- SQL & data modeling Q&A
- Spark & big data Q&A
- Streaming & Kafka Q&A
- Warehousing & dbt Q&A
- Pipeline/orchestration & reliability Q&A
- Cloud & infra Q&A
- Behavioral + scenario questions (STAR method cho DE)
- "Explain like senior": giải thích sâu 10 khái niệm hay bị hỏi

## Module C — System Design for Data Engineering
- Framework thiết kế hệ thống DE (requirements → data model → pipeline → serving → scale)
- Case: E-commerce analytics platform
- Case: Real-time fraud detection
- Case: IoT / sensor data platform
- Case: Ride-sharing data platform (như Uber)
- Case: Clickstream / social media analytics
- Case: Fintech ledger + reconciliation
- Case: Ad-tech / real-time bidding
- Case: Recommendation system data pipeline

## Module D — Advanced Tool Deep-dives
- Spark internals: memory management, Tungsten, AQE sâu, debug job chậm
- dbt advanced: semantic layer/metrics, packages, custom materialization, cấu trúc project lớn
- Kafka internals: storage, replication protocol, exactly-once sâu, tuning
- Snowflake deep: kiến trúc, micro-partition, clustering, tối ưu chi phí
- BigQuery deep: slot, partition/cluster, tối ưu bytes-scanned
- Airflow advanced: dynamic DAG, custom operator, deferrable, best practice scale
- Iceberg deep: metadata layers, hidden partition, compaction, catalog

## Module E — Advanced Data Modeling
- Data Vault 2.0 (hub/link/satellite)
- One Big Table, wide tables, activity schema
- Modeling event/clickstream data
- Bitemporal modeling (valid time vs transaction time)
- Semantic layer & metrics layer

## Module F — DataOps, Architecture & Career
- Data testing strategy toàn diện
- Pipeline reliability & incident management (SRE cho data)
- Modern data stack landscape & cách chọn tool
- Cost optimization case studies (số liệu thật)
- Data mesh, data products, ownership & team topology
- DataOps & CI/CD nâng cao cho data
- Roadmap senior/staff DE & cách phát triển sự nghiệp

## Module AI — AI Data Engineering ⭐ (ƯU TIÊN — tiêu chuẩn phỏng vấn mới 2025+)
> Trụ cột thứ 4 trong tiêu chuẩn DE mới: **hạ tầng dữ liệu cho AI** (trọng số ngang SQL/pipeline/modeling). "Danh từ đổi, tư duy không đổi." Mục này có **code chạy được** (ngoại lệ notes-first) vì là portfolio piece. Đã có capstone `projects/06-ai-data-engineering/rag_over_notes.py` (RAG trên chính kho notes, local).
- RAG capstone over own notes (chunk→embed→DuckDB vector store→search→recall@k) — ĐÃ BUILD
- Chunking strategies sâu (fixed/semantic/structure-aware, overlap, parent-child)
- Embedding models & **versioning** (chọn model, dimension, re-embed khi đổi model — đắt)
- Vector DB internals (HNSW/IVF, ANN vs brute-force, DuckDB VSS, metadata filter)
- Retrieval **eval** sâu (recall@k, MRR, nDCG, re-ranking, RAG faithfulness/RAGAS)
- **LLM-as-data-producer governance** ⭐: validate structured output (pydantic+repair), data contract cho output LLM, version model+prompt+output, drift, human-in-loop
- **Testing dữ liệu non-deterministic** ⭐: golden set, semantic equivalence (cosine), schema validation, statistical/distribution tests thay exact-match
- **Cost & latency** cho AI pipeline (token cost, cache/batch embedding, rate-limit, real-time serving)
- **Streaming cho AI infra**: re-index <1 phút khi tài liệu đổi (event-driven), feature serving real-time
- Module AI review + map sang tiêu chuẩn phỏng vấn mới

---
*Khi hết tất cả module → loop có thể đào sâu thêm bất kỳ chủ đề nào ở trên (set bài tập mới, case study mới), hoặc dừng.*

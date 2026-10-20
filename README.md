# Data Science Project Template (uv)

เทมเพลตโปรเจกต์ Data Science ที่ใช้ [uv](https://docs.astral.sh/uv/) จัดการ Python, virtualenv และ dependencies

## เริ่มต้นใช้งาน

```bash
# 1. ติดตั้ง uv (ครั้งเดียว)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. ติดตั้ง dependencies ทั้งหมด (สร้าง .venv ให้อัตโนมัติ)
uv sync

# 3. ติดตั้ง pre-commit hooks
uv run pre-commit install

# 4. ลองเทรนโมเดลตัวอย่าง
uv run train
```

หรือใช้ `make install`, `make test`, `make train`, `make notebook`

## โครงสร้างโปรเจกต์

```
├── data/
│   ├── raw/          # ข้อมูลดิบ (ห้ามแก้ไข)
│   ├── interim/      # ข้อมูลระหว่างการแปลง
│   ├── processed/    # ข้อมูลพร้อมใช้สำหรับโมเดล
│   └── external/     # ข้อมูลจากแหล่งภายนอก
├── models/           # โมเดลที่เทรนแล้ว
├── notebooks/        # Jupyter notebooks สำหรับ EDA / ทดลอง
├── reports/figures/  # กราฟและรายงาน
├── src/ds_project/   # โค้ดหลักของโปรเจกต์
│   ├── config.py     # paths และค่าตั้งต้น
│   ├── data.py       # โหลดและแบ่งข้อมูล
│   ├── features.py   # feature engineering pipeline
│   ├── train.py      # เทรนและบันทึกโมเดล
│   └── rename.py     # คำสั่ง rename (ใช้ครั้งเดียว แล้วลบตัวเอง)
├── tests/            # unit tests (pytest)
├── pyproject.toml    # metadata, dependencies, การตั้งค่า ruff/pytest
├── uv.lock           # lockfile (commit ไฟล์นี้ด้วย)
└── .python-version   # เวอร์ชัน Python ที่ uv จะใช้
```

ไฟล์ใน `data/` และ `models/` ถูก ignore จาก git เก็บไว้แค่โครงสร้างโฟลเดอร์

## คำสั่ง uv ที่ใช้บ่อย

| งาน | คำสั่ง |
| --- | --- |
| เพิ่ม dependency | `uv add xgboost` |
| เพิ่ม dev dependency | `uv add --dev mypy` |
| เพิ่มเข้า group notebook | `uv add --group notebook plotly` |
| ลบ dependency | `uv remove xgboost` |
| อัปเดต lockfile | `uv lock --upgrade` |
| รันคำสั่งใน venv | `uv run python script.py` |
| เปิด Jupyter Lab | `uv run jupyter lab` |
| เปลี่ยนเวอร์ชัน Python | `uv python pin 3.13` แล้ว `uv sync` |
| ติดตั้งแบบ production (ไม่มี dev/notebook) | `uv sync --no-default-groups` |

## ใช้เทมเพลตนี้กับโปรเจกต์ใหม่

1. กด **Use this template** บน GitHub หรือ clone repo นี้
2. เปลี่ยนชื่อโปรเจกต์ด้วยคำสั่ง `rename` (แก้ชื่อใน `pyproject.toml`, `src/`, `tests/`, README และสร้าง `uv.lock` ใหม่ให้อัตโนมัติ เสร็จแล้วคำสั่งนี้จะลบตัวเองออก)

   ```bash
   uv run rename churn-model --dry-run  # ดูก่อนว่าจะแก้อะไร
   uv run rename churn-model
   uv sync
   ```

   ผลลัพธ์: แพ็กเกจ `churn_model`, ชื่อ distribution `churn-model`, คำสั่ง `uv run train` ใช้ชื่อเดิม
3. คัดลอก `.env.example` เป็น `.env` แล้วใส่ค่าที่ต้องใช้

## Quality checks

```bash
uv run ruff check .        # lint
uv run ruff format .       # format
uv run pytest              # test
```

GitHub Actions (`.github/workflows/ci.yml`) จะรัน lint และ test ทุกครั้งที่ push / เปิด PR

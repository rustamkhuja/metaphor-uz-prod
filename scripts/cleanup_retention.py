from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import SessionLocal, init_db
from app.services.retention import clean_expired_raw_inputs

init_db()
with SessionLocal() as db:
    print({"records_cleaned": clean_expired_raw_inputs(db)})

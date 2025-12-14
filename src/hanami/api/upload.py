from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from hanami.services.ingestion import load_and_validate_file, InvalidDataError
from hanami.db.connection import engine
from hanami.db.repository import SalesRepository
import uuid

router = APIRouter()

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(None)):
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")

    file_id = uuid.uuid4().hex
    destination = RAW_DIR / f"{file_id}_{file.filename}"

    try:
        contents = await file.read()
        destination.write_bytes(contents)

        df = load_and_validate_file(destination)

        repo = SalesRepository(engine)
        linhas = repo.save_dataframe(df)

        return {
            "status": "sucesso",
            "linhas_processadas": linhas,
            "arquivo": destination.name,
        }

    except InvalidDataError as e:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=str(e))

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from loguru import logger
import uuid

from hanami.services.ingestion import load_and_validate_file, InvalidDataError
from hanami.db.connection import engine
from hanami.db.repository import SalesRepository

router = APIRouter(prefix="/upload", tags=["Upload"])

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(None)):
    """
    Recebe um arquivo CSV ou XLSX, valida os dados
    e persiste o conteúdo no banco de dados.
    """

    if file is None:
        logger.error("Upload falhou: nenhum arquivo enviado")
        raise HTTPException(
            status_code=400,
            detail="Nenhum arquivo enviado"
        )

    file_id = uuid.uuid4().hex
    file_path = RAW_DIR / f"{file_id}_{file.filename}"

    try:
        # Salva arquivo temporariamente
        content = await file.read()
        file_path.write_bytes(content)

        # Validação e limpeza
        df = load_and_validate_file(file_path)

        # Persistência
        repository = SalesRepository(engine)
        rows_inserted = repository.save_dataframe(df)

        logger.info(
            "Upload concluído com sucesso | arquivo={} | linhas_processadas={}",
            file_path.name,
            rows_inserted,
        )

        return {
            "status": "sucesso",
            "linhas_processadas": rows_inserted,
        }

    except InvalidDataError as exc:
        logger.error(
            "Erro de validação no upload | arquivo={} | erro={}",
            file.filename,
            exc,
        )
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception as exc:
        logger.exception(
            "Erro inesperado durante upload | arquivo={}",
            file.filename,
        )
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Erro interno no servidor",
        )

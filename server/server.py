import httpx
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from helical.utils import get_anndata_from_hf_dataset
import os
import logging
import warnings
from datasets import load_dataset

from pydantic import BaseModel

SERVICE1_URL = os.getenv("SERVICE1_URL", "http://localhost:8001")  # Dev fallback
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://localhost:8002")
SERVICE3_URL = os.getenv("SERVICE3_URL", "http://localhost:8006")

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")

class Dataset(BaseModel):
    name: str

class State(BaseModel):
    model_name: str
    batch_size: int
    dataset_name: str
    application_name: str


logging.getLogger().setLevel(logging.ERROR)

warnings.filterwarnings("ignore")

app = FastAPI()

@app.post("/run")
async def run_application(request: State):
    """
    Run the application.
    """
    response = None
    match request.application_name:
        case "Cell type":
            print("Running Cell type application")
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{SERVICE1_URL}/predict",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    }
                )
        case "Cell type - fine tuning":
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"http://localhost:8011/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case "Cell Gene Embeddings":
            async with httpx.AsyncClient(timeout=1200) as client:
                response = await client.post(
                    "http://localhost:8003/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case "Helix-mRNA":
            async with httpx.AsyncClient(timeout=1200) as client:
                response = await client.post(
                    "http://localhost:8004/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case "Genegpt":
            async with httpx.AsyncClient(timeout=1200) as client:
                response = await client.post(
                    "http://localhost:8005/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case "Geneformer VS TranscriptFormer":
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{SERVICE3_URL}/predict",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    }
                )
        case "HyenaDNA - Fine Tuning":
            async with httpx.AsyncClient(timeout=1200) as client:
                response = await client.post(
                    "http://localhost:8007/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case "HyenaDNA - Inference":
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{SERVICE2_URL}/predict",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    }
                )
        case "Evo 2":
            async with httpx.AsyncClient(timeout=1200) as client:
                response = await client.post(
                    "http://localhost:8009/run",
                    json={
                        "model_name": request.model_name,
                        "dataset_name": request.dataset_name,
                        "batch_size": request.batch_size,
                    },
                )
        case _:
            pass

    # Placeholder for application logic
    return JSONResponse(content=response.json())


@app.post("/dataset")
async def dataset(request: Dataset):
    """
    Load a dataset pre-defined.
    """
    dataset = load_dataset(request.name, split="train[:10%]", trust_remote_code=True, download_mode="reuse_cache_if_exists")
    labels = dataset["LVL1"]
    ann_data = get_anndata_from_hf_dataset(dataset)

    return JSONResponse(content={"message": "Dataset loaded successfully", "labels": labels})


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)
    return JSONResponse(content={"success": True, "filename": file.filename})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
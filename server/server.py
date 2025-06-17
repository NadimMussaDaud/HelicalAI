from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import scanpy as sc
import tempfile
import os
import logging
import warnings
from datasets import load_dataset
from helical.utils import get_anndata_from_hf_dataset


from pydantic import BaseModel

class Dataset(BaseModel):
    name: str


logging.getLogger().setLevel(logging.ERROR)

warnings.filterwarnings("ignore")

app = FastAPI()
"""
@app.post("/annotate")
async def annotate(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Read expression matrix and annotate with Helical
    adata = sc.read_csv(tmp_path)
    os.remove(tmp_path)

    annotated = annotate_cell_types(adata)

    # Return summary of predicted cell types
    summary = annotated.obs["predicted_cell_type"].value_counts().to_dict()
    return JSONResponse(content={"annotation_summary": summary})
"""

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
    save_path = f"/workspaces/HelicalAI/datasets/{file.filename}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)
    return JSONResponse(content={"success": True, "filename": file.filename})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
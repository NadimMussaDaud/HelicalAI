from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import scanpy as sc
from helical import annotate_cell_types
import tempfile
import os

app = FastAPI()

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

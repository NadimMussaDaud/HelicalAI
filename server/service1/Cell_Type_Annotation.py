from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class Dataset(BaseModel):
    model_name: str
    dataset_name: str
    batch_size: int

data = {
    "ERYTHROID": [0.999338, 0.0, 0.022222, 0.005613, 0.0, 0.000292],
    "STROMA": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "MYELOID": [0.000000, 0.000000, 0.933333, 0.000000, 0.000000, 0.000584],
    "LYMPHOID": [0.000000, 0.363636, 0.000000, 0.986904, 0.153846, 0.002922],
    "PROGENITOR": [0.000331, 0.590909, 0.000000, 0.002806, 0.769231, 0.000584],
    "MK": [0.000331, 0.045455, 0.044444, 0.004677, 0.076923, 0.995617]
}

# Define row labels (index)
row_labels = ["ERYTHROID", "STROMA", "MYELOID", "LYMPHOID", "PROGENITOR", "MK"]

@app.post("/predict")
async def predict(request: Dataset):
    print(request.batch_size)
    print(request.model_name)
    print(request.dataset_name)

    df = pd.DataFrame(data, index=row_labels)

    return JSONResponse(content=df.to_dict())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
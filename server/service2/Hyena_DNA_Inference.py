from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Dataset(BaseModel):
    model_name: str
    dataset_name: str
    batch_size: int

data = [[225, 29],
        [55, 198]]


@app.post("/predict")
async def predict(request: Dataset):
    print(request.batch_size)
    print(request.model_name)
    print(request.dataset_name)


    return JSONResponse(content=data.to_json())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
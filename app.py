from nicegui import ui, app
import pandas as pd
from io import StringIO
import requests
import httpx

url = "http://localhost:8000/dataset"


#spinner = ui.spinner(size='lg').props('color=primary').classes(
 #   'fixed top-1/2 left-1/2 z-50'
#).bind_visibility_from(app.storage.user, 'loading')



# App State
class State:
    def __init__(self):
        self.input_data = None
        self.dataset = None
        self.model = None

state = State()

# Mock model functions (replace with your actual package)
def train_model(input_data, model_name, epochs, lr):
    if state.input_data is None:
        ui.notify("No data loaded! Upload data first.", type="negative")
        return
    if state.model is None:
        ui.notify("No model trained! Train a model first.", type="negative")
        return
    return f"Model trained with {model_name=}, {epochs=}, {lr=}."

def predict_model(input_data):
    if state.model is None:
        ui.notify("No model trained! Train a model first.", type="negative")
        return
    return f"Prediction for input: {input_data} (based on {state.model})"

# Initialize app
with ui.column().classes("items-center"):
    ui.markdown("# Helical Workflow Interface")

    # Tabs for different workflow steps
    with ui.tabs() as tabs:
        ui.tab("Data Upload", icon="upload")
        ui.tab("Training", icon="model_training")
        ui.tab("Application", icon="apps")

with ui.tab_panels(tabs, value="Data Upload"):
    #1. Data Upload Tab
    with ui.tab_panel("Data Upload"):
        with ui.card().classes("w-full p-4 gap-4"):
            # Option 1: Upload new file
            with ui.expansion("Upload New Data", icon="upload").classes("w-full"):
                ui.upload(
                    label='CSV/TSV or .h5ad (AnnData)',
                    auto_upload=True,
                    multiple=False,
                    on_upload=lambda e: handle_upload(e),
                ).classes("w-full")
                
                ui.button("Preview Uploaded Data", on_click=lambda: preview_data(uploaded_file))
            
            # Option 2: Select existing dataset
            with ui.expansion("Use Existing Dataset", icon="dataset").classes("w-full"):
                existing_datasets = [
                    "helical-ai/yolksac_human"
                ]
                
                dataset_select = ui.select(
                    options=existing_datasets,
                    label="Available Datasets",
                    with_input=True
                ).classes("w-full")
                
                ui.button("Load Selected Dataset", 
                        on_click=lambda: load_dataset(dataset_select.value),
                        icon="cloud_download").classes("w-full")

    # Tab 2: Model Training
    with ui.tab_panel("Training"):
        with ui.card().classes("w-full p-4 gap-4"):
            # Model Selection
            ui.label("Select Model Architecture").classes("text-lg font-medium")
            model_select = ui.select(
                options={
                    "Geneformer": "Geneformer (pretrained foundation model)",
                    "scGPT": "scGPT (pretrained foundation model)", 
                    "Mamba2-mRNA": "Mamba2-mRNA (custom architecture)",
                    "Helix-mRNA": "Helix",
                    "UCE": "Universal Cell Embedding",
                    "TranscriptFormer": "TranscriptFormer",
                    "HyenaDNA": "HyenaDNA (custom architecture)",
                    "Caduceus": "Caduceus (custom architecture)",
                    "Evo 2": "Evo 2 (custom architecture)"
                },
                label="Helical Models",
                value="Geneformer"
            ).classes("w-full")

            # Training Controls
            with ui.row().classes("items-center w-full"):
                batch_size = ui.number(
                    label="Batch Size", 
                    value=10, 
                    min=1, 
                    max=100
                ).classes("w-32")
                
                ui.space()
                
                train_btn = ui.button(
                    "Train Model", 
                    on_click=lambda: train_model(
                        model_select.value,
                        batch_size.value
                    ),
                    icon="play_arrow"
                )

    # Tab 3: Application
    with ui.tab_panel("Application"):
        #input_data = ui.input(label="Input for Prediction")
        ui.label("Select Application").classes("text-lg font-medium")

        model_select = ui.select(
                options={
                    "Cell type": "Cell type Annotation prediction",
                    "Cell type - fine tuning": "Cell type Annotation prediction (fine-tuning)", 
                    "Cell Gene Embeddings": "Cell Gene CLS Embeddings Generation",
                    "Helix-mRNA": "Helix",
                    "Genegpt": "GeneGPT sample run",
                    "Geneformer VS TranscriptFormer": "Comparison of Geneformer and TranscriptFormer",
                    "HyenaDNA - Fine Tuning": "HyenaDNA (fine-tuning)",
                    "HyenaDNA - Inference": "HyenaDNA (inference)",
                    "Evo 2": "Evo 2"
                },
                label="Helical Applications",
                value="Cell type"
            ).classes("w-full")

        ui.button("Run Application", on_click=lambda: run_application())

# Output Log
#output = ui.log(max_lines=10)

def preview_data(uploaded_file):
    if not uploaded_file.content:
        ui.notify("No file uploaded!", type="negative")
        return
    data = pd.read_csv(StringIO(uploaded_file.content.read().decode()))
    output.push(f"Data Preview:\n{data.head()}")

def train_and_show(param1, param2):
    # Simulate model training
    result = train_model(pd.DataFrame(), param1, param2)
    output.push(result)
    ui.notify("Model trained successfully!")


async def load_dataset(name):
    #app.storage.user['loading'] = True  # Show spinner

    # Replace with your dataset loading logic
    state.dataset = name
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json={"name": name})
    if response.status_code != 200:
        ui.notify(f"Failed to load dataset: {response.text}", type="negative")
    else:
        ui.notify(f"Successfully loaded dataset: {response.text}")
    #app.storage.user['loading'] = False  # Hide spinner

async def handle_upload(e):
    file = e.content  # arquivo em memória (BytesIO)
    filename = e.name
    # Enviar manualmente para o backend
    files = {'file': (filename, file, e.type)}
    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:8000/upload_file', files=files)
    if response.status_code == 200:
        ui.notify(f'File {filename} uploaded successfully!')
    else:
        ui.notify(f'Failed to upload {filename}', type='negative')


def run_application():
    # Simulate application logic
    ##
    result = run_model("trained_model", state.input_data)
    output.push(f"Application Result: {result}")

ui.run(title="Model Workflow", port=8080)
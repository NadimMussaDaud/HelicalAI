from nicegui import ui
import pandas as pd
from io import StringIO

# App State
class State:
    def __init__(self):
        self.input_data = None
        self.model = None
        self.prediction_result = None

state = State()

# Mock model functions
def train_model(model_name, epochs, lr):
    if state.input_data is None:
        ui.notify("No data loaded! Upload data first.", type="negative")
        return
    
    result = f"Training {model_name} on {len(state.input_data)} rows with {epochs=}, {lr=}"
    state.model = f"trained_{model_name}"
    return result

def predict_model():
    if not state.model:
        ui.notify("No trained model available!", type="negative")
        return
    return f"Prediction using {state.model} on {state.input_data.shape[0]} samples"

# Initialize app
ui.markdown("# Helical Workflow Interface").classes("text-2xl font-bold text-center mb-8")

# 1. Data Upload Section
with ui.card().classes("w-full p-6 mb-6 shadow-md"):
    ui.markdown("## Data Input").classes("text-xl font-semibold mb-4")
    
    # File Upload
    uploaded_file = ui.upload(
        label='Upload CSV/TSV or .h5ad (AnnData)',
        on_upload=lambda e: handle_upload(e)
    ).classes("w-full mb-4")
    
    # Dataset Selection
    with ui.row().classes("w-full items-center"):
        dataset_select = ui.select(
            options=[
                "10x Genomics PBMC",
                "Tabula Muris (Mouse)", 
                "Human Cell Atlas Blood"
            ],
            label="Or select example dataset",
            with_input=True
        ).classes("flex-grow")
        
        ui.button("Load", 
                on_click=lambda: load_dataset(dataset_select.value),
                icon="cloud_download").classes("ml-4")

# 2. Model Training Section
with ui.card().classes("w-full p-6 mb-6 shadow-md"):
    ui.markdown("## Model Training").classes("text-xl font-semibold mb-4")
    
    with ui.grid(columns=2).classes("w-full gap-4"):
        # Model Selection
        ui.select(
            options={
                "Geneformer": "Geneformer",
                "scGPT": "scGPT", 
                "Mamba2-mRNA": "Mamba2-mRNA"
            },
            label="Model Architecture",
            value="Geneformer"
        ).classes("col-span-2")
        
        # Training Parameters
        ui.number(label="Epochs", value=10, min=1).classes("w-full")
        ui.number(label="Learning Rate", value=0.001, format="%.4f").classes("w-full")
        
        # Train Button
        ui.button("Train Model", 
                on_click=lambda: train_action(),
                icon="play_arrow").classes("col-span-2")

# 3. Prediction Section
with ui.card().classes("w-full p-6 shadow-md"):
    ui.markdown("## Prediction").classes("text-xl font-semibold mb-4")
    
    ui.button("Run Prediction", 
            on_click=lambda: predict_action(),
            icon="rocket").classes("w-full mb-4")
    
    # Results Display
    with ui.expansion("Results", icon="insights").classes("w-full"):
        ui.label().bind_text_from(state, "prediction_result")

# Output and handlers
def handle_upload(e):
    try:
        content = e.content.read()
        if e.name.endswith('.h5ad'):
            ui.notify("Loading .h5ad file...")
            state.input_data = read_h5ad(content)  # Replace with your AnnData reader
        else:
            state.input_data = pd.read_csv(StringIO(content.decode()))
        ui.notify(f"Loaded {e.name} successfully!")
    except Exception as ex:
        ui.notify(f"Upload failed: {str(ex)}", type="negative")

def load_dataset(name):
    # Replace with your dataset loading logic
    state.input_data = pd.DataFrame()  # Mock data
    ui.notify(f"Loaded dataset: {name}")

def train_action():
    result = train_model(model_select.value, epochs.value, lr.value)
    ui.notify(result)

def predict_action():
    state.prediction_result = predict_model()
    
ui.run(title="Helical Workflow", port=8080)
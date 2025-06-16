from nicegui import ui
import pandas as pd
from io import StringIO


# App State
class State:
    def __init__(self):
        self.input_data = None
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
ui.markdown("# Helical Workflow Interface")

# Tabs for different workflow steps
with ui.tabs() as tabs:
    ui.tab("Data Upload", icon="upload")
    ui.tab("Training", icon="model_training")
    ui.tab("Prediction", icon="rocket")

with ui.tab_panels(tabs, value="Data Upload"):
    #1. Data Upload Tab
    with ui.tab_panel("Data Upload"):
        with ui.card().classes("w-full p-4 gap-4"):
            # Option 1: Upload new file
            with ui.expansion("Upload New Data", icon="upload").classes("w-full"):
                uploaded_file = ui.upload(
                      label='CSV/TSV or .h5ad (AnnData)',
                      on_upload=lambda e: handle_upload(e),
                ).classes("w-full")
                ui.button("Preview Uploaded Data", on_click=lambda: preview_data(uploaded_file))
            
            # Option 2: Select existing dataset
            with ui.expansion("Use Existing Dataset", icon="dataset").classes("w-full"):
                existing_datasets = [
                    "10x Genomics PBMC",
                    "Tabula Muris (Mouse)",
                    "Human Cell Atlas Blood",
                    "Custom Dataset 1",
                    "Custom Dataset 2"
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
                epochs = ui.number(
                    label="Epochs", 
                    value=10, 
                    min=1, 
                    max=100
                ).classes("w-32")
                
                lr = ui.number(
                    label="Learning Rate",
                    value=0.001,
                    format="%.04f",
                    step=0.0001
                ).classes("w-32")
                
                ui.space()
                
                train_btn = ui.button(
                    "Train Model", 
                    on_click=lambda: train_model(
                        model_select.value,
                        epochs.value,
                        lr.value
                    ),
                    icon="play_arrow"
                )

    # Tab 3: Prediction
    with ui.tab_panel("Prediction"):
        input_data = ui.input(label="Input for Prediction")
        ui.button("Run Prediction", on_click=lambda: show_prediction(input_data.value))

# Output Log
output = ui.log(max_lines=10)

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


def load_dataset(name):
    # Replace with your dataset loading logic
    state.input_data = pd.DataFrame()  # Mock data
    ui.notify(f"Loaded dataset: {name}")

def handle_upload(e):
    try:
        content = e.content.read()
        if e.name.endswith('.h5ad'):
            state.input_data = read_h5ad(content)  # Replace with your AnnData reader
        else:
            state.input_data = pd.read_csv(StringIO(content.decode()))
        ui.notify(f"Loaded {e.name} successfully!")
    except Exception as ex:
        ui.notify(f"Upload failed: {str(ex)}", type="negative")

def show_prediction(input_data):
    # Simulate prediction
    prediction = predict_model("trained_model", input_data)
    output.push(f"Prediction Result: {prediction}")

ui.run(title="Model Workflow", port=8080)
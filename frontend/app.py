from nicegui import ui
import pandas as pd
import requests
import httpx
import matplotlib.pyplot as plt
import seaborn as sns
import os
import base64
import io

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
url = f"{SERVER_URL}/dataset"

with ui.column().classes("items-center justify-center w-full"):
    ui.markdown("# Helical Workflow Interface").classes("text-center w-full")

result_zone = ui.column().classes("w-full items-center")


# App State
class State:
    def __init__(self):
        self.dataset = None
        self.application = None
        self.model = None
        self.batch_size = 10
        self.loading = False

state = State()

spinner = ui.spinner(size='lg').props('color=black').classes(
    'fixed top-1/2 left-1/2 z-50'
).bind_visibility_from(state, 'loading')

# Mock model functions (replace with your actual package)
def set_model(model_name, batch_size):
    state.model = model_name
    state.batch_size = batch_size
    ui.notify(f"Model set to {model_name} with batch size {batch_size}", type="success")
    if state.dataset is None:
        ui.notify("No data loaded! Upload data!", type="negative")
        return
    if state.model is None:
        ui.notify("No model trained! Train a model first.", type="negative")
        return

tabs_zone = ui.column()

# Initialize app

    
with tabs_zone.classes("justify-center items-center w-full"):
    # Tabs for different workflow steps
    with ui.tabs() as tabs:
        ui.tab("Data Upload", icon="upload")
        ui.tab("Training", icon="model_training")
        ui.tab("Application", icon="apps")
all_panels = ui.tab_panels(tabs, value="Data Upload").classes("w-full")
with all_panels:
    #1. Data Upload Tab
    with ui.tab_panel("Data Upload").classes("items-center justify-center"):
        with ui.card().classes("p-4 gap-4"):
            # Option 1: Upload new file
            with ui.expansion("Upload New Data", icon="upload").classes("w-full"):
                ui.upload(
                    label='CSV/TSV or .h5ad (AnnData)',
                    auto_upload=True,
                    multiple=False,
                    on_upload=lambda e: handle_upload(e),
                ).classes("w-full")
                
                #ui.button("Preview Uploaded Data", on_click=lambda: preview_data(uploaded_file))
            
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
    with ui.tab_panel("Training").classes("items-center justify-center"):
        with ui.card().classes("p-4 gap-4"):
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
                    "Set Model", 
                    on_click=lambda: set_model(
                        model_select.value,
                        batch_size.value
                    ),
                    icon="play_arrow"
                )

    # Tab 3: Application
    application_panel = ui.tab_panel("Application")
    with application_panel.classes("items-center justify-center"):
        ui.label("Select Application").classes("text-lg font-medium")

        application_select = ui.select(
                options={
                    "Cell type": "Cell type Annotation prediction",
                    #"Cell type - fine tuning": "Cell type Annotation prediction (fine-tuning)", 
                    #"Cell Gene Embeddings": "Cell Gene CLS Embeddings Generation",
                    #"Helix-mRNA": "Helix",
                    #"Genegpt": "GeneGPT sample run",
                    "Geneformer VS TranscriptFormer": "Comparison of Geneformer and TranscriptFormer",
                    #"HyenaDNA - Fine Tuning": "HyenaDNA (fine-tuning)",
                    "HyenaDNA - Inference": "HyenaDNA (inference)"
                    #"Evo 2": "Evo 2"
                },
                label="Helical Applications",
                value="Cell type"
            )

        ui.button("Run Application", on_click=lambda: run_application(application_select.value))

async def load_dataset(name):
    all_panels.style("display: none")  # Show application panel
    state.loading = True  # Show spinner

    # Replace with your dataset loading logic
    state.dataset = name
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json={"name": name})
    if response.status_code != 200:
        ui.notify(f"Failed to load dataset", type="negative")
    else:
        ui.notify(f"Successfully loaded dataset")
    state.loading = False  # Hide spinner
    all_panels.style("display: flex")  # Show application panel

async def handle_upload(e):
    all_panels.style("display: none")  # Show application panel
    state.loading = True  # Show spinner
    file = e.content  # arquivo em memória (BytesIO)
    filename = e.name
    # Enviar manualmente para o backend
    files = {'file': (filename, file, e.type)}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVER_URL}/upload_file", files=files)
    if response.status_code == 200:
        ui.notify(f'File {filename} uploaded successfully!')
        state.dataset = filename  # Update state with the uploaded filename
    else:
        ui.notify(f'Failed to upload {filename}', type='negative')
    state.loading = False  # Hide spinner
    all_panels.style("display: flex")  # Show application panel


def plot_results(data):
        result_zone.clear()  # Clear previous results


        with result_zone:
            ui.button("Back to Application", 
                    on_click=lambda: (result_zone.clear(), application_panel.style("display: flex"), tabs_zone.style("display: flex")),
                    icon="arrow_back").props("color=black").classes("mb-4")
            
        match state.application:
            case "Cell type":
                # Assuming data is a DataFrame with columns as cell types and rows as samples
                cm = pd.DataFrame(data)
                # Plot the confusion matrix
                fig, ax = plt.subplots(figsize=(12, 12))
                sns.heatmap(cm, annot=True, fmt=".2f", cmap="Blues", ax=ax)
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                plt.close(fig)
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode("utf-8")
                with result_zone:
                    ui.markdown("## Results").classes("text-lg font-medium")
                    # Display the image
                    ui.image(f'data:image/png;base64,{img_base64}').style("max-width: 100%; height: auto;").classes("w-full")
            case "HyenaDNA - Inference":
                plt.figure(figsize=(10,7))
                sns.heatmap(data, annot=True, fmt='d')
                plt.xlabel('Predicted')
                plt.ylabel('Truth')
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                plt.close()
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode("utf-8")
                with result_zone:
                    ui.markdown("## Results").classes("text-lg font-medium")
                    # Display the image
                    ui.image(f'data:image/png;base64,{img_base64}').style("max-width: 100%; height: auto;").classes("w-full")
            case "Geneformer VS TranscriptFormer":
                df = pd.DataFrame(data['data'])

                fig, ax = plt.subplots(figsize=(7, 5))
                sns.scatterplot(data=df, x='x',y='y',hue='Cell Type',sizes=(25,100),ax=ax,palette="pastel")
                ax.set_title('UMAP of Reference Data with labels')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close(fig)
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                with result_zone:
                    ui.markdown("## Results").classes("text-lg font-medium")
                    # Display the image
                    ui.image(f'data:image/png;base64,{img_base64}').style("max-width: 50%; height: auto;").classes("w-full")

async def run_application(application_name):
    tabs_zone.style("display: none")  # Hide tabs during processing
    application_panel.style("display: none")  # Show application panel
    # Simulate application logic
    state.application = application_name
    if state.model is None:
        ui.notify("No model set! Please set a model first.", type="negative")
        return
    if state.dataset is None:
        ui.notify("No dataset loaded! Please upload a dataset first.", type="negative")
        return
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{SERVER_URL}/run",
            json={
                "model_name": state.model,
                "application_name": application_name,
                "dataset_name": state.dataset,
                "batch_size": state.batch_size
            }
        )
    if response.status_code == 200:
        plot_results(response.json())
    

   
ui.run(title="Model Workflow", port=8080)
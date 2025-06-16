from nicegui import ui
import pandas as pd
from io import StringIO

# Mock model functions (replace with your actual package)
def train_model(data, param1, param2):
    return f"Model trained with {param1=}, {param2=} on {len(data)} rows."

def predict_model(model_result, input_data):
    return f"Prediction for input: {input_data} (based on {model_result})"

# Initialize app
ui.markdown("# Helical Workflow Interface")

# Tabs for different workflow steps
with ui.tabs() as tabs:
    ui.tab("Data Upload", icon="upload")
    ui.tab("Training", icon="train")
    ui.tab("Prediction", icon="rocket")

with ui.tab_panels(tabs, value="Data Upload"):
    # Tab 1: Data Upload
    with ui.tab_panel("Data Upload"):
        uploaded_file = ui.upload(label="Upload CSV", on_upload=lambda e: ui.notify(f"Uploaded {e.name}"))
        ui.button("Preview Data", on_click=lambda: preview_data(uploaded_file))

    # Tab 2: Model Training
    with ui.tab_panel("Training"):
        with ui.column():  # Wrap in column for better layout
            ui.label("Parameter 1")  # Separate label
            param1 = ui.slider(min=0, max=100, value=50)
            ui.label("Parameter 2")
            param2 = ui.number(value=1.0)
            ui.button("Train Model", on_click=lambda: train_and_show(param1.value, param2.value))

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

def show_prediction(input_data):
    # Simulate prediction
    prediction = predict_model("trained_model", input_data)
    output.push(f"Prediction Result: {prediction}")

ui.run(title="Model Workflow", port=8080)
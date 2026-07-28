## About the Project

This workspace contains code related to float32 to int8 conversion and demonstrates model quantization on a simple CNN model trained on MNIST dataset.

## Project Structure

The project is organized as follows:

```text
SUDAR-QUANTIZATION/
├── .venv/
├── .vscode/
├── task_06_pytorch_to_int8_tflite/
│   ├── calib/
│   ├── saved_model/
│   ├── __init__.py
│   ├── best-model.pth
│   ├── conversation_logger.text
│   ├── convert_model.py
│   ├── model_definition.py
│   ├── model_int8.tflite
│   ├── model.onnx
│   ├── model.onnx.data
│   └── train_save_calib.ipynb
├── .gitignore
├── pyproject.toml
├── README.md
├── task_01_basic_quantization.ipynb
├── task_02_scale_zero_point.ipynb
├── task_03_symmetric_asymmetric.ipynb
├── task_04_bit_width_comparison.ipynb
└── task_05_per_tensor_per_channel.ipynb
```

## Errors faced during Development:
- Task 1: As the task was much straight forward, I didn't get any error.
- Task 2: Initially chose an extremely small value 10^-9 for scale, but when the tensor's range (x_max - x_min < 10^-9>). Later I realized that the data to handle actually had smaller value within that range, so chose a higher tensor range of 10^-11 and used scale as 1.0 to prevent the explosion of quantized tensor at step x_min / scale.
- Task 3: During outlier calculation had some difficulty in plotting the heatmap for 1D array. 
- Task 4: Didn't face any issue during this task.
- Task 5: Made a semantic error. Used the global convolution variables reference everywhere instead of the one within the functional scope. Though these didn't change the result. I noticed it and changed it in the further steps.
- Task 6: Faced several issues. The most important one is not noticing the dim change between PyTorch and Tensorflow (TF mentions Tensor as [N, H, W, C] while PyTorch uses ([N, C, H, W])). This made the entire code crash without any error on the console and log file. 

## Requirements and Installation

### Prerequisites

Before running the projects, ensure you have the following installed:

- Python 3.11 or >
- uv (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/SUDAR2005/ai-ml-assessment.git/
cd ai_ml-assessment/onboarding-Quantization/Sudar-Quantization
```

### Install uv

If you don't have uv installed:

Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or install using pip:

```bash
pip install uv
```

### Create the Virtual Environment

```bash
uv venv
```

Activate the environment:

Windows

```bash
.venv\Scripts\activate
```

macOS / Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
uv sync
```

This command installs all dependencies specified in `pyproject.toml` and locks them according to `uv.lock`.
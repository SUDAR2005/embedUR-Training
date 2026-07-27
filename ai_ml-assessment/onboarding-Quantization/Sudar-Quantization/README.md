## About the Project

This workspace contains code related to f-32 to int8 conversion and demonstrates model quantization on a simple CNN model.

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
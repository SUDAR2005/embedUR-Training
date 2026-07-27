import os
import torch
from model_definition import SimpleCNN
# create logger
import logging
import sys
import onnx
import onnx2tf
import tensorflow as tf

import numpy as np

# Logger configuration
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[
                        logging.FileHandler("conversation_logger.text", mode="w"),
                        logging.StreamHandler(sys.stdout)
                    ],
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


MODEL_PATH = "./best-model.pth"
# load from the state dict and set to evaluation mode

def load_model():
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Checkpoint not found at {MODEL_PATH}")
        raise FileNotFoundError(f"Checkpoint not found")
    
    model = SimpleCNN()
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    except Exception as e:
        logger.error(f"Failed to load the model: {e}")
    model.eval()
    logger.info("Phase 1 completed: Model Loaded and set to eval mode")
    return model
    

CALIB_PATH = "./calib/"
CALIB_SIZE = 50
# validate calibration data

def validate_calibration_data():
    if not os.path.exists(CALIB_PATH):
        logger.error(f"Calibration Dataset not found at {CALIB_PATH}")
        raise FileNotFoundError(f"Missing Calibration Dataset")
    
    bin_files = [file for file in os.listdir(CALIB_PATH)]
    
    if len(bin_files) == 0 or len(bin_files) < CALIB_SIZE:
        logger.error("Folder is empty / No. of calib dataset is less than expected size")
        raise ValueError("Low or No calibration Data found")
    
    bin_files_np = []
    
    for bin_file in bin_files:
        path = os.path.join(CALIB_PATH, bin_file)
        try:
            loaded_bin = np.load(path)
        except Exception as e:
            logger.warning(f"Can't read file at {path}. Throws Exception {e}")
            continue
        # check input shape matches MNIST share (C, H, W)
        if loaded_bin.shape != (1, 28, 28):
            logger.warning(f"The saved numpy bin {path} doesn't match the expected shape... Skipping the file...")
            continue
        
        if np.isnan(loaded_bin).any() or np.isinf(loaded_bin).any():
            logger.warning(f"The Calib data contains Inf or NA values... Skipping Datapoint at {path}")
            continue
        bin_files_np.append(loaded_bin.astype(np.float32))
        
    # check valid bin file is empty
    if len(bin_files_np) == 0 or len(bin_files_np) < CALIB_SIZE:
        logger.error("Folder is empty / No. of calib dataset is less than expected size")
        raise ValueError("Low or No calibration Data found")
    logger.info(f"Step 2 complete: {len(bin_files_np)}/{len(bin_files_np)} calibration samples validated.")
    return bin_files_np

ONNX_PATH = "./model.onnx"
def export_onnx(model):
    dummy_input = torch.randn(1, 1, 28, 28, dtype=torch.float32)
    
    try:
        torch.onnx.export(model, dummy_input, ONNX_PATH,
                        input_names=["input"], output_names=["output"],
                        opset_version=13, dynamic_axes=None)
    
    except Exception as e:
        logger.error(f"ONNX export failed: {e}")
        raise Exception(f"Error in exporting to ONNX")
    
    try:
        onnx_model = onnx.load(ONNX_PATH)
        # check with model checker
        onnx.checker.check_model(onnx_model)
    except Exception as e:
        logger.error(f"ONNX model validation failed: {e}")
        raise

    logger.info(f"Step 3 complete: exported and validated '{ONNX_PATH}'.")

SAVED_MODEL_DIR = "saved_model"
def onnx_to_tf():
    try:
        onnx2tf.convert(
            input_onnx_file_path=ONNX_PATH, output_folder_path=SAVED_MODEL_DIR,
            non_verbose=True)
        
    except Exception as e:
        logger.error(f"ONNX to TensorFlow conversion failed: {e}")
        raise

    if not os.path.isdir(SAVED_MODEL_DIR):
        logger.error(f"Expected SavedModel directory '{SAVED_MODEL_DIR}' not found.")
        raise RuntimeError(f"SavedModel conversion did not produce output directory.")

    logger.info(f"Step 4 complete: SavedModel written to '{SAVED_MODEL_DIR}/'.")

TFLITE_PATH = "model_int8.tflite"

def convert_to_int8_tflite(calib_samples):
    def rep_data():
        for sample in calib_samples:
            nhwc_sample = np.transpose(sample, (1, 2, 0))       # (28, 28, 1)
            batched_data = np.expand_dims(nhwc_sample, axis=0)   # (1, 28, 28, 1)
            yield [batched_data.astype(np.float32)]
    
    try:
        converter = tf.lite.TFLiteConverter.from_saved_model(SAVED_MODEL_DIR)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = rep_data
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8
        tflite_model = converter.convert()
        
    except Exception as e:
        logger.error(f"INT8 TFLite conversion failed: {e}")
        raise

    with open(TFLITE_PATH, "wb") as f:
        f.write(tflite_model)

    logger.info(f"Step 5 complete: INT8 TFLite model saved to '{TFLITE_PATH}'.")


def verify_tflite_model(calib_samples):
    interpreter = tf.lite.Interpreter(model_path=TFLITE_PATH)
    interpreter.allocate_tensors()
    print(interpreter.get_input_details()[0]['shape'])
    
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    logger.info(f"Input dtype: {input_details['dtype']}")
    logger.info(f"Output dtype: {output_details['dtype']}")

    in_scale, in_zp = input_details["quantization"]
    out_scale, out_zp = output_details["quantization"]
    logger.info(f"Input scale/zero_point: {in_scale} / {in_zp}")
    logger.info(f"Output scale/zero_point: {out_scale} / {out_zp}")

    is_fully_int8 = (
        input_details["dtype"] == np.int8 and output_details["dtype"] == np.int8
    )
    if not is_fully_int8:
        logger.warning(
            "Model fell back to float I/O — not fully INT8. "
            "Check for unsupported ops in the graph."
        )
    else:
        logger.info("Confirmed: model is fully INT8 (input and output).")

    size_kib = os.path.getsize(TFLITE_PATH) / 1024
    logger.info(f"Model file size: {size_kib:.2f} KiB")
    sample = calib_samples[0]
    nhwc_sample = np.transpose(sample, (1, 2, 0))
    batched = np.expand_dims(nhwc_sample, axis=0).astype(np.float32)
    # quantize input manually to int8 using the input scale/zero_point
    quant_input = np.round(batched / in_scale + in_zp).astype(np.int8)

    interpreter.set_tensor(input_details["index"], quant_input)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details["index"])

    logger.info(f"Test inference raw INT8 output: {output}")

    # dequantize output for a human-readable prediction
    dequant_output = (output.astype(np.float32) - out_zp) * out_scale
    predicted_class = int(np.argmax(dequant_output))
    logger.info(f"Test inference dequantized output: {dequant_output}")
    logger.info(f"Predicted class: {predicted_class}")
    logger.info("Step 6 complete: verification finished.")
    

if __name__ == "__main__":
    model = load_model()
    calib_samples = validate_calibration_data()
    export_onnx(model)
    onnx_to_tf()
    convert_to_int8_tflite(calib_samples)
    verify_tflite_model(calib_samples)
    
    logger.info("Execution Completed")
    print("Execution Completed")
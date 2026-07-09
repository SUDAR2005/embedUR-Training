import shutil

import numpy as np
import torch
import cv2

# import preprecessing pipeline
from  image_preprocessing_pipeline import ImagePreprocessingPipeline
import os
import shutil

preprocess = ImagePreprocessingPipeline(resize_dim=(28, 28), normalize=True, gray_scale=True, argument=True)
def test_preprocess():
    image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)  # Random color image
    processed_image = preprocess.preprocess(image)
    
    assert processed_image.shape == (28, 28, 1), f"Expected shape (28, 28, 1), but got {processed_image.shape}"
    assert torch.all((processed_image >= 0.0) & (processed_image <= 1.0)), "Values should be between 0 and 1 after normalization"
    assert isinstance(processed_image, torch.Tensor), "Output should be a torch.Tensor"
    print("Preprocessing test passed!")
    
def test_split():
    os.makedirs('temp_dataset/class1', exist_ok=True)
    os.makedirs('temp_dataset/class2', exist_ok=True)

    for i in range(10):
        cv2.imwrite(f'temp_dataset/class1/img_{i}.jpg', np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8))
        cv2.imwrite(f'temp_dataset/class2/img_{i}.jpg', np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8))
    
    preprocess.test_train_split('temp_dataset', test_size=0.2, keep_old=False)
    
    # Check if the split was successful
    assert os.path.exists('temp_dataset/train/class1'), "Train directory for class1 not created"
    assert os.path.exists('temp_dataset/train/class2'), "Train directory for class2 not created"
    assert os.path.exists('temp_dataset/test/class1'), "Test directory for class1 not created"
    assert os.path.exists('temp_dataset/test/class2'), "Test directory for class2 not created"
    
    # Clean up
    # shutil.rmtree('temp_dataset')
    print("Train-test split test passed!")
    
def test_main():
    test_preprocess()
    test_split()
    print("All tests passed!")
    
if __name__ == "__main__":
    test_main()
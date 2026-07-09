import cv2
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import os 
import shutil
import pandas as pd

class ImagePreprocessingPipeline:
    def __init__(self, resize_dim=(28, 28), normalize = True, gray_scale = True, argument = False):
        self.resize_dim = resize_dim
        self.__normalize = normalize
        self.__gray_scale = gray_scale
        self.__argument = argument
        self.transform = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),     # 50% chance to flip horizontally
            transforms.RandomRotation(degrees=30),      # Rotate by up to 30 degrees
            transforms.ColorJitter(brightness=0.2),     # Randomly tweak brightness
            transforms.ToTensor()])                       # Convert PIL Image to PyTorch Tensor
            
    def _resize(self, image) -> np.ndarray:
        return cv2.resize(image, self.resize_dim)
    
    def _normalize(self, image) -> np.ndarray:
        return image / 255.0

    def _gray_scale(self, image) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _augment(self, image) -> np.ndarray:
        # convert the image to PIL format for torchvision transforms
        pil_image = Image.fromarray(image)
        augmented_image = self.transform(pil_image)
        # convert back to numpy array
        return augmented_image.permute(1, 2, 0).numpy()
    
    def preprocess(self, image: np.ndarray) -> torch.Tensor:
        if self.__gray_scale:
            image = self._gray_scale(image)
        image = self._resize(image)
        
        if self.__normalize:
            image = self._normalize(image)
        
        if self.__argument:
            image = self._augment(image)
        
        # convert to tensor
        image_tensor = torch.from_numpy(image).float()
        
        # if grayscale, add channel dimension
        if len(image_tensor.shape) == 2:
            image_tensor = image_tensor.unsqueeze(0)  # add channel dimension
        
        return image_tensor
    
    def test_train_split(self, path: str, test_size=0.2, keep_old = False, random_seed=42):
        
        root_folder = path
        train_folder = root_folder + '/train'
        test_folder = root_folder + '/test'
        # to write metadata
        metadata_file = os.path.join(root_folder, 'metadata.csv')
        metadata = []
        
        # purge old directory and build new directory
        if not keep_old:
            for folder in [train_folder, test_folder]:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                os.makedirs(folder)
        
        valid_extensions = ('.jpg', '.jpeg', '.png')
        # to get reproducible results set the random seed
        np.random.seed(random_seed)
        
        for class_folder in os.listdir(root_folder):
            class_path = os.path.join(root_folder, class_folder)
            if os.path.isdir(class_path):
                images = [file for file in os.listdir(class_path) if file.lower().endswith(valid_extensions)]
                num_images = len(images)
                num_test = int(num_images * test_size)

                # Shuffle images
                np.random.shuffle(images)
                
                test_images = images[:num_test]
                train_images = images[num_test:]
                
                # Create class folders in train and test directories
                if not os.path.exists(os.path.join(train_folder, class_folder)):
                    os.makedirs(os.path.join(train_folder, class_folder), exist_ok=True)
                if not os.path.exists(os.path.join(test_folder, class_folder)):
                    os.makedirs(os.path.join(test_folder, class_folder), exist_ok=True)
                
                # Move images to respective folders
                for img in train_images:
                    shutil.move(os.path.join(class_path, img), os.path.join(train_folder, class_folder, img))
                    metadata.append((os.path.join(train_folder, class_folder, img), class_folder, 'train'))
                for img in test_images:
                    shutil.move(os.path.join(class_path, img), os.path.join(test_folder, class_folder, img))
                    metadata.append((os.path.join(test_folder, class_folder, img), class_folder, 'test'))
        # save metadata to CSV
        df = pd.DataFrame(metadata, columns=['image_path', 'class', 'split'])
        df.to_csv(metadata_file, index=False)
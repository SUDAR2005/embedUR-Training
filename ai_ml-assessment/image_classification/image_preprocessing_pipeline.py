import cv2
import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import os
import shutil
import pandas as pd

class ImagePreprocessingPipeline:
    def __init__(self, resize_dim=(28, 28), normalize=True, gray_scale=True, argument=False):
        self.resize_dim = resize_dim
        self.__normalize = normalize
        self.__gray_scale = gray_scale
        self.__argument = argument
        self.transform = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=30),
            transforms.ColorJitter(brightness=0.2),
            transforms.ToTensor()])  # ToTensor already scales to [0,1]

    def _resize(self, image) -> np.ndarray:
        return cv2.resize(image, self.resize_dim)

    def _normalize(self, image) -> np.ndarray:
        return image / 255.0

    def _gray_scale(self, image) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _augment(self, image) -> np.ndarray:
        pil_image = Image.fromarray(image)
        augmented_image = self.transform(pil_image)
        return augmented_image.permute(1, 2, 0).numpy()

    def preprocess(self, image: np.ndarray) -> torch.Tensor:
        if self.__gray_scale:
            image = self._gray_scale(image)
        image = self._resize(image)

        # FIX: _augment() already applies ToTensor(), which scales pixels to [0,1].
        if self.__argument:
            image = self._augment(image)
        elif self.__normalize:
            image = self._normalize(image)

        image_tensor = torch.from_numpy(image).float()
        if len(image_tensor.shape) == 2:
            image_tensor = image_tensor.unsqueeze(0)  # add channel dimension

        return image_tensor

    def test_train_split(self, path: str, test_size=0.2, keep_old=False, random_seed=42, move_files=False):
        """
        move_files=False (default): copies images, leaving the source class
        folders intact. Safer for re-running / working with downloaded datasets.
        Set move_files=True to reproduce the old (destructive) behavior.
        """
        root_folder = path
        train_folder = os.path.join(root_folder, 'train')
        test_folder = os.path.join(root_folder, 'test')
        metadata_file = os.path.join(root_folder, 'metadata.csv')
        metadata = []

        if not keep_old:
            for folder in [train_folder, test_folder]:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                os.makedirs(folder)

        valid_extensions = ('.jpg', '.jpeg', '.png')
        np.random.seed(random_seed)

        # fix: skip 'train'/'test' (and metadata.csv) so re-running this function
        # doesn't treat previously-created output folders as class folders.
        skip_dirs = {os.path.basename(train_folder), os.path.basename(test_folder)}

        for class_folder in os.listdir(root_folder):
            if class_folder in skip_dirs:
                continue
            class_path = os.path.join(root_folder, class_folder)
            if not os.path.isdir(class_path):
                continue

            images = [f for f in os.listdir(class_path) if f.lower().endswith(valid_extensions)]
            num_images = len(images)
            num_test = int(num_images * test_size)

            np.random.shuffle(images)
            test_images = images[:num_test]
            train_images = images[num_test:]

            os.makedirs(os.path.join(train_folder, class_folder), exist_ok=True)
            os.makedirs(os.path.join(test_folder, class_folder), exist_ok=True)

            file_op = shutil.move if move_files else shutil.copy2

            for img in train_images:
                src = os.path.join(class_path, img)
                dst = os.path.join(train_folder, class_folder, img)
                file_op(src, dst)
                metadata.append((dst, class_folder, 'train'))
            for img in test_images:
                src = os.path.join(class_path, img)
                dst = os.path.join(test_folder, class_folder, img)
                file_op(src, dst)
                metadata.append((dst, class_folder, 'test'))

        df = pd.DataFrame(metadata, columns=['image_path', 'class', 'split'])
        df.to_csv(metadata_file, index=False)
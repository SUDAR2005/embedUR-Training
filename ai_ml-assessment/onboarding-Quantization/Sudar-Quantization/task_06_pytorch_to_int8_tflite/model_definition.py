import torch.nn as nn
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), # Using MNIST (1 -> 16 feature maps of 28 x 28)
            nn.ReLU(), # induce non-linearity resulting in learning complex features
            nn.MaxPool2d(2), # Reduce size to 14 x 14
            nn.Conv2d(16, 32, 3, padding=1), # (16 feature maps -> 32 Feature Maps of size 14 x 14)
            nn.ReLU(), 
            nn.MaxPool2d(2), # reduce Size to 7 x 7
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 64), # from last max-pooling layer
            nn.ReLU(),
            nn.Linear(64, num_classes), 
        )
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
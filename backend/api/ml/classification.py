import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import os


# Load pretrained ResNet50 model
model = resnet50(pretrained=True)
model.eval()

# Get the imagenet classes path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABELS_PATH = os.path.join(BASE_DIR, 'imagenet_classes.txt')

# Load labels
try:
    with open(LABELS_PATH, 'r') as f:
        labels = f.read().splitlines()
except FileNotFoundError:
    labels = [f"class_{i}" for i in range(1000)]

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])
])


def classify_image(image_path):
    """Classify an image using ResNet50 model and return top 3 predictions."""
    try:
        img = Image.open(image_path).convert("RGB")
        input_tensor = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)

        # Get probabilities for all classes
        probabilities = torch.softmax(output, dim=1)[0]
        
        # Get top 3 predictions
        top_k = 3
        top_probs, top_indices = torch.topk(probabilities, k=top_k)
        
        # Build results for top 3
        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            idx = idx.item()
            prob = prob.item()
            label = labels[idx] if idx < len(labels) else f"class_{idx}"
            predictions.append({
                'label': label,
                'confidence': round(prob, 4),
                'percentage': round(prob * 100, 2)
            })
        
        return {
            'predictions': predictions,
            'top_prediction': predictions[0]['label'],
            'top_confidence': predictions[0]['confidence']
        }
    except Exception as e:
        return {
            'predictions': [],
            'top_prediction': 'Error',
            'top_confidence': 0.0,
            'error': str(e)
        }

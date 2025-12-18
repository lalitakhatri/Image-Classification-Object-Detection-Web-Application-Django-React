# API Reference - Image AI Processing Platform

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### POST /api/process/

Process an image with filters, classification, and object detection.

#### Request

**Content-Type:** `multipart/form-data`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | File | Yes | Image file (JPEG, PNG, etc.) |
| filter | String | No | Filter name (default: "grayscale") |

**Example with cURL:**
```bash
curl -X POST http://localhost:8000/api/process/ \
  -F "image=@image.jpg" \
  -F "filter=blur"
```

**Example with Python requests:**
```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'image': f}
    data = {'filter': 'sepia'}
    response = requests.post(
        'http://localhost:8000/api/process/',
        files=files,
        data=data
    )
    print(response.json())
```

**Example with JavaScript fetch:**
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('filter', 'canny');

const response = await fetch('http://localhost:8000/api/process/', {
  method: 'POST',
  body: formData
});
const result = await response.json();
```

#### Response

**Success (200 OK):**
```json
{
  "success": true,
  "image": "media/image_abc123.jpg",
  "filter_applied": "blur",
  "classification": {
    "label": "golden retriever",
    "confidence": 0.9234
  },
  "objects": [
    {
      "class": "dog",
      "confidence": 0.8745,
      "bbox": [120, 150, 380, 450]
    },
    {
      "class": "person",
      "confidence": 0.7823,
      "bbox": [50, 80, 200, 320]
    }
  ],
  "detected_image": "media/image_abc123_det.jpg"
}
```

**Error Response (400):**
```json
{
  "error": "No image file provided"
}
```

**Error Response (500):**
```json
{
  "error": "Internal server error message"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| success | Boolean | Indicates if processing was successful |
| image | String | Path to the processed image |
| filter_applied | String | Name of the filter that was applied |
| classification | Object | Image classification results |
| classification.label | String | Detected object/scene label |
| classification.confidence | Float | Confidence score (0-1) |
| objects | Array | Array of detected objects |
| objects[].class | String | Object class name |
| objects[].confidence | Float | Detection confidence (0-1) |
| objects[].bbox | Array | Bounding box [x1, y1, x2, y2] |
| detected_image | String | Path to the image with detection boxes |

#### Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (missing image, invalid format) |
| 405 | Method not allowed (use POST) |
| 500 | Server error |

### HTTP Status Codes

- **200 OK**: Request successful
- **400 Bad Request**: Missing required parameters or invalid input
- **405 Method Not Allowed**: Wrong HTTP method
- **500 Internal Server Error**: Server-side error

## Available Filters

The `filter` parameter accepts any of these values:

| Filter | Description | Use Case |
|--------|-------------|----------|
| grayscale | Black and white conversion | Converting to grayscale |
| blur | Gaussian blur | Smoothing/blurring |
| canny | Edge detection (Canny algorithm) | Finding edges |
| sepia | Sepia tone effect | Vintage/warm effect |
| negative | Inverted colors | Negative effect |
| sharpen | Image sharpening | Enhancing details |
| emboss | Embossed effect | 3D-like effect |
| median | Median blur | Noise reduction |
| bilateral | Bilateral filter | Edge-preserving blur |
| threshold | Binary threshold | Black and white conversion |
| sobel | Sobel edge detection | Edge detection |
| laplacian | Laplacian edge detection | Edge detection |
| hsv | HSV color space | Color analysis |
| erosion | Morphological erosion | Thinning objects |
| dilation | Morphological dilation | Thickening objects |
| edge_enhance | Edge enhancement | Sharpening edges |

## Models Used

### Image Classification
- **Model**: ResNet50 (PyTorch)
- **Dataset**: ImageNet (1000 classes)
- **Input Size**: 224x224 pixels
- **Output**: Single class label with confidence

### Object Detection
- **Model**: YOLOv8 Nano (Ultralytics)
- **Classes**: 80 COCO classes
- **Speed**: Real-time on CPU
- **Output**: Multiple objects with class, confidence, and bounding box

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
    }
}
```

## Authentication

Currently, no authentication is required. For production, consider adding:

```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

## Performance Metrics

### Processing Times (Average on CPU)
| Operation | Time |
|-----------|------|
| Image upload | < 1s |
| Filter application | 0.1 - 2s |
| Classification | 1 - 3s |
| Object detection | 2 - 5s |
| Total | 3 - 10s |

Note: Times vary based on image size and system specs

### File Size Limits
- Recommended max: 5MB
- Hard max: Limited by server configuration
- Optimal size: < 2MB

## CORS Headers

The API includes CORS support. Allowed origins:
- http://localhost:3000
- http://127.0.0.1:3000

To add more origins, edit `CORS_ALLOWED_ORIGINS` in settings.py:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://yourdomain.com",
]
```

## Error Handling

### Common Errors

**Missing Image File:**
```json
{
  "error": "No image file provided"
}
```

**Invalid Image File:**
```json
{
  "error": "Could not read image file"
}
```

**Server Error:**
```json
{
  "error": "Internal server error details"
}
```

### Error Codes

| Error | Status | Solution |
|-------|--------|----------|
| No image file provided | 400 | Include 'image' field in request |
| Could not read image file | 400 | Ensure valid image format |
| Invalid filter name | 500 | Check filter spelling |
| Model not loaded | 500 | Restart server, check model download |
| Internal server error | 500 | Check server logs, restart server |

## Examples

### Python Example

```python
import requests
import json

def process_image(image_path, filter_name='grayscale'):
    url = 'http://localhost:8000/api/process/'
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {'filter': filter_name}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Classification: {result['classification']['label']}")
            print(f"Detected objects: {len(result['objects'])}")
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.json())

# Usage
result = process_image('my_image.jpg', 'blur')
```

### JavaScript Example

```javascript
async function processImage(imageFile, filter = 'grayscale') {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('filter', filter);
  
  try {
    const response = await fetch('http://localhost:8000/api/process/', {
      method: 'POST',
      body: formData
    });
    
    const result = await response.json();
    
    console.log(`Label: ${result.classification.label}`);
    console.log(`Confidence: ${result.classification.confidence}`);
    console.log(`Objects detected: ${result.objects.length}`);
    
    return result;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Usage
const fileInput = document.getElementById('imageInput');
processImage(fileInput.files[0], 'sepia');
```

### cURL Example

```bash
# Simple request
curl -X POST http://localhost:8000/api/process/ \
  -F "image=@test.jpg"

# With filter
curl -X POST http://localhost:8000/api/process/ \
  -F "image=@test.jpg" \
  -F "filter=canny"

# Save response to file
curl -X POST http://localhost:8000/api/process/ \
  -F "image=@test.jpg" \
  -F "filter=sepia" \
  > response.json
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial release |

## Support & Documentation

- API Base URL: `http://localhost:8000/api/`
- Frontend: `http://localhost:3000/`
- Admin Panel: `http://localhost:8000/admin/`

For more information, see the main README.md file.

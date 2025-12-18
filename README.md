# Image AI Processing Platform

A complete full-stack application for image processing with AI capabilities. The platform provides:
- **15+ Image Filters** (grayscale, blur, canny, sepia, sharpen, emboss, etc.)
- **Image Classification** using ResNet50 (ImageNet)
- **Object Detection** using YOLOv8

## Project Structure

```
backend/
├── backend/
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
├── api/
│   ├── models.py
│   ├── views.py             # API endpoints
│   ├── urls.py              # API routes
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── filters.py       # Image filters
│   │   ├── classification.py # ResNet50 model
│   │   └── detection.py     # YOLOv8 model
│   └── migrations/
├── media/                    # Uploaded images
├── manage.py
└── imagenet_classes.txt     # ImageNet labels

frontend/
├── src/
│   ├── components/
│   │   └── ImageUpload.js   # Main upload component
│   ├── App.js
│   ├── index.js
│   ├── App.css
│   └── index.css
├── public/
├── package.json
├── tailwind.config.js       # Tailwind CSS config
└── postcss.config.js        # PostCSS config
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip and npm
- Virtual environment tool

### Backend Setup

1. **Create Python Virtual Environment**
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install django djangorestframework django-cors-headers
pip install opencv-python torch torchvision
pip install ultralytics pillow
```

3. **Run Migrations**
```bash
python manage.py migrate
```

4. **Start Django Development Server**
```bash
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Install Tailwind CSS (if not already installed)**
```bash
npm install -D tailwindcss postcss autoprefixer
```

3. **Start React Development Server**
```bash
npm start
```

Frontend runs at: `http://localhost:3000`

## Available Filters

The application includes 15+ image filters:

1. **grayscale** - Convert to grayscale
2. **blur** - Gaussian blur
3. **canny** - Edge detection (Canny)
4. **sepia** - Sepia tone effect
5. **negative** - Negative/inverted image
6. **sharpen** - Sharpen filter
7. **emboss** - Emboss effect
8. **median** - Median blur
9. **bilateral** - Bilateral filter (edge-preserving blur)
10. **threshold** - Binary threshold
11. **sobel** - Sobel edge detection
12. **laplacian** - Laplacian edge detection
13. **hsv** - Convert to HSV color space
14. **erosion** - Morphological erosion
15. **dilation** - Morphological dilation
16. **edge_enhance** - Edge enhancement

## API Endpoints

### POST /api/process/

Process an image with filter, classification, and object detection.

**Request:**
```json
{
  "image": <file>,
  "filter": "grayscale"
}
```

**Response:**
```json
{
  "success": true,
  "image": "path/to/processed/image.jpg",
  "filter_applied": "grayscale",
  "classification": {
    "label": "dog",
    "confidence": 0.95
  },
  "objects": [
    {
      "class": "dog",
      "confidence": 0.92,
      "bbox": [100, 150, 300, 400]
    }
  ],
  "detected_image": "path/to/detected/image.jpg"
}
```

## Features

✔ **Real-time Image Processing** - Instant filter application
✔ **ResNet50 Image Classification** - Classify images using ImageNet
✔ **YOLOv8 Object Detection** - Detect and locate objects in images
✔ **15+ Image Filters** - Comprehensive image manipulation
✔ **Responsive UI** - Tailwind CSS design
✔ **Error Handling** - Comprehensive error messages
✔ **CORS Support** - Cross-origin requests enabled
✔ **Media Serving** - View processed images

## Configuration

### Django Settings (`backend/settings.py`)
- DEBUG = True (development)
- ALLOWED_HOSTS = ['*']
- INSTALLED_APPS includes: rest_framework, corsheaders, api
- MEDIA_ROOT configured for image storage
- CORS_ALLOWED_ORIGINS configured for localhost:3000

### Environment Variables
Create a `.env` file in the backend directory if needed for production:
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=your-secret-key
```

## Running the Application

1. **Terminal 1 - Start Backend**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

2. **Terminal 2 - Start Frontend**
```bash
cd frontend
npm start
```

3. **Open Browser**
Navigate to: `http://localhost:3000`

## Troubleshooting

### Model Download Issues
- YOLOv8 model auto-downloads on first use
- ResNet50 model auto-downloads with PyTorch

### Port Already in Use
```bash
# Change Django port
python manage.py runserver 8001

# Change React port
PORT=3001 npm start
```

### CORS Errors
Ensure backend includes `corsheaders` in INSTALLED_APPS and MIDDLEWARE

### Module Not Found
Install missing packages:
```bash
pip install -r requirements.txt  # Backend
npm install  # Frontend
```

## Development

### Adding New Filters
Edit `backend/api/ml/filters.py` and add filter function in `apply_filter()`

### Customizing UI
Edit React components in `frontend/src/components/`

### Modifying ML Models
Update imports and functions in `backend/api/ml/` modules

## Performance Considerations

- Image size: Recommended < 5MB
- Large images may be slower to process
- YOLOv8 nano (yolov8n) used for speed
- GPU acceleration available with CUDA

## License

Open source project

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure both servers are running
4. Check browser console for frontend errors
5. Check terminal for backend errors
"# Image-Classification-Object-Detection-Web-Application-Django-React" 

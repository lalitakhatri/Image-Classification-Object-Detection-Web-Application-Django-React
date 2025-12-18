# Quick Start Guide - Image AI Processing Platform

## One-Command Setup (Windows)

### Option 1: Using Batch Script

Create a `setup.bat` file in the project root:

```batch
@echo off
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
echo Backend setup complete!
```

Then run:
```bash
setup.bat
```

### Option 2: Manual Setup

#### Step 1: Backend Setup (Terminal 1)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### Step 2: Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
npm start
```

**Expected Output:**
```
webpack compiled with warnings
Compiled successfully!
You can now view frontend in the browser.
Local: http://localhost:3000
```

#### Step 3: Open Application
- Open `http://localhost:3000` in your web browser
- You should see the "Image AI Processing" page

## First Use - Test the Application

1. **Upload an Image**
   - Click "Select Image" and choose a JPEG or PNG image
   - Image preview will appear

2. **Select a Filter**
   - Choose from 15+ available filters
   - "grayscale" is the default

3. **Process Image**
   - Click "Process Image" button
   - Processing may take 5-30 seconds depending on image size

4. **View Results**
   - Classification result shows detected object and confidence
   - Detected objects list shows all detected items
   - Links to view processed and detection images

## File Locations

### Important Directories
- **Backend**: `backend/` - Django REST API
- **Frontend**: `frontend/` - React UI
- **Media**: `backend/media/` - Processed images storage
- **ML Models**: `backend/api/ml/` - Image processing code

### Key Files
- `backend/backend/settings.py` - Django configuration
- `backend/api/views.py` - API endpoints
- `frontend/src/components/ImageUpload.js` - Main UI component
- `frontend/src/App.js` - React app root

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Cannot find module 'react'"
**Solution:**
```bash
cd frontend
npm install
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
python manage.py runserver 8001
```

### Issue: "Port 3000 already in use"
**Solution:**
```bash
set PORT=3001
npm start
```

### Issue: CORS Error in browser console
**Solution:**
- Verify backend is running on http://localhost:8000
- Check `CORS_ALLOWED_ORIGINS` in backend/settings.py

### Issue: Images not processing / timeout
**Solution:**
- Try with a smaller image (< 2MB)
- Check backend console for error messages
- Ensure YOLOv8 model has downloaded

## Model Downloads

The first time you run the application:
- ResNet50 model will download (~100MB) - takes ~2-5 minutes
- YOLOv8 model will download (~35MB) - takes ~1-3 minutes

This only happens once. Subsequent runs will be faster.

## Performance Tips

1. **Use Smaller Images**
   - Recommended: 640x480 to 1024x768
   - Max recommended: 2048x1536

2. **GPU Acceleration** (Optional)
   - Install CUDA if you have an NVIDIA GPU
   - Automatically uses GPU if available

3. **Filter Selection**
   - Simple filters (grayscale, blur) are fastest
   - Edge detection filters (canny, sobel) take longer

## Next Steps

### Customize Filters
Edit `backend/api/ml/filters.py` to add or modify filters

### Change Models
Edit `backend/api/ml/classification.py` or `detection.py` to use different models

### Modify UI
Edit React components in `frontend/src/components/`

### Deploy to Production
See main README.md for production deployment guide

## Support & Troubleshooting

1. **Check Backend Logs**
   - Look at terminal where you ran `python manage.py runserver`

2. **Check Frontend Logs**
   - Open Browser DevTools (F12)
   - Check Console tab for errors

3. **Test API Directly**
   - Use Postman or curl to test `/api/process/` endpoint
   - Verify backend is responding

4. **Verify Dependencies**
   - Run `pip list` to see installed packages
   - Run `npm list` to see frontend packages

## Quick Reference Commands

```bash
# Activate backend environment
cd backend
venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver

# Deactivate virtual environment
deactivate

# Install frontend dependencies
cd frontend
npm install

# Start React dev server
npm start

# Build for production
npm run build
```

## Environment Files

### Backend (.env - Optional)
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=your-generated-key
```

### Frontend (.env - Optional)
```
REACT_APP_API_URL=http://localhost:8000
```

## Ready to Go!

You're all set! The Image AI Processing Platform is ready to use.

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Admin Panel: http://localhost:8000/admin (if needed)

Enjoy processing images with AI! 🎉
